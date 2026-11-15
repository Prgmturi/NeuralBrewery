"""What the dashboard asks the API, over HTTP, and the API's errors in words.

The brewer's token goes only with the three requests that need it:
propose, approve and reject. Every other request carries nothing, so no
read can leak it. Every error, of the API or of the network, becomes an
ApiError with a sentence in Italian and the status: the page shows it as
it is, a 401 included.
"""

from typing import Any

import httpx

from neuralbrewery.dashboard.settings import DashboardSettings

TOKEN_HEADER = "X-Approval-Token"
# A day of brew in one advance takes about 4 s of the API
TIMEOUT_S = 30.0
# A diagnosis is up to twelve calls of the model: httpx's 5 s would cut it
DIAGNOSIS_TIMEOUT_S = 180.0
# Listed in the API's description only while the simulation is on
SIMULATION_PATH = "/simulation/advance"

WORDS = {
    401: "Token di approvazione mancante o sbagliato",
    404: "Non trovato",
    409: "La proposta non è più in attesa: è già stata decisa",
    422: "Richiesta non valida",
    502: "Il fornitore del modello ha dato una risposta inutilizzabile",
    503: (
        "Servizio non disponibile: per la diagnosi, manca la chiave del modello "
        "o il fornitore non risponde"
    ),
}

JSON = dict[str, Any]


class ApiError(Exception):
    """What went wrong, for the brewer: a sentence, the status, the API's detail."""


def words(response: httpx.Response) -> str:
    """A failed answer as a sentence, with the status and the detail of the API."""
    status = response.status_code
    sentence = f"{WORDS.get(status, "Errore dell'API")} (HTTP {status})"
    try:
        detail = response.json().get("detail")
    except ValueError:  # not JSON: a proxy's page, for one
        detail = None
    return f"{sentence}: {detail}" if isinstance(detail, str) and detail else sentence


class Api:
    """The API of NeuralBrewery, as the brewer's dashboard uses it."""

    def __init__(self, http: httpx.Client, token: str) -> None:
        self._http = http
        self._token = token

    def plant(self) -> JSON:
        result: JSON = self._send("GET", "/plant").json()
        return result

    def simulation_on(self) -> bool:
        """Whether the API exposes the routes that move time and break the plant.

        Its description lists them only then. Out of development there is
        no description, and no simulation either: production refuses it.
        """
        response = self._request("GET", "/openapi.json")
        return response.status_code == 200 and SIMULATION_PATH in response.json().get(
            "paths", {}
        )

    def advance(self, seconds: float) -> JSON:
        result: JSON = self._send(
            "POST", "/simulation/advance", json={"seconds": seconds}
        ).json()
        return result

    def inject_fault(self, kind: str, target: str, value: float | None) -> None:
        fault = {"kind": kind, "target": target, "value": value}
        self._send("POST", "/simulation/faults", json=fault)

    def clear_faults(self) -> None:
        self._send("DELETE", "/simulation/faults")

    def diagnose(self) -> JSON:
        """The run of the agent and, if it proposed a button, its place in the queue."""
        result: JSON = self._send(
            "POST", "/agents/plant/diagnose", timeout=DIAGNOSIS_TIMEOUT_S
        ).json()
        return result

    def proposals(self) -> list[JSON]:
        """The queue, the newest first, each proposal with its story."""
        result: list[JSON] = self._send("GET", "/approvals").json()
        return result

    def propose(self, command: str, why: str, by: str) -> JSON:
        body = {"command": command, "why": why, "by": by}
        result: JSON = self._send("POST", "/approvals", json=body, token=True).json()
        return result

    def approve(self, proposal_id: str, by: str) -> JSON:
        path = f"/approvals/{proposal_id}/approve"
        result: JSON = self._send("POST", path, json={"by": by}, token=True).json()
        return result

    def reject(self, proposal_id: str, by: str, reason: str) -> JSON:
        path = f"/approvals/{proposal_id}/reject"
        body = {"by": by, "reason": reason}
        result: JSON = self._send("POST", path, json=body, token=True).json()
        return result

    def _send(
        self,
        method: str,
        path: str,
        *,
        json: JSON | None = None,
        token: bool = False,
        timeout: float = TIMEOUT_S,
    ) -> httpx.Response:
        response = self._request(method, path, json=json, token=token, timeout=timeout)
        if response.is_error:
            raise ApiError(words(response))
        return response

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: JSON | None = None,
        token: bool = False,
        timeout: float = TIMEOUT_S,
    ) -> httpx.Response:
        # Without a token no header at all: the API answers 401, and says so
        headers = {TOKEN_HEADER: self._token} if token and self._token else {}
        try:
            return self._http.request(
                method, path, json=json, headers=headers, timeout=timeout
            )
        except httpx.TimeoutException as error:
            raise ApiError(f"L'API non ha risposto in tempo ({timeout:g} s)") from error
        except httpx.HTTPError as error:
            url = str(self._http.base_url).rstrip("/")
            raise ApiError(f"L'API non risponde a {url}: è accesa?") from error


def connect(
    settings: DashboardSettings | None = None,
    transport: httpx.BaseTransport | None = None,
) -> Api:
    """The API of the settings, with the brewer's token."""
    settings = settings or DashboardSettings()
    http = httpx.Client(base_url=settings.api_url, transport=transport)
    return Api(http, settings.approval_token.get_secret_value())
