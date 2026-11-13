"""The faults a test or an eval can inject: which, where, and what they break.

Each fault is one row of docs/impianto.md, "Guasti iniettabili". A fault
is put on a device or on the process, never on the controller: what the
controller comes to know of it is what the devices can tell.
"""

from neuralbrewery.adapters.plant_sim.devices.field import Field
from neuralbrewery.adapters.plant_sim.layout import (
    AGITATOR,
    CHILLER,
    HEATERS,
    HYDROMETER,
    LEVELS,
    PROBES,
    PUMPS,
    VALVES,
)
from neuralbrewery.adapters.plant_sim.process import Process
from neuralbrewery.core.exceptions import ValidationError
from neuralbrewery.core.plant.schemas import Fault, FaultKind, Vessel

# Where each fault can be
ADMITTED: dict[FaultKind, frozenset[str]] = {
    FaultKind.PROBE_BROKEN: frozenset(PROBES),
    FaultKind.PROBE_OFFSET: frozenset(PROBES),
    FaultKind.SIGNAL_CABLE_BROKEN: frozenset(PROBES) | frozenset(LEVELS),
    FaultKind.LEVEL_STUCK: frozenset(LEVELS),
    FaultKind.LEVEL_FOAM: frozenset(LEVELS),
    FaultKind.HYDROMETER_BATTERY_LOW: frozenset({HYDROMETER}),
    FaultKind.HYDROMETER_WIFI_LOST: frozenset({HYDROMETER}),
    FaultKind.PUMP_BLOCKED: frozenset(PUMPS),
    FaultKind.VALVE_STUCK: frozenset(VALVES),
    FaultKind.SSR_SHORTED: frozenset(HEATERS),
    FaultKind.HEATER_OPEN: frozenset(HEATERS),
    FaultKind.GLYCOL_FAILED: frozenset({CHILLER}),
    FaultKind.DRIVE_FAULT: frozenset({AGITATOR}),
    FaultKind.FERMENTATION_STUCK: frozenset({Vessel.FERM.value}),
}
# The faults that say how much: degrees off, the code of the drive
VALUE_NEEDED = frozenset({FaultKind.PROBE_OFFSET, FaultKind.DRIVE_FAULT})
# A level may be stuck at a given value, or where it is now
VALUE_ALLOWED = VALUE_NEEDED | {FaultKind.LEVEL_STUCK}


def check(fault: Fault) -> None:
    """Refuse a fault the plant cannot have.

    A fault that is accepted and does nothing would make a scenario run
    healthy, and look passed.
    """
    if fault.target not in ADMITTED[fault.kind]:
        raise ValidationError(
            f"{fault.kind} cannot be on {fault.target}: it can be on "
            f"{', '.join(sorted(ADMITTED[fault.kind]))}",
            field="target",
        )
    if fault.value is None and fault.kind in VALUE_NEEDED:
        raise ValidationError(f"{fault.kind} needs a value", field="value")
    if fault.value is not None and fault.kind not in VALUE_ALLOWED:
        raise ValidationError(f"{fault.kind} takes no value", field="value")


def apply(fault: Fault, field: Field, process: Process) -> None:
    """Put the fault on its device, or on the process."""
    check(fault)
    target = fault.target
    match fault.kind:
        case FaultKind.PROBE_BROKEN:
            field.transmitters[target].sensor_broken = True
        case FaultKind.PROBE_OFFSET:
            field.transmitters[target].offset = fault.value or 0.0
        case FaultKind.SIGNAL_CABLE_BROKEN:
            field.transmitters[target].cable_broken = True
        case FaultKind.LEVEL_STUCK:
            field.transmitters[target].stick(fault.value)
        case FaultKind.LEVEL_FOAM:
            field.transmitters[target].foam = True
        case FaultKind.HYDROMETER_BATTERY_LOW:
            field.hydrometer.battery_failing = True
        case FaultKind.HYDROMETER_WIFI_LOST:
            field.hydrometer.wifi_lost = True
        case FaultKind.PUMP_BLOCKED:
            field.pumps[target].blocked = True
        case FaultKind.VALVE_STUCK:
            field.valves[target].stuck = True
        case FaultKind.SSR_SHORTED:
            field.heaters[target].shorted = True
        case FaultKind.HEATER_OPEN:
            field.heaters[target].open_circuit = True
        case FaultKind.GLYCOL_FAILED:
            field.glycol_failed = True
        case FaultKind.DRIVE_FAULT:
            field.drive.cause = int(fault.value or 0)
        case _:  # FERMENTATION_STUCK, the only kind left
            process.fermentation.stuck = True


def clear(field: Field, process: Process) -> None:
    """Take every fault away. What it did to the plant in the meantime stays."""
    field.clear_faults()
    process.fermentation.stuck = False
