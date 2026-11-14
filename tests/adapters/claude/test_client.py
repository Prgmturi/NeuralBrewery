"""Tests for the Claude adapter.

Under test: src/neuralbrewery/adapters/claude/client.py
No network: building the client makes no call.

WHY these tests exist: the step-1 trial of M5 (docs/decisioni.md) found
what datapizza leaves to the caller with Claude: max_tokens falls back to
2048, effort is not set, a forced tool_choice is a 400. These arguments are
the whole fix, so a lost one would change every diagnosis without a sign.
"""

from datapizza.clients.anthropic import AnthropicClient

from neuralbrewery.adapters.claude.client import (
    FALLBACK_BETA,
    create_client,
    generation_args,
)
from neuralbrewery.core.config.claude import ClaudeSettings


def test_the_client_takes_model_and_key_from_the_settings():
    """[HP] One client per model; the key goes to the SDK and nowhere else."""
    client = create_client(
        ClaudeSettings(api_key="sk-ant-test", model="claude-opus-5-5")
    )

    assert isinstance(client, AnthropicClient)
    assert client.model_name == "claude-opus-5-5"
    assert client.api_key == "sk-ant-test"


def test_every_call_carries_tokens_effort_fallback_and_cache():
    """[HP] What datapizza would otherwise leave out or get wrong."""
    args = generation_args(ClaudeSettings(max_tokens=9000, effort="medium"))

    assert args == {
        "max_tokens": 9000,
        "output_config": {"effort": "medium"},
        "extra_headers": {"anthropic-beta": FALLBACK_BETA},
        "extra_body": {
            "fallbacks": "default",
            "cache_control": {"type": "ephemeral"},
        },
    }


def test_no_call_forces_a_tool():
    """[EC] A forced tool_choice is a 400 on the current Claude models."""
    assert "tool_choice" not in generation_args(ClaudeSettings())
