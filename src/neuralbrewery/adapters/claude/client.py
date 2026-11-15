"""Claude through datapizza: the client, and what every call carries.

datapizza's Anthropic client passes any extra argument of a call on to the
Anthropic SDK, and the SDK sends extra_headers and extra_body as they are.
That is how the fallback on refusals and the prompt cache reach the API
with no client of our own (docs/decisioni.md, "datapizza con Claude").

ClaudeClient changes one thing: the errors of the SDK become the app's
(ADR 0006), so the agent endpoint answers 503 or 502, not 500. The SDK
retries by itself before giving up (twice, on connection errors, 429 and
5xx); what reaches here is final.
"""

from typing import Any

import anthropic
from datapizza.clients.anthropic import AnthropicClient
from datapizza.core.clients import ClientResponse

from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.exceptions import ExternalServiceError, ServiceUnavailableError

# On a refusal the API runs the same request again on the model it picks
# for that kind of refusal, inside the same call
FALLBACK_BETA = "server-side-fallback-2026-07-01"
SERVICE = "Claude"


class ClaudeClient(AnthropicClient):
    """datapizza's client for Claude, with the errors translated, no more.

    - no answer (connection refused, timeout): ServiceUnavailableError, 503;
    - busy or down (429, 5xx, 529 overloaded): ServiceUnavailableError, 503;
    - any other refusal (400, a wrong key, an unknown model): 502.
    """

    # *args and **kwargs, passed on as they come: datapizza's Client and its
    # AnthropicClient declare two signatures that no third one matches
    async def _a_invoke(self, *args: Any, **kwargs: Any) -> ClientResponse:
        try:
            response: ClientResponse = await super()._a_invoke(*args, **kwargs)
        except anthropic.APIConnectionError as error:  # timeouts included
            raise ServiceUnavailableError(SERVICE) from error
        except anthropic.APIStatusError as error:
            if error.status_code == 429 or error.status_code >= 500:
                raise ServiceUnavailableError(SERVICE) from error
            raise ExternalServiceError(
                SERVICE, f"Claude refused the request ({error.status_code})"
            ) from error
        return response


def create_client(settings: ClaudeSettings) -> ClaudeClient:
    """The datapizza client for the model of the settings. No call is made."""
    return ClaudeClient(
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
