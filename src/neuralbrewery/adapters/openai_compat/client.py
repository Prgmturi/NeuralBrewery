"""An API that copies OpenAI's, through datapizza: Gemini by default.

datapizza's OpenAILikeClient speaks the chat completions of OpenAI to any
address: base URL, model and key are settings (docs/decisioni.md, "Secondo
fornitore"). OpenAICompatClient changes three things, no more:

- the errors of the SDK become the app's (ADR 0006), so the agent endpoint
  answers 503 or 502, not 500;
- Gemini's thought signatures go back with the conversation. Gemini 3 signs
  the first tool call of each answer, and refuses with a 400 a conversation
  whose tool calls come back unsigned; datapizza drops the signature when it
  turns its memory into messages. The client keeps it by the id of the call,
  and puts it back. Other providers send none, and nothing changes for them;
- the calls of one answer go back in one message, as the model sent them:
  datapizza writes one message per call, and Gemini refuses the second of
  two parallel calls as an unsigned turn.

The SDK retries by itself before giving up (twice, with short waits, on
connection errors, 429 and 5xx): what reaches here is final.
"""

from collections import OrderedDict
from typing import Any

import openai
from datapizza.clients.openai_like import OpenAILikeClient
from datapizza.core.clients import ClientResponse
from datapizza.memory import Memory
from datapizza.tools import Tool

from neuralbrewery.core.config.openai_compat import OpenAICompatSettings
from neuralbrewery.core.exceptions import ExternalServiceError, ServiceUnavailableError

SERVICE = "OpenAI-compatible API"
# Per call. A diagnosis on Gemini Flash-Lite writes a few hundred tokens a call
MAX_TOKENS = 8192
# One client serves the app for its whole life: the signatures of the latest
# calls are enough, as a conversation needs only its own
SIGNATURES_KEPT = 256


class OpenAICompatClient(OpenAILikeClient):
    """datapizza's OpenAI-like client, with the errors translated.

    - no answer (connection refused, timeout): ServiceUnavailableError, 503;
    - over the limits or down (429, 5xx): ServiceUnavailableError, 503;
    - any other refusal (400, a wrong key, a model gone): 502;
    - an answer that cannot be used (arguments that are not JSON, a tool
      that does not exist, no choice at all): 502.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._signatures: OrderedDict[str, str] = OrderedDict()

    # *args and **kwargs, passed on as they come, as in adapters/claude
    async def _a_invoke(self, *args: Any, **kwargs: Any) -> ClientResponse:
        try:
            response: ClientResponse = await super()._a_invoke(*args, **kwargs)
        except openai.APIConnectionError as error:  # timeouts included
            raise ServiceUnavailableError(SERVICE) from error
        except openai.APIStatusError as error:
            if error.status_code == 429 or error.status_code >= 500:
                raise ServiceUnavailableError(SERVICE) from error
            raise ExternalServiceError(
                SERVICE, f"The model refused the request ({error.status_code})"
            ) from error
        except (ValueError, IndexError) as error:
            # Raised by datapizza as it reads the answer
            raise ExternalServiceError(
                SERVICE, "The model gave an answer that cannot be used"
            ) from error
        return response

    def _response_to_client_response(
        self, response: Any, tool_map: dict[str, Tool] | None
    ) -> ClientResponse:
        for choice in response.choices:
            for call in choice.message.tool_calls or []:
                extra = (call.model_extra or {}).get("extra_content") or {}
                signature = (extra.get("google") or {}).get("thought_signature")
                if signature:
                    self._signatures[call.id] = signature
                    while len(self._signatures) > SIGNATURES_KEPT:
                        self._signatures.popitem(last=False)
        result: ClientResponse = super()._response_to_client_response(
            response, tool_map
        )
        return result

    def _memory_to_contents(
        self, system_prompt: str | None, input: str, memory: Memory | None = None
    ) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = super()._memory_to_contents(
            system_prompt, input, memory
        )
        merged: list[dict[str, Any]] = []
        for message in messages:
            for call in message.get("tool_calls") or []:
                signature = self._signatures.get(call["id"])
                if signature:
                    call["extra_content"] = {"google": {"thought_signature": signature}}
            if _more_calls_of_the_same_answer(merged, message):
                last = merged[-1]
                last["tool_calls"] = [
                    *last.get("tool_calls", []),
                    *message["tool_calls"],
                ]
            else:
                merged.append(message)
        return merged


def _more_calls_of_the_same_answer(
    merged: list[dict[str, Any]], message: dict[str, Any]
) -> bool:
    """A message of calls alone, right after one of the model: the same answer.

    datapizza sends each call of an answer as a message of its own. Gemini
    takes each one as a turn, whose first call must be signed, and refuses
    the unsigned ones with a 400; OpenAI wants them in one message too.
    """
    return (
        bool(merged)
        and merged[-1]["role"] == "assistant"
        and message["role"] == "assistant"
        and bool(message.get("tool_calls"))
        and not message.get("content")
    )


def create_client(settings: OpenAICompatSettings) -> OpenAICompatClient:
    """The datapizza client for the API of the settings. No call is made."""
    return OpenAICompatClient(
        api_key=settings.api_key.get_secret_value(),
        model=settings.model,
        base_url=settings.base_url,
    )


def generation_args() -> dict[str, Any]:
    """The arguments of every call of an agent, given to Agent.a_run().

    Only a token budget: effort, the prompt cache and the fallback on
    refusals are Claude's (adapters/claude). datapizza sends it as
    max_completion_tokens.
    """
    return {"max_tokens": MAX_TOKENS}
