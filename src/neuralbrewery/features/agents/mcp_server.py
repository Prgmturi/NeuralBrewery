"""The MCP server of the app: read the plant, propose an action. Nothing more.

Mounted in the API at /mcp over HTTP (bootstrap.py), so an MCP client such
as Claude Code sees the same plant and the same queue as the API. The four
reading tools are the plant agent's own functions (tools.py).
propose_action drops a proposal in the queue through the ProposalInbox
port, as from "mcp": out of limits it is blocked, and the reason comes
back as an answer.

The server receives a reader and the inbox, nothing else: no settings,
so no approval token, and no executor, so no button. AGENTS.md, rule 1.
"""

import json
from typing import Annotated, Any

from mcp.server.mcpserver import MCPServer
from pydantic import Field

from neuralbrewery.core.approvals.protocols import ProposalInbox
from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.plant.panel import BUTTONS
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.readonly import ReadOnlyPlant
from neuralbrewery.core.state import StateKey
from neuralbrewery.features.agents.tools import reading_functions

# Set by bootstrap.py; the lifespan runs its session manager
MCP_SERVER = StateKey[MCPServer]("mcp_server")

# Who proposes, in the audit: MCP gives no identity to trust
BY = "mcp"

INSTRUCTIONS = (
    "Il server di NeuralBrewery, un birrificio pilota simulato da 20 L. Leggi "
    "l'impianto con i tool di lettura; con propose_action proponi al birraio un "
    "pulsante del pannello. Non puoi comandare né approvare: il birraio approva o "
    "rifiuta, e solo allora l'impianto esegue. Il tempo è simulato (sim_time_s)."
)

COMMAND = "Il pulsante del pannello"
ARGUMENTS = (
    "Gli argomenti del pulsante per nome, per esempio "
    '{"vessel": "FERM", "celsius": 18}; vuoto per un pulsante che non ne prende'
)
WHY = "Perché lo proponi: per il birraio, in italiano, breve"


def _buttons() -> str:
    """Each button with its arguments: needed, and optional with a ?."""
    return "; ".join(
        f"{command}({', '.join([*button.needs, *(f'{n}?' for n in button.takes)])})"
        for command, button in BUTTONS.items()
    )


PROPOSE = (
    "Proponi al birraio un pulsante del pannello. La proposta va in coda e "
    "aspetta la sua approvazione: non viene eseguita adesso. Fuori dai limiti è "
    "bloccata, e la risposta dice perché. Pulsanti: "
    + _buttons()
    + ". route: hlt_to_mash, hlt_to_boil, mash_recirc, mash_to_boil, boil_to_ferm. "
    "vessel: HLT, MASH, BOIL, FERM. celsius assente spegne il recipiente; liters "
    "assente su mash_recirc ricircola finché non lo si ferma."
)


def create_mcp_server(reader: PlantReader, inbox: ProposalInbox) -> MCPServer:
    plant = ReadOnlyPlant(reader)  # whatever the caller hands in
    server: MCPServer = MCPServer(name="neuralbrewery", instructions=INSTRUCTIONS)
    for function in reading_functions(plant):
        server.add_tool(function)

    async def propose_action(
        command: Annotated[str, Field(description=COMMAND)],
        arguments: Annotated[
            dict[str, Any] | None, Field(description=ARGUMENTS)
        ] = None,
        why: Annotated[str, Field(description=WHY)] = "",
    ) -> str:
        receipt = await inbox.propose(command, arguments or {}, Actor.MCP, BY, why)
        # The id and the outcome: no real time, a model reads it (rule 5)
        return json.dumps(
            {
                "proposal_id": str(receipt.proposal_id),
                "status": receipt.status,
                "reason": receipt.reason,
            },
            ensure_ascii=False,
        )

    server.add_tool(propose_action, description=PROPOSE)
    return server
