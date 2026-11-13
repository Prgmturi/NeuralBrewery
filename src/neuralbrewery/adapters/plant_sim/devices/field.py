"""The field: every device of the plant, wired as on the drawing.

Two moves for each calculation step. actuate() takes the outputs of the
controller to the devices and says what they do to the process. measure()
reads the process and gives the controller its signals.
"""

from neuralbrewery.adapters.plant_sim.devices.actuators import (
    Drive,
    Heater,
    Pump,
    Valve,
)
from neuralbrewery.adapters.plant_sim.devices.safety import SafetyChain
from neuralbrewery.adapters.plant_sim.devices.sensors import (
    Hydrometer,
    Transmitter,
    class_a_tolerance_c,
    level_tolerance_l,
)
from neuralbrewery.adapters.plant_sim.layout import (
    GLYCOL_COOLING_W,
    GLYCOL_VALVE,
    LEVELS,
    PROBES,
    PUMP_FLOW_L_PER_MIN,
    PUMPS,
    ROUTES,
    TEMPERATURE_SPAN_C,
    VALVES,
    VESSELS,
)
from neuralbrewery.adapters.plant_sim.process import Flow, Process
from neuralbrewery.adapters.plant_sim.signals import FieldInputs, FieldOutputs
from neuralbrewery.core.plant.schemas import Vessel

TEMPERATURE_NOISE_SD_C = 0.02
LEVEL_NOISE_SD_L = 0.05


class Field:
    def __init__(self, seed: int, hydrometer_on: bool) -> None:
        self.transmitters: dict[str, Transmitter] = {
            tag: Transmitter(
                tag,
                TEMPERATURE_SPAN_C,
                class_a_tolerance_c,
                TEMPERATURE_NOISE_SD_C,
                seed,
            )
            for tag in PROBES
        }
        for plate in VESSELS.values():
            self.transmitters[plate.level] = Transmitter(
                plate.level,
                (0.0, plate.capacity_l),
                level_tolerance_l,
                LEVEL_NOISE_SD_L,
                seed,
            )
        self.hydrometer = Hydrometer(seed, on=hydrometer_on)
        self.pumps = {tag: Pump() for tag in PUMPS}
        self.valves = {tag: Valve() for tag in VALVES}
        self.heaters = {
            plate.heater: Heater(plate.heater_w) for plate in VESSELS.values()
        }
        self.drive = Drive()
        self.safety = SafetyChain()
        self.glycol_failed = False  # fault: the chiller sends no cold glycol

    def clear_faults(self) -> None:
        """Every device healthy again. A drive in fault still waits its reset."""
        for transmitter in self.transmitters.values():
            transmitter.clear_faults()
        self.hydrometer.clear_faults()
        for pump in self.pumps.values():
            pump.blocked = False
        for valve in self.valves.values():
            valve.stuck = False
        for heater in self.heaters.values():
            heater.shorted = heater.open_circuit = False
        self.drive.cause = None
        self.glycol_failed = False

    def actuate(
        self, outputs: FieldOutputs, process: Process
    ) -> tuple[dict[Vessel, float], list[Flow]]:
        """Obey the controller; returns the power into each vessel, and the flows."""
        for tag, pump in self.pumps.items():
            pump.on = outputs.pumps_on[tag]
        for tag, valve in self.valves.items():
            valve.command(outputs.valves_open[tag])
        self.drive.command(outputs.drive_run, outputs.drive_acknowledge)
        # The thermostats feel the vessels themselves: the true temperatures
        self.safety.check(
            {vessel: content.temp_c for vessel, content in process.vessels.items()},
            outputs.contactor_reset,
        )

        heat_w = {
            vessel: self.heaters[plate.heater].power_w(
                outputs.heaters_pct[plate.heater], powered=self.safety.closed
            )
            for vessel, plate in VESSELS.items()
        }
        if self.valves[GLYCOL_VALVE].open and not self.glycol_failed:
            heat_w[Vessel.FERM] -= GLYCOL_COOLING_W
        return heat_w, self._flows()

    def _flows(self) -> list[Flow]:
        """Where liquid moves: along each route whose pump runs and valves are open.

        One route in normal work. A valve stuck open may open a second way
        for the same pump, which then shares its flow between the two.
        """
        flows = []
        for tag, pump in self.pumps.items():
            ways = [
                plate
                for plate in ROUTES.values()
                if plate.pump == tag
                and pump.pumping
                and all(self.valves[valve].open for valve in plate.valves)
            ]
            flows += [
                Flow(way.source, way.destination, PUMP_FLOW_L_PER_MIN / 60 / len(ways))
                for way in ways
            ]
        return flows

    def measure(self, process: Process, now_s: float) -> FieldInputs:
        """One measure from every instrument, and the state of every contact."""
        currents = {
            tag: self.transmitters[tag].current_ma(process.vessels[vessel].temp_c)
            for tag, vessel in PROBES.items()
        }
        for tag, vessel in LEVELS.items():
            # A level probe sees the surface: in the tun, liquid and grain
            currents[tag] = self.transmitters[tag].current_ma(
                process.vessels[vessel].filled_l
            )
        return FieldInputs(
            currents_ma=currents,
            valve_contacts={tag: valve.contacts for tag, valve in self.valves.items()},
            contactor_closed=self.safety.closed,
            drive=self.drive.status,
            hydrometer=self.hydrometer.message(
                now_s,
                process.fermentation.gravity,
                process.vessels[Vessel.FERM].temp_c,
            ),
        )
