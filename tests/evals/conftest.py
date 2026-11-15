"""Eval fixtures: the real model of AGENT_PROVIDER, its key, what each scenario cost.

Every test in this folder gets the ``eval`` marker. A plain ``pytest``
leaves them out (addopts in pyproject.toml): they call a real model, and CI
has no key. ``uv run pytest -m eval`` runs only them, by hand.

The provider is AGENT_PROVIDER, as for the app: claude by default, or
openai_compat (Gemini on its free tier). Provider and keys come exported or
from .env, although the autouse fixture of tests/conftest.py switches both
off for every other test.

The cost is measured on the answers of the API, through a hook of the HTTP
client: datapizza keeps the tokens read from Claude's prompt cache but not
those written to it, and with the cache on most of the input goes through
it. The free tier of Gemini costs nothing, but allows 15 requests a minute:
a scenario makes up to 12, so there scenarios start a minute apart.

At the end, a table of this run, then one comparing the last run of each
provider. In .evals/<provider>/, one JSON per scenario: the diagnosis, every
step of the trace, the tokens, the cost.
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic
import openai
import pytest
from datapizza.core.clients import Client

from neuralbrewery.adapters.claude import client as claude_adapter
from neuralbrewery.adapters.openai_compat import client as compat_adapter
from neuralbrewery.core.config.agent import AgentSettings
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.config.openai_compat import OpenAICompatSettings
from neuralbrewery.features.agents.diagnosis import DiagnosisRun

HERE = Path(__file__).parent
REPOSITORY = HERE.parent.parent
ENV_FILE = REPOSITORY / ".env"
OUT = REPOSITORY / ".evals"

# Read before the autouse fixture of tests/conftest.py removes them
EXPORTED = {
    name: os.environ[name]
    for name in (
        "AGENT_PROVIDER",
        "ANTHROPIC_API_KEY",
        "OPENAI_COMPAT_API_KEY",
        "OPENAI_COMPAT_BASE_URL",
        "OPENAI_COMPAT_MODEL",
    )
    if os.environ.get(name)
}

# Dollars per million tokens. claude-sonnet-5-5: a cache write costs 1.25
# times the input, a cache read a twentieth of it. Gemini: the free tier
PRICES = {
    "claude": {"input": 2.00, "output": 10.00, "cache_write": 2.50, "cache_read": 0.10},
    "openai_compat": {
        "input": 0.0,
        "output": 0.0,
        "cache_write": 0.0,
        "cache_read": 0.0,
    },
}
KINDS = ("input", "output", "cache_write", "cache_read")

# Gemini's free tier: 15 requests a minute, and a scenario makes up to 12
PAUSE_S = 60.0


# tryfirst: the marker must be there before pytest deselects by -m.
# The hook sees the items of the whole run, hence the path check.
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if item.path.is_relative_to(HERE):
            item.add_marker(pytest.mark.eval)


@dataclass
class Meter:
    """The usage of every call that reached the model, as the API reported it."""

    provider: str
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def on_response(self, response: Any) -> None:
        path = response.request.url.path
        if not path.endswith(("/messages", "/chat/completions")):
            return
        await response.aread()
        body = response.json()
        if response.status_code != 200:
            self.calls.append({"status": response.status_code, "error": body})
        elif path.endswith("/messages"):
            usage = body["usage"]
            self.calls.append(
                {
                    "model": body["model"],
                    "stop_reason": body["stop_reason"],
                    "input": usage["input_tokens"],
                    "output": usage["output_tokens"],
                    "cache_write": usage.get("cache_creation_input_tokens") or 0,
                    "cache_read": usage.get("cache_read_input_tokens") or 0,
                }
            )
        else:
            usage = body.get("usage") or {}
            cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens")
            cached = cached or 0
            self.calls.append(
                {
                    "model": body["model"],
                    "stop_reason": (body.get("choices") or [{}])[0].get(
                        "finish_reason"
                    ),
                    "input": (usage.get("prompt_tokens") or 0) - cached,
                    "output": usage.get("completion_tokens") or 0,
                    "cache_write": 0,
                    "cache_read": cached,
                }
            )

    def total(self, kind: str) -> int:
        return sum(call.get(kind, 0) for call in self.calls)

    def cost(self) -> float:
        prices = PRICES[self.provider]
        return sum(self.total(kind) * prices[kind] for kind in KINDS) / 1e6


def settings_from_env(cls: Any, monkeypatch: pytest.MonkeyPatch) -> Any:
    for name, value in EXPORTED.items():
        monkeypatch.setenv(name, value)
    return cls(_env_file=ENV_FILE)


@pytest.fixture
def provider(monkeypatch: pytest.MonkeyPatch) -> str:
    return str(settings_from_env(AgentSettings, monkeypatch).provider)


@pytest.fixture
def meter(provider: str) -> Meter:
    return Meter(provider)


def hooked(meter: Meter, default_client: Any) -> Any:
    return default_client(event_hooks={"response": [meter.on_response]})


_last_start: list[float] = []


@pytest.fixture
async def model(
    provider: str, meter: Meter, monkeypatch: pytest.MonkeyPatch
) -> tuple[Client, dict[str, Any]]:
    """The client of the adapter, with the meter on its HTTP client, and its args.

    datapizza builds its async SDK client on the first call, unless one is
    there already: this one is, with the hook on every answer.
    """
    if provider == "openai_compat":
        compat = settings_from_env(OpenAICompatSettings, monkeypatch)
        if not compat.api_key.get_secret_value():
            pytest.fail(
                "OPENAI_COMPAT_API_KEY is missing: export it, or put it in .env"
            )
        client: Client = compat_adapter.create_client(compat)
        client.a_client = openai.AsyncOpenAI(
            api_key=compat.api_key.get_secret_value(),
            base_url=compat.base_url,
            http_client=hooked(meter, openai.DefaultAsyncHttpxClient),
        )
        if _last_start:
            wait = PAUSE_S - (time.monotonic() - _last_start[-1])
            await asyncio.sleep(max(0.0, wait))
        _last_start.append(time.monotonic())
        return client, compat_adapter.generation_args()

    claude = settings_from_env(ClaudeSettings, monkeypatch)
    if not claude.api_key.get_secret_value():
        pytest.fail("ANTHROPIC_API_KEY is missing: export it, or put it in .env")
    client = claude_adapter.create_client(claude)
    client.a_client = anthropic.AsyncAnthropic(
        api_key=claude.api_key.get_secret_value(),
        http_client=hooked(meter, anthropic.DefaultAsyncHttpxClient),
    )
    return client, claude_adapter.generation_args(claude)


RESULTS: list[dict[str, Any]] = []


@pytest.fixture
def record(provider: str, meter: Meter) -> Any:
    """Keep the result of a scenario for the tables and for .evals/<provider>/."""

    def keep(name: str, title: str, run: DiagnosisRun, failures: list[str]) -> None:
        result = {
            "scenario": name,
            "title": title,
            "provider": provider,
            "passed": not failures,
            "failures": failures,
            "run": run.model_dump(mode="json"),
            "usage": {
                "calls": meter.calls,
                **{kind: meter.total(kind) for kind in KINDS},
                "cost_usd": round(meter.cost(), 4),
            },
        }
        RESULTS.append(result)
        folder = OUT / provider
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{name}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return keep


def _model_of(result: dict[str, Any]) -> str:
    models = [call["model"] for call in result["usage"]["calls"] if "model" in call]
    return models[0] if models else "-"


def _input(usage: dict[str, Any]) -> int:
    return int(usage["input"] + usage["cache_write"] + usage["cache_read"])


def pytest_terminal_summary(terminalreporter: Any) -> None:
    if not RESULTS:
        return
    write = terminalreporter.write_line
    terminalreporter.section(f"eval: plant agent on {RESULTS[0]['provider']}")
    write(
        f"{'scenario':<28}{'verdict':<9}{'calls':>6}{'in':>8}{'out':>8}"
        f"{'cache w':>9}{'cache r':>9}{'cost $':>9}"
    )
    for result in RESULTS:
        usage = result["usage"]
        write(
            f"{result['scenario'] + ' ' + result['title']:<28.27}"
            f"{'PASS' if result['passed'] else 'FAIL':<9}"
            f"{len(usage['calls']):>6}{usage['input']:>8}{usage['output']:>8}"
            f"{usage['cache_write']:>9}{usage['cache_read']:>9}"
            f"{usage['cost_usd']:>9.4f}"
        )
        for failure in result["failures"]:
            write(f"    - {failure}")
    total = sum(result["usage"]["cost_usd"] for result in RESULTS)
    passed = sum(result["passed"] for result in RESULTS)
    write(
        f"{passed}/{len(RESULTS)} passed, total cost ${total:.4f}. Details in .evals/"
    )

    # The last run of each provider, from .evals/
    last = [
        json.loads(path.read_text(encoding="utf-8"))
        for name in PRICES
        for path in sorted((OUT / name).glob("S*.json"))
    ]
    if len({result["provider"] for result in last}) < 2:
        return
    terminalreporter.section("eval: the providers compared, last run of each")
    write(
        f"{'scenario':<28}{'model':<24}{'verdict':<9}{'in':>8}{'out':>7}{'cost $':>9}"
    )
    for result in sorted(last, key=lambda result: result["scenario"]):
        usage = result["usage"]
        write(
            f"{result['scenario'] + ' ' + result['title']:<28.27}"
            f"{_model_of(result):<24.23}"
            f"{'PASS' if result['passed'] else 'FAIL':<9}"
            f"{_input(usage):>8}{usage['output']:>7}{usage['cost_usd']:>9.4f}"
        )
    for name in PRICES:
        mine = [result for result in last if result["provider"] == name]
        write(
            f"{name}: {sum(r['passed'] for r in mine)}/{len(mine)} passed, "
            f"${sum(r['usage']['cost_usd'] for r in mine):.4f}"
            + (" (free tier)" if name == "openai_compat" else "")
        )
