"""The simulated plant: process, devices and controller, moved on together.

One calculation step, always in this order:

1. the devices obey the outputs of the controller, and the wired safety
   looks at the true temperatures;
2. the process moves on by one step;
3. the devices measure it;
4. the controller reads the signals and decides its outputs.

The step is fixed when the simulator is made, and time is a count of whole
steps: the same seed with the same actions gives the same plant, to the
last digit. Nothing here reads the real clock.
"""

from neuralbrewery.adapters.plant_sim import faults
from neuralbrewery.adapters.plant_sim.controller.controller import Controller
from neuralbrewery.adapters.plant_sim.devices.field import Field
from neuralbrewery.adapters.plant_sim.process import Process
from neuralbrewery.core.exceptions import ValidationError
from neuralbrewery.core.plant.schemas import Fault

HISTORY_WINDOW_S = 24 * 3600
HISTORY_PERIOD_S = 60


class PlantSimulator:
    def __init__(
        self,
        process: Process,
        *,
        seed: int = 42,
        step_s: int = 1,
        hydrometer_on: bool = False,
        history_window_s: int = HISTORY_WINDOW_S,
        history_period_s: int = HISTORY_PERIOD_S,
    ) -> None:
        """A plant around that process. starts.py has the ready-made ones."""
        if step_s < 1:
            raise ValueError(f"the calculation step is at least 1 s, not {step_s}")
        self.process = process  # the true values: for tests and evals only
        self.step_s = step_s
        self.field = Field(seed, hydrometer_on=hydrometer_on)
        self._steps = 0
        self.controller = Controller(
            self.field.measure(process, 0.0),
            history_window_s=history_window_s,
            history_period_s=history_period_s,
        )

    @property
    def time_s(self) -> int:
        """Simulated time: whole steps, so it never drifts."""
        return self._steps * self.step_s

    def advance(self, seconds: float) -> None:
        """Move on by that long, which must be a whole number of steps."""
        steps, rest = divmod(seconds, self.step_s)
        if seconds < 0 or rest:
            raise ValidationError(
                f"{seconds:g} s is not a whole number of steps of {self.step_s} s",
                field="seconds",
            )
        for _ in range(int(steps)):
            self._step()

    def _step(self) -> None:
        heat_w, flows = self.field.actuate(self.controller.outputs, self.process)
        self.process.step(self.step_s, heat_w, flows)
        self._steps += 1
        self.controller.scan(self.field.measure(self.process, self.time_s), self.time_s)

    def inject_fault(self, fault: Fault) -> None:
        """Raises ValidationError for a fault its target cannot have."""
        faults.apply(fault, self.field, self.process)

    def clear_faults(self) -> None:
        faults.clear(self.field, self.process)
