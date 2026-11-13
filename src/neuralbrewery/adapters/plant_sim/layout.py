"""The nameplate of the plant: what is installed, its tag and its size.

Fixed data that the three layers share, as a real plant shares its
drawings. No true value and no state live here. docs/impianto.md has the
same numbers, with their sources.
"""

from dataclasses import dataclass

from neuralbrewery.core.plant.schemas import Route, Vessel


@dataclass(frozen=True)
class VesselPlate:
    capacity_l: float
    level: str  # tag of its level transmitter, ranged 0 to capacity
    probe: str  # tag of the probe its regulation reads
    heater: str
    heater_w: float
    heater_covered_l: float  # below this level the element is dry
    max_setpoint_c: float
    thermostat_c: float  # where the wired thermostat opens K1


VESSELS: dict[Vessel, VesselPlate] = {
    Vessel.HLT: VesselPlate(40.0, "LT1", "TT1", "R1", 3000.0, 8.0, 85.0, 90.0),
    Vessel.MASH: VesselPlate(30.0, "LT2", "TT2", "R2", 2000.0, 6.0, 80.0, 85.0),
    Vessel.BOIL: VesselPlate(40.0, "LT3", "TT3", "R3", 3500.0, 6.0, 100.0, 105.0),
    Vessel.FERM: VesselPlate(26.5, "LT4", "TT5a", "R4", 100.0, 4.0, 30.0, 35.0),
}

# The fermenter has a second probe: for comparison, and as a spare
BACKUP_PROBE = "TT5b"
PROBES: dict[str, Vessel] = {
    **{plate.probe: vessel for vessel, plate in VESSELS.items()},
    BACKUP_PROBE: Vessel.FERM,
}
LEVELS: dict[str, Vessel] = {plate.level: vessel for vessel, plate in VESSELS.items()}
HEATERS: dict[str, Vessel] = {plate.heater: vessel for vessel, plate in VESSELS.items()}

# Every temperature transmitter is ranged alike: 4 mA at 0 °C, 20 mA at 150 °C
TEMPERATURE_SPAN_C = (0.0, 150.0)


@dataclass(frozen=True)
class RoutePlate:
    source: Vessel
    destination: Vessel
    pump: str
    valves: tuple[str, ...]


ROUTES: dict[Route, RoutePlate] = {
    Route.HLT_TO_MASH: RoutePlate(Vessel.HLT, Vessel.MASH, "P1", ("EV2a",)),
    Route.HLT_TO_BOIL: RoutePlate(Vessel.HLT, Vessel.BOIL, "P1", ("EV2b",)),
    Route.MASH_RECIRC: RoutePlate(Vessel.MASH, Vessel.MASH, "P2", ("EV3", "EV5")),
    Route.MASH_TO_BOIL: RoutePlate(Vessel.MASH, Vessel.BOIL, "P2", ("EV3", "EV6")),
    Route.BOIL_TO_FERM: RoutePlate(Vessel.BOIL, Vessel.FERM, "P2", ("EV4", "EV7")),
}

PUMPS = ("P1", "P2")
PUMP_FLOW_L_PER_MIN = 10.0

GLYCOL_VALVE = "EV9"
VALVES = ("EV2a", "EV2b", "EV3", "EV4", "EV5", "EV6", "EV7", GLYCOL_VALVE)
GLYCOL_COOLING_W = 300.0
CHILLER = "CHILLER"  # a machine of its own: no tag on the drawing, no signal

AGITATOR = "M1"
AGITATOR_COVERED_L = 8.0  # below this level in the tun the blades are dry
CONTACTOR = "K1"
HYDROMETER = "DT1"
