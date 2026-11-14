"""Actuators: what the controller commands, and what each does about it.

A fault is a flag on the device: the command still arrives, the device
does something else. What the controller can learn of it is only what the
device is wired to say (signals.py).
"""

from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.signals import DriveStatus, ValveContacts

DRIVE_FREQUENCY_HZ = 50.0
DRIVE_CURRENT_A = 1.2


@dataclass
class Pump:
    on: bool = False
    blocked: bool = False  # fault: seized, or it lost its prime

    @property
    def pumping(self) -> bool:
        return self.on and not self.blocked


@dataclass
class Valve:
    """A motorised ball valve. It gets there within one calculation step.

    The 5-wire version, with two end contacts. To be verified: the manual
    in data/manuals/ is of the 3-wire one (docs/impianto.md, "Da verificare").
    """

    open: bool = False
    stuck: bool = False  # fault: it stays where it is

    def command(self, open_: bool) -> None:
        if not self.stuck:
            self.open = open_

    @property
    def contacts(self) -> ValveContacts:
        return ValveContacts(open=self.open, closed=not self.open)


@dataclass
class Heater:
    """An element with its solid state relay, fed through K1."""

    rated_w: float
    shorted: bool = False  # fault of the relay: on whatever the command
    open_circuit: bool = False  # fault of the element: it never heats

    def power_w(self, commanded_pct: float, powered: bool) -> float:
        if self.open_circuit or not powered:
            return 0.0
        return self.rated_w * (1.0 if self.shorted else commanded_pct / 100.0)


@dataclass
class Drive:
    """The inverter of the agitator. A fault stays until it is acknowledged."""

    run: bool = False
    fault_code: int | None = None
    cause: int | None = None  # fault: the code the drive trips with

    def command(self, run: bool, acknowledge: bool) -> None:
        self.run = run
        if self.cause is not None:
            self.fault_code = self.cause
        elif acknowledge:
            self.fault_code = None

    @property
    def status(self) -> DriveStatus:
        running = self.run and self.fault_code is None
        return DriveStatus(
            running=running,
            frequency_hz=DRIVE_FREQUENCY_HZ if running else 0.0,
            current_a=DRIVE_CURRENT_A if running else 0.0,
            fault_code=self.fault_code,
        )
