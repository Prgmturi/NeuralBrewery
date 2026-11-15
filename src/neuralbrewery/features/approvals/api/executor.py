"""The executor: the only code that holds PlantCommander (AGENTS.md, rule 1).

It presses the button of a proposal the brewer approved, and nothing
else: the domain calls it after the approval is written, through the
Panel port. bootstrap.py builds it on the plant and keeps it in app.state
under EXECUTOR, typed as the Panel: what reads it there gets press(), not
the buttons.
"""

from collections.abc import Awaitable, Callable

from neuralbrewery.core.plant.panel import BUTTONS
from neuralbrewery.core.plant.protocols import PlantCommander
from neuralbrewery.core.plant.schemas import CommandResult, Proposal
from neuralbrewery.core.state import StateKey
from neuralbrewery.features.approvals.domain.proposal import Action, Answer
from neuralbrewery.features.approvals.domain.protocols import Panel

EXECUTOR = StateKey[Panel]("executor")


class Executor:
    def __init__(self, commander: PlantCommander) -> None:
        self._commander = commander

    async def press(self, action: Action) -> Answer:
        """The method of the button, with the arguments it takes.

        The guardrail checked the action before it was queued; pydantic
        turns its JSON back into the names of the plant.
        """
        proposal = Proposal.model_validate(
            {"command": action.command, **action.arguments}
        )
        button = BUTTONS[proposal.command]
        names = (*button.needs, *button.takes)
        method: Callable[..., Awaitable[CommandResult]] = getattr(
            self._commander, proposal.command.value
        )
        result = await method(**{name: getattr(proposal, name) for name in names})
        return Answer(
            accepted=result.accepted, code=result.code.value, reason=result.reason
        )
