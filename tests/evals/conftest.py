"""Eval fixtures: the real Claude, its key, and what each scenario cost.

Every test in this folder gets the ``eval`` marker. A plain ``pytest``
leaves them out (addopts in pyproject.toml): they cost money, and CI has no
key. ``uv run pytest -m eval`` runs only them, by hand.

The key comes from ANTHROPIC_API_KEY, exported or in .env, although the
autouse fixture of tests/conftest.py switches both off for every other test.

The cost is measured on the answers of the API, through a hook of the HTTP
client: datapizza keeps the tokens read from the prompt cache but not those
written to it, and with the cache on most of the input goes through it.
At the end, a table of the scenarios, and in .evals/ one JSON per scenario:
the diagnosis, every step of the trace, the tokens, the cost.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic
import pytest
from datapizza.clients.anthropic import AnthropicClient

from neuralbrewery.adapters.claude.client import create_client
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.features.agents.diagnosis import DiagnosisRun

HERE = Path(__file__).parent
REPOSITORY = HERE.parent.parent
OUT = REPOSITORY / ".evals"

# Read before the autouse fixture of tests/conftest.py removes it
EXPORTED_KEY = os.environ.get("ANTHROPIC_API_KEY")

# claude-sonnet-5-5, dollars per million tokens. A cache write costs 1.25
# times the input, a cache read a twentieth of it
PRICES = {"input": 2.00, "output": 10.00, "cache_write": 2.50, "cache_read": 0.10}


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

    calls: list[dict[str, Any]] = field(default_factory=list)

    async def on_response(self, response: Any) -> None:
        if not response.request.url.path.endswith("/messages"):
            return
        await response.aread()
        body = response.json()
        if response.status_code != 200:
            self.calls.append({"status": response.status_code, "error": body})
            return
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

    def total(self, kind: str) -> int:
        return sum(call.get(kind, 0) for call in self.calls)

    def cost(self) -> float:
        return sum(self.total(kind) * price for kind, price in PRICES.items()) / 1e6


@pytest.fixture
def claude_settings(monkeypatch: pytest.MonkeyPatch) -> ClaudeSettings:
    if EXPORTED_KEY:
        monkeypatch.setenv("ANTHROPIC_API_KEY", EXPORTED_KEY)
    settings = ClaudeSettings(_env_file=REPOSITORY / ".env")
    if not settings.api_key.get_secret_value():
        pytest.fail("ANTHROPIC_API_KEY is missing: export it, or put it in .env")
    return settings


@pytest.fixture
def meter() -> Meter:
    return Meter()


@pytest.fixture
def claude(claude_settings: ClaudeSettings, meter: Meter) -> AnthropicClient:
    """The client of the adapter, with the meter on its HTTP client.

    datapizza builds its async SDK client on the first call, unless one is
    there already: this one is, with the hook on every answer.
    """
    client = create_client(claude_settings)
    client.a_client = anthropic.AsyncAnthropic(
        api_key=claude_settings.api_key.get_secret_value(),
        http_client=anthropic.DefaultAsyncHttpxClient(
            event_hooks={"response": [meter.on_response]}
        ),
    )
    return client


RESULTS: list[dict[str, Any]] = []


@pytest.fixture
def record(meter: Meter) -> Any:
    """Keep the result of a scenario for the table and for .evals/."""

    def keep(name: str, title: str, run: DiagnosisRun, failures: list[str]) -> None:
        result = {
            "scenario": name,
            "title": title,
            "passed": not failures,
            "failures": failures,
            "run": run.model_dump(mode="json"),
            "usage": {
                "calls": meter.calls,
                **{kind: meter.total(kind) for kind in PRICES},
                "cost_usd": round(meter.cost(), 4),
            },
        }
        RESULTS.append(result)
        OUT.mkdir(exist_ok=True)
        (OUT / f"{name}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return keep


def pytest_terminal_summary(terminalreporter: Any) -> None:
    if not RESULTS:
        return
    write = terminalreporter.write_line
    terminalreporter.section("M5 eval: plant agent on Claude")
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
