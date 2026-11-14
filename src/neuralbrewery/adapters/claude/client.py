"""Claude through datapizza: the client, and what every call carries.

datapizza's Anthropic client passes any extra argument of a call on to the
Anthropic SDK, and the SDK sends extra_headers and extra_body as they are.
That is how the fallback on refusals and the prompt cache reach the API
with no client of our own (docs/decisioni.md, "datapizza con Claude").

Errors of the SDK are not translated here (ADR 0006): they are raised
inside datapizza's loop, where this module has no hand. docs/decisioni.md
keeps it open until the agents are served by the API.
"""

from typing import Any

from datapizza.clients.anthropic import AnthropicClient

from neuralbrewery.core.config.claude import ClaudeSettings

# On a refusal the API runs the same request again on the model it picks
# for that kind of refusal, inside the same call
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def create_client(settings: ClaudeSettings) -> AnthropicClient:
    """The datapizza client for the model of the settings. No call is made."""
    return AnthropicClient(
        api_key=settings.api_key.get_secret_value(), model=settings.model
    )


def generation_args(settings: ClaudeSettings) -> dict[str, Any]:
    """The arguments of every call of an agent, given to Agent.a_run().

    No tool_choice: datapizza turns "required" or a list of names into a
    forced tool, which the current Claude models refuse with a 400. The
    agents leave it to "auto".
    """
    return {
        "max_tokens": settings.max_tokens,
        "output_config": {"effort": settings.effort},
        "extra_headers": {"anthropic-beta": FALLBACK_BETA},
        "extra_body": {
            "fallbacks": "default",
            # Each call of a loop sends the whole conversation again: the part
            # already sent is read from the cache, for a twentieth of the
            # input price on claude-sonnet-5-5
            "cache_control": {"type": "ephemeral"},
        },
    }
