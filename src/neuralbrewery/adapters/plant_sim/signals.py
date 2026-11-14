"""The wires between the field and the controller.

Everything the controller knows about the plant arrives in a FieldInputs,
and everything it does leaves in a FieldOutputs. There is no other way
between the two: the controller imports this module, and neither the
devices nor the process (import contract in pyproject.toml).

A device says only what its manual lets it say. A pump has no wire back,
so nothing here speaks of a pump that runs.
"""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValveContacts:
    """The two end contacts of a motorised valve."""

    open: bool
    closed: bool


@dataclass(frozen=True, slots=True)
class DriveStatus:
    """What the drive of the agitator answers on its serial line."""

    running: bool
    frequency_hz: float
    current_a: float
    fault_code: int | None


@dataclass(frozen=True, slots=True)
class HydrometerMessage:
    """One message of the wireless hydrometer."""

    sent_at_s: float
    gravity: float
    temperature_c: float
    battery_v: float
    rssi_dbm: float


@dataclass(frozen=True, slots=True)
class FieldInputs:
    """What the field tells the controller at one scan."""

    currents_ma: Mapping[str, float]  # one for each 4-20 mA transmitter
    valve_contacts: Mapping[str, ValveContacts]
    contactor_closed: bool  # the auxiliary contact of K1
    drive: DriveStatus
    hydrometer: HydrometerMessage | None  # the message that came in, if one did


@dataclass(slots=True)
class FieldOutputs:
    """What the controller commands. The two pulses last one scan."""

    pumps_on: dict[str, bool]
    valves_open: dict[str, bool]
    heaters_pct: dict[str, float]
    drive_run: bool = False
    drive_acknowledge: bool = False  # pulse: confirm the fault of the drive
    contactor_reset: bool = False  # pulse: close K1 again, if the thermostats let it
