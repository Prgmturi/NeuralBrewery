"""The scan cycle of the controller, its commands and its interlocks.

Every scan the controller reads the signals of the field, decides, and
writes its outputs. A command changes what the brewer wants and the
controller decides again at once, on the signals of the last scan.

Two rules shape the code (docs/impianto.md, "Interlock"):

- A command is refused when an interlock would stop it right away.
- What the controller stops on its own stays stopped. The alarm is latched
  with it, and only the brewer re-arms: with reset, or with a new command
  on the same thing. The controller never starts again by itself.

So `_latched` is two things at once: the alarms that wait for the brewer,
and the list of what may not run.

The brew program (program.py) is a brewer made of code: it presses the same
buttons, so the same two rules answer it.
"""

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

from neuralbrewery.adapters.plant_sim.controller.history import History
from neuralbrewery.adapters.plant_sim.controller.journal import AlarmKey, Journal
from neuralbrewery.adapters.plant_sim.controller.measurements import (
    SPANS,
    UNITS,
    Measure,
    from_current,
    from_hydrometer,
)
from neuralbrewery.adapters.plant_sim.controller.program import Progress, Step
from neuralbrewery.adapters.plant_sim.controller.regulation import Loop
from neuralbrewery.adapters.plant_sim.layout import (
    AGITATOR,
    AGITATOR_COVERED_L,
    BACKUP_PROBE,
    CONTACTOR,
    GLYCOL_VALVE,
    HEATERS,
    HYDROMETER,
    PROGRAM,
    PUMPS,
    ROUTES,
    VALVES,
    VESSELS,
)
from neuralbrewery.adapters.plant_sim.signals import (
    FieldInputs,
    FieldOutputs,
    HydrometerMessage,
)
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    CommandCode,
    CommandResult,
    ContactorState,
    Devices,
    DriveState,
    Event,
    EventKind,
    HeaterState,
    HistorySample,
    PlantState,
    ProgramStatus,
    PumpState,
    Quality,
    Reading,
    Regulation,
    Route,
    Transfer,
    ValveState,
    Vessel,
)

VALVE_TRAVEL_MAX_S = 10.0
TRANSFER_MIN_SOURCE_L = 2.0  # below this the pump would run dry
NO_PROGRESS_AFTER_S = 60.0
# What a level probe cannot tell: its accuracy, about half a litre. Less than
# this is not a flow, and not a quantity still to move.
LEVEL_DOUBT_L = 0.5
HOT_SIDE = (Vessel.HLT, Vessel.MASH, Vessel.BOIL)
# The end of the text of a latched alarm: it waits for the brewer
LATCHED = "(bloccato: serve reset)"

_ACCEPTED = CommandResult(accepted=True, code=CommandCode.OK)


def _refused(code: CommandCode, reason: str) -> CommandResult:
    return CommandResult(accepted=False, code=code, reason=reason)


@dataclass
class _Transfer:
    route: Route
    requested_l: float | None  # None: a recirculation
    for_step: bool = False  # started by the program: its litres count for the step
    # The measured level of the source when the pump started. None while
    # the valves are still opening.
    start_level_l: float | None = None
    done_l: float = 0.0
    progress_l: float = 0.0  # the litres done when the level last moved
    progress_at_s: float = 0.0


class Controller:
    def __init__(
        self, inputs: FieldInputs, *, history_window_s: int, history_period_s: int
    ) -> None:
        """Start idle, with the signals of time zero."""
        self.outputs = FieldOutputs(
            pumps_on=dict.fromkeys(PUMPS, False),
            valves_open=dict.fromkeys(VALVES, False),
            heaters_pct=dict.fromkeys(HEATERS, 0.0),
        )
        self._loops = {vessel: Loop() for vessel in Vessel}
        self._agitator_wanted = False
        self._transfer: _Transfer | None = None
        self._latched: dict[AlarmKey, str] = {}
        self._valve_moved_at_s: dict[str, float] = {}
        self._rearm = False
        self._hydrometer: HydrometerMessage | None = None
        self._program = Progress()
        self._now_s = 0.0
        self._journal = Journal()
        self._history = History(history_window_s, history_period_s)
        self.scan(inputs, 0.0)

    # ------------------------------------------------------------------
    # The scan cycle
    # ------------------------------------------------------------------

    def scan(self, inputs: FieldInputs, now_s: float) -> None:
        """One cycle: read the signals, decide, write the outputs."""
        passed_s = now_s - self._now_s
        self._now_s = now_s
        self._inputs = inputs
        # The field has taken the pulses of the cycle before
        self.outputs.drive_acknowledge = self.outputs.contactor_reset = False

        self._hydrometer = inputs.hydrometer or self._hydrometer
        self._measures: dict[str, Measure] = {
            tag: from_current(current_ma, SPANS[tag], now_s)
            for tag, current_ma in inputs.currents_ma.items()
        }
        self._measures.update(from_hydrometer(self._hydrometer, now_s))

        if self._rearm:
            # One scan after reset, so the field has had the time to answer.
            # Whatever still has its cause trips again in _decide, just below.
            self._rearm = False
            self._latched.clear()
        self._run_program(passed_s)
        self._decide()
        self._history.record(
            now_s,
            readings={tag: measure.value for tag, measure in self._measures.items()},
            commands={
                **self.outputs.heaters_pct,
                **{tag: 100.0 * on for tag, on in self.outputs.pumps_on.items()},
                GLYCOL_VALVE: 100.0 * self.outputs.valves_open[GLYCOL_VALVE],
            },
        )

    def _decide(self) -> None:
        """From what is wanted and what is measured to the outputs and the alarms."""
        self._watch_valves()
        self._run_transfer()
        self._run_agitator()
        for vessel in Vessel:
            self._regulate(vessel)
        # A latched alarm says so, as a panel shows it: its cause may be gone
        # (a probe that reads again), the block is not
        latched = {key: f"{text} {LATCHED}" for key, text in self._latched.items()}
        self._journal.update(
            self._now_s, {**self._facts(), **self._program.alarms(), **latched}
        )

    def _facts(self) -> dict[AlarmKey, str]:
        """The alarms that only report: each lasts as long as its cause."""
        facts: dict[AlarmKey, str] = {
            (AlarmCode.SIGNAL_FAULT, tag): measure.reason
            for tag, measure in self._measures.items()
            if measure.quality is Quality.BAD
        }
        silent = self._measures[HYDROMETER]
        if self._hydrometer is not None and silent.quality is Quality.STALE:
            facts[(AlarmCode.HYDROMETER_SILENT, HYDROMETER)] = silent.reason
        fault_code = self._inputs.drive.fault_code
        if fault_code is not None:
            facts[(AlarmCode.DRIVE_FAULT, AGITATOR)] = (
                f"inverter in guasto: F{fault_code}"
            )
        if not self._inputs.contactor_closed:
            facts[(AlarmCode.SAFETY_OPEN, CONTACTOR)] = (
                f"{CONTACTOR} aperto: resistenze senza corrente"
            )
        return facts

    def _latch(self, code: AlarmCode, tag: str, text: str) -> None:
        """Stop something until the brewer re-arms. The first reason is kept."""
        self._latched.setdefault((code, tag), text)

    def _forget(self, *codes: AlarmCode) -> None:
        """Re-arm these alarms: those that still have their cause trip again."""
        for key in [key for key in self._latched if key[0] in codes]:
            del self._latched[key]

    # ------------------------------------------------------------------
    # Valves and transfers
    # ------------------------------------------------------------------

    def _set_valve(self, tag: str, open_: bool) -> None:
        if self.outputs.valves_open[tag] != open_:
            self.outputs.valves_open[tag] = open_
            self._valve_moved_at_s[tag] = self._now_s

    def _watch_valves(self) -> None:
        """Interlock 7: a valve whose end contacts disagree with its command."""
        for tag, contacts in self._inputs.valve_contacts.items():
            wanted = self.outputs.valves_open[tag]
            if contacts.open == wanted and contacts.closed != wanted:
                self._valve_moved_at_s.pop(tag, None)
                continue
            waiting_s = self._now_s - self._valve_moved_at_s.setdefault(
                tag, self._now_s
            )
            if waiting_s >= VALVE_TRAVEL_MAX_S:
                position = "aperta" if wanted else "chiusa"
                self._latch(
                    AlarmCode.VALVE_NOT_REACHED,
                    tag,
                    f"{tag} comandata {position}: il fine corsa non arriva",
                )

    def _run_transfer(self) -> None:
        """Open the valves, start the pump, count the litres, stop."""
        transfer = self._transfer
        if transfer is None:
            return
        plate = ROUTES[transfer.route]
        source = self._level(plate.source)
        destination = self._level(plate.destination)
        recirculation = plate.source is plate.destination

        if any(
            (AlarmCode.VALVE_NOT_REACHED, valve) in self._latched
            for valve in plate.valves
        ):
            self._end_transfer(transfer)  # the alarm of the valve says why
        elif source is None or destination is None:
            self._stop_transfer(transfer, "livello non valido")  # interlock 9
        elif source < TRANSFER_MIN_SOURCE_L:  # interlock 4
            self._stop_transfer(
                transfer, f"{plate.source} sotto {TRANSFER_MIN_SOURCE_L:g} L"
            )
        elif not recirculation and destination >= VESSELS[plate.destination].capacity_l:
            self._stop_transfer(transfer, f"{plate.destination} è pieno")
        elif transfer.start_level_l is None:
            if all(self._inputs.valve_contacts[valve].open for valve in plate.valves):
                transfer.start_level_l = source
                transfer.progress_at_s = self._now_s
                self.outputs.pumps_on[plate.pump] = True
        elif transfer.requested_l is not None:
            self._count(transfer, transfer.start_level_l - source, transfer.requested_l)

    def _count(self, transfer: _Transfer, done_l: float, requested_l: float) -> None:
        """Litres are counted on the level of the source: there is no flow meter.

        So the count is as good as the level probe. A transfer that stops
        moving within that doubt of its quantity is done, not in alarm: the
        tun gives its last litre when it gives it.
        """
        route, plate = transfer.route.value, ROUTES[transfer.route]
        transfer.done_l = max(transfer.done_l, done_l)
        if transfer.done_l >= transfer.progress_l + LEVEL_DOUBT_L:
            transfer.progress_l = transfer.done_l
            transfer.progress_at_s = self._now_s
        still = self._now_s - transfer.progress_at_s >= NO_PROGRESS_AFTER_S
        missing_l = requested_l - transfer.done_l

        if missing_l <= 0 or (still and missing_l < LEVEL_DOUBT_L):
            self._journal.record(
                self._now_s,
                EventKind.TRANSFER_DONE,
                "transfer_done",
                route,
                f"travaso completato: {transfer.done_l:.1f} L",
            )
            self._end_transfer(transfer)
        elif still:  # interlock 6
            self._latch(
                AlarmCode.TRANSFER_NO_PROGRESS,
                route,
                f"{plate.pump} comandata, livello di {plate.source} fermo da "
                f"{NO_PROGRESS_AFTER_S:g} s: travaso fermato a {transfer.done_l:.1f} L",
            )
            self._end_transfer(transfer)

    def _stop_transfer(self, transfer: _Transfer, reason: str) -> None:
        self._latch(
            AlarmCode.TRANSFER_STOPPED,
            transfer.route.value,
            f"travaso fermato: {reason}",
        )
        self._end_transfer(transfer)

    def _end_transfer(self, transfer: _Transfer) -> None:
        plate = ROUTES[transfer.route]
        self.outputs.pumps_on[plate.pump] = False
        for valve in plate.valves:
            self._set_valve(valve, False)
        self._transfer = None
        if transfer.for_step:
            self._program.moved_l += transfer.done_l

    # ------------------------------------------------------------------
    # Agitator and temperature
    # ------------------------------------------------------------------

    def _level(self, vessel: Vessel) -> float | None:
        return self._measures[VESSELS[vessel].level].value

    def _covered(
        self, vessel: Vessel, minimum_l: float, what: str
    ) -> CommandResult | None:
        """Interlocks 1, 3 and 9: no level, or too little, to switch that on."""
        tag = VESSELS[vessel].level
        level = self._level(vessel)
        if level is None:
            return _refused(
                CommandCode.LEVEL_UNKNOWN,
                f"livello {tag} non valido: serve per accendere {what}",
            )
        if level < minimum_l:
            return _refused(
                CommandCode.LEVEL_LOW,
                f"livello {tag} sotto {minimum_l:g} L, il minimo per accendere {what}",
            )
        return None

    def _agitator_block(self) -> CommandResult | None:
        return self._covered(Vessel.MASH, AGITATOR_COVERED_L, AGITATOR)

    def _heater_block(self, vessel: Vessel) -> CommandResult | None:
        plate = VESSELS[vessel]
        block = self._covered(vessel, plate.heater_covered_l, plate.heater)
        if block is None and vessel is Vessel.MASH and not self._wort_moves():
            return _refused(  # interlock 2
                CommandCode.WORT_NOT_MOVING,
                "mosto fermo nel tino: serve l'agitatore o il ricircolo",
            )
        return block

    def _wort_moves(self) -> bool:
        """Interlock 2 goes by what is commanded, for the agitator as for the pump.

        The run signal of the drive comes a scan after the command: going by
        it, "agitator on" and then "heat the tun" would be refused. A drive
        that cannot run says so with its fault code.
        """
        transfer = self._transfer
        recirculating = transfer is not None and transfer.route is Route.MASH_RECIRC
        agitating = (
            self._agitator_wanted
            and (AlarmCode.AGITATOR_BLOCKED, AGITATOR) not in self._latched
            and self._inputs.drive.fault_code is None
        )
        return agitating or recirculating

    def _run_agitator(self) -> None:
        blocked = (AlarmCode.AGITATOR_BLOCKED, AGITATOR)
        if self._agitator_wanted:
            block = self._agitator_block()
            if block is not None:
                self._latch(*blocked, block.reason)
        self.outputs.drive_run = self._agitator_wanted and blocked not in self._latched

    def _probe_block(self, vessel: Vessel) -> CommandResult | None:
        """No probe to regulate with: its own or, in the fermenter, the spare."""
        probe = VESSELS[vessel].probe
        spare = vessel is Vessel.FERM and self._measures[BACKUP_PROBE].value is not None
        if self._measures[probe].value is None and not spare:
            return _refused(
                CommandCode.PROBE_FAULT, f"sonda {probe} non valida: non posso regolare"
            )
        return None

    def _on_spare_probe(self, vessel: Vessel) -> bool:
        probe_failed = (AlarmCode.CONTROL_PROBE_FAULT, vessel.value) in self._latched
        return probe_failed and vessel is Vessel.FERM

    def _control_temperature(self, vessel: Vessel) -> float | None:
        """What regulation follows; None while it is suspended."""
        if (AlarmCode.CONTROL_PROBE_FAULT, vessel.value) not in self._latched:
            return self._measures[VESSELS[vessel].probe].value
        if self._on_spare_probe(vessel):
            return self._measures[BACKUP_PROBE].value
        return None

    def _regulate(self, vessel: Vessel) -> None:
        plate, loop = VESSELS[vessel], self._loops[vessel]
        blocked = (AlarmCode.HEATER_BLOCKED, plate.heater)
        if loop.setpoint_c is not None:
            if self._measures[plate.probe].value is None:
                then = (
                    f"regolazione su {BACKUP_PROBE}"
                    if vessel is Vessel.FERM
                    else "regolazione sospesa"
                )
                self._latch(
                    AlarmCode.CONTROL_PROBE_FAULT,
                    vessel.value,
                    f"sonda {plate.probe} non valida: {then}",
                )
            block = self._heater_block(vessel)
            if block is not None:
                self._latch(*blocked, block.reason)

        loop.follow(self._control_temperature(vessel))
        heating = blocked not in self._latched
        self.outputs.heaters_pct[plate.heater] = loop.heater_pct if heating else 0.0
        if vessel is Vessel.FERM:
            self._set_valve(GLYCOL_VALVE, loop.cooling)

    def _want_setpoint(self, vessel: Vessel, celsius: float | None) -> None:
        """A new setpoint is the brewer taking charge: the vessel is re-armed."""
        self._loops[vessel].setpoint_c = celsius
        self._latched.pop((AlarmCode.HEATER_BLOCKED, VESSELS[vessel].heater), None)
        self._latched.pop((AlarmCode.CONTROL_PROBE_FAULT, vessel.value), None)

    def _want_agitator(self, on: bool) -> None:
        self._agitator_wanted = on
        self._latched.pop((AlarmCode.AGITATOR_BLOCKED, AGITATOR), None)

    # ------------------------------------------------------------------
    # The buttons: what each does, whoever presses it
    # ------------------------------------------------------------------

    def _done(self, command: str, tag: str, text: str) -> CommandResult:
        """An accepted command is an event."""
        self._journal.record(self._now_s, EventKind.COMMAND, command, tag, text)
        return _ACCEPTED

    def _activate_route(
        self, route: Route, liters: float | None, *, for_step: bool = False
    ) -> CommandResult:
        plate = ROUTES[route]
        recirculation = plate.source is plate.destination
        if self._transfer is not None:  # interlock 5
            return _refused(
                CommandCode.ROUTE_BUSY,
                f"{self._transfer.route} è in corso: un percorso alla volta",
            )
        if recirculation != (liters is None) or (liters is not None and liters <= 0):
            return _refused(
                CommandCode.INVALID_QUANTITY,
                "un travaso chiede più di zero litri; il ricircolo non ne chiede",
            )
        source = self._level(plate.source)
        destination = self._level(plate.destination)
        if source is None or destination is None:  # interlock 9
            return _refused(
                CommandCode.LEVEL_UNKNOWN,
                f"livello di {plate.source} o di {plate.destination} non valido",
            )
        if source < TRANSFER_MIN_SOURCE_L:  # interlock 4
            return _refused(
                CommandCode.SOURCE_LOW,
                f"{plate.source} sotto {TRANSFER_MIN_SOURCE_L:g} L: la pompa "
                "girerebbe a secco",
            )
        room_l = VESSELS[plate.destination].capacity_l - destination
        if liters is not None and liters > room_l:
            return _refused(
                CommandCode.NO_ROOM,
                f"{liters:g} L non entrano in {plate.destination}: "
                f"restano {room_l:.1f} L",
            )

        # A new transfer takes the place of the one that ended badly
        self._forget(
            AlarmCode.VALVE_NOT_REACHED,
            AlarmCode.TRANSFER_NO_PROGRESS,
            AlarmCode.TRANSFER_STOPPED,
        )
        self._transfer = _Transfer(route, liters, for_step=for_step)
        for valve in plate.valves:
            self._set_valve(valve, True)
        quantity = "ricircolo" if liters is None else f"{liters:g} L"
        return self._done("activate_route", route.value, quantity)

    def _stop_route(self) -> CommandResult:
        transfer = self._transfer
        if transfer is None:
            return self._done("stop_route", "", "nessun travaso in corso")
        self._end_transfer(transfer)
        return self._done(
            "stop_route", transfer.route.value, f"fermato a {transfer.done_l:.1f} L"
        )

    def _set_temperature(self, vessel: Vessel, celsius: float | None) -> CommandResult:
        plate = VESSELS[vessel]
        if celsius is None:
            self._want_setpoint(vessel, None)
            return self._done("set_temperature", vessel.value, "spento")
        if not 0.0 <= celsius <= plate.max_setpoint_c:  # interlock 8
            return _refused(
                CommandCode.SETPOINT_OUT_OF_RANGE,
                f"{celsius:g} °C fuori dai limiti di {vessel}: "
                f"da 0 a {plate.max_setpoint_c:g} °C",
            )
        block = self._probe_block(vessel) or self._heater_block(vessel)
        if block is not None:
            return block
        self._want_setpoint(vessel, celsius)
        return self._done("set_temperature", vessel.value, f"{celsius:g} °C")

    def _set_agitator(self, on: bool) -> CommandResult:
        if on:
            if self._inputs.drive.fault_code is not None:
                return _refused(
                    CommandCode.DRIVE_FAULT, "inverter in guasto: serve prima reset"
                )
            block = self._agitator_block()
            if block is not None:
                return block
        self._want_agitator(on)
        return self._done("set_agitator", AGITATOR, "acceso" if on else "spento")

    def _stop_hot_side(self) -> None:
        """A fermentation goes on for days: the fermenter is left alone."""
        if self._transfer is not None:
            self._end_transfer(self._transfer)
        for vessel in HOT_SIDE:
            self._want_setpoint(vessel, None)
        self._want_agitator(False)

    # ------------------------------------------------------------------
    # The brew program (the recipe is in program.py)
    # ------------------------------------------------------------------

    def _run_program(self, passed_s: float) -> None:
        """Once a scan: see what stops the step, give its commands, see it end.

        Anything blocked, or a command refused, pauses the program with the
        reason. Going on after that is for the brewer to say.
        """
        program = self._program
        if not program.running:
            return
        block = self._program_block()
        if block is not None:
            self._pause_program(block, by_alarm=True)
        elif not program.given:
            refusal = self._give(program.step)
            if refusal is None:
                program.given = True
            else:
                self._pause_program(refusal.reason, by_alarm=True)
        else:
            program.elapsed_s += passed_s
            if self._step_done(program.step):
                self._next_step()

    def _program_block(self) -> str | None:
        """Why the program may not go on: the text of the alarm that says so.

        K1 open, the drive in fault, or anything an interlock has stopped.
        """
        facts = self._facts()
        stops = (
            facts.get((AlarmCode.SAFETY_OPEN, CONTACTOR)),
            facts.get((AlarmCode.DRIVE_FAULT, AGITATOR)),
            *self._latched.values(),
        )
        return next((text for text in stops if text is not None), None)

    def _give(self, step: Step) -> CommandResult | None:
        """Bring the plant to what the step wants; return the first refusal.

        Only the commands that are missing: one already in place is not
        given again, so the program never re-arms what an interlock stopped.
        The order is one no interlock objects to: first the setpoints to
        take away, then the route, the agitator, and the setpoints to set.
        """
        for vessel in HOT_SIDE:
            off = vessel not in step.setpoints
            if off and self._loops[vessel].setpoint_c is not None:
                self._set_temperature(vessel, None)
        if self._transfer is not None:
            self._stop_route()

        orders: list[Callable[[], CommandResult]] = []
        # After a pause, only the litres still to move. None of them, when
        # the pause came in the very scan the transfer ended.
        moved_l = self._program.moved_l
        liters = None if step.liters is None else step.liters - moved_l
        if step.route is not None and (liters is None or liters > 0):
            orders.append(
                partial(self._activate_route, step.route, liters, for_step=True)
            )
        if self._agitator_wanted != step.agitator:
            orders.append(partial(self._set_agitator, step.agitator))
        orders += [
            partial(self._set_temperature, vessel, celsius)
            for vessel, celsius in step.setpoints.items()
            if self._loops[vessel].setpoint_c != celsius
        ]
        for order in orders:
            result = order()
            if not result.accepted:
                return result
        return None

    def _step_done(self, step: Step) -> bool:
        if step.liters is not None:
            # A transfer that ends in any other way leaves a block behind
            return self._transfer is None
        if step.reach is not None:
            vessel, celsius = step.reach
            temp_c = self._control_temperature(vessel)
            return temp_c is not None and temp_c >= celsius
        return step.lasts_s is not None and self._program.elapsed_s >= step.lasts_s

    def _next_step(self) -> None:
        program = self._program
        program.advance()
        if program.status is ProgramStatus.DONE:
            self._journal.record(
                self._now_s,
                EventKind.PROGRAM_DONE,
                "program_done",
                PROGRAM,
                "programma finito",
            )
        else:
            self._log_step()

    def _log_step(self) -> None:
        self._journal.record(
            self._now_s,
            EventKind.PROGRAM_STEP,
            "program_step",
            PROGRAM,
            self._program.label,
        )

    def _pause_program(self, reason: str, *, by_alarm: bool) -> None:
        """Hold the step: setpoints and recirculation stay, to keep the tun warm.

        A transfer with a quantity stops, and its litres stay counted.
        """
        transfer = self._transfer
        if transfer is not None and transfer.requested_l is not None:
            self._end_transfer(transfer)
        self._program.pause(reason, by_alarm=by_alarm)

    def _blocked_program(self) -> CommandResult | None:
        """Starting or resuming into a block is refused: reset comes first.

        Right after reset the controller cannot know yet what will hold.
        The program is let go, and pauses again if something still does.
        """
        block = None if self._rearm else self._program_block()
        if block is None:
            return None
        return _refused(CommandCode.ALARM_ACTIVE, f"serve prima reset: {block}")

    # ------------------------------------------------------------------
    # Commands: the panel of the brewer
    # ------------------------------------------------------------------

    def _decided(self, result: CommandResult) -> CommandResult:
        """After an accepted command the controller decides again at once."""
        if result.accepted:
            self._decide()
        return result

    def _manual(self, *, stops: bool) -> CommandResult | None:
        """A manual command on the hot side while the program runs.

        One that stops something is obeyed, and the program pauses: a stop
        is never refused. One that starts something is refused: the hot
        side is the program's until it is paused.
        """
        if not self._program.running:
            return None
        if stops:
            self._pause_program("fermato con un comando manuale", by_alarm=False)
            return None
        return _refused(
            CommandCode.PROGRAM_RUNNING,
            "il programma è in corso: va messo in pausa per comandare a mano",
        )

    def activate_route(self, route: Route, liters: float | None) -> CommandResult:
        return self._decided(
            self._manual(stops=False) or self._activate_route(route, liters)
        )

    def stop_route(self) -> CommandResult:
        return self._decided(self._manual(stops=True) or self._stop_route())

    def set_temperature(self, vessel: Vessel, celsius: float | None) -> CommandResult:
        taken = self._manual(stops=celsius is None) if vessel in HOT_SIDE else None
        return self._decided(taken or self._set_temperature(vessel, celsius))

    def set_agitator(self, on: bool) -> CommandResult:
        return self._decided(self._manual(stops=not on) or self._set_agitator(on))

    def stop_all(self) -> CommandResult:
        """Stop the hot side; the program, if it runs, pauses."""
        self._manual(stops=True)
        self._stop_hot_side()
        return self._decided(self._done("stop_all", "", "lato caldo fermo"))

    def reset(self) -> CommandResult:
        """Re-arm. Always accepted: the controller sends the pulses and sees after.

        It cannot know whether K1 will close: that is for the thermostats.
        """
        self.outputs.drive_acknowledge = self.outputs.contactor_reset = True
        self._rearm = True
        return self._decided(self._done("reset", "", "riarmo"))

    def start_program(self) -> CommandResult:
        """Open the program at its first step. Its commands come with the next scan."""
        program = self._program
        if program.open:
            return _refused(
                CommandCode.PROGRAM_STATE,
                f"c'è già un programma aperto, al {program.label}",
            )
        refusal = self._blocked_program()
        if refusal is not None:
            return refusal
        result = self._done("start_program", PROGRAM, "cotta di riferimento")
        program.start()
        self._log_step()
        return self._decided(result)

    def confirm_step(self) -> CommandResult:
        program = self._program
        if not program.waiting:
            return _refused(
                CommandCode.PROGRAM_STATE, "nessun passo aspetta una conferma"
            )
        result = self._done("confirm_step", PROGRAM, program.label)
        self._next_step()
        return self._decided(result)

    def pause_program(self) -> CommandResult:
        """Always accepted, as every command that stops."""
        program = self._program
        if program.running:
            self._pause_program("pausa chiesta dal birraio", by_alarm=False)
        state = program.label if program.open else "nessun programma aperto"
        return self._decided(self._done("pause_program", PROGRAM, state))

    def resume_program(self) -> CommandResult:
        program = self._program
        if program.status is not ProgramStatus.PAUSED:
            return _refused(CommandCode.PROGRAM_STATE, "il programma non è in pausa")
        refusal = self._blocked_program()
        if refusal is not None:
            return refusal
        program.resume()
        return self._decided(self._done("resume_program", PROGRAM, program.label))

    def abort_program(self) -> CommandResult:
        """Close the program and stop the hot side. Always accepted."""
        self._program.abort()
        self._stop_hot_side()
        return self._decided(self._done("abort_program", PROGRAM, "lato caldo fermo"))

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def snapshot(self) -> PlantState:
        outputs, inputs, transfer = self.outputs, self._inputs, self._transfer
        return PlantState(
            sim_time_s=self._now_s,
            readings={
                tag: Reading(
                    tag=tag,
                    value=measure.value,
                    unit=UNITS[tag],
                    quality=measure.quality,
                    reason=measure.reason,
                    current_ma=measure.current_ma,
                    sim_time_s=measure.at_s,
                )
                for tag, measure in self._measures.items()
            },
            devices=Devices(
                pumps={
                    tag: PumpState(commanded_on=on)
                    for tag, on in outputs.pumps_on.items()
                },
                valves={
                    tag: ValveState(
                        commanded_open=outputs.valves_open[tag],
                        open_contact=contacts.open,
                        closed_contact=contacts.closed,
                    )
                    for tag, contacts in inputs.valve_contacts.items()
                },
                heaters={
                    tag: HeaterState(commanded_pct=pct)
                    for tag, pct in outputs.heaters_pct.items()
                },
                safety_contactor=ContactorState(closed=inputs.contactor_closed),
                agitator=DriveState(
                    commanded_run=outputs.drive_run,
                    running=inputs.drive.running,
                    frequency_hz=inputs.drive.frequency_hz,
                    current_a=inputs.drive.current_a,
                    fault_code=inputs.drive.fault_code,
                ),
            ),
            regulation={
                vessel: Regulation(
                    setpoint_c=loop.setpoint_c,
                    probe=(
                        BACKUP_PROBE
                        if self._on_spare_probe(vessel)
                        else VESSELS[vessel].probe
                    ),
                )
                for vessel, loop in self._loops.items()
            },
            transfer=(
                None
                if transfer is None
                else Transfer(
                    route=transfer.route,
                    requested_l=transfer.requested_l,
                    done_l=round(transfer.done_l, 1),
                )
            ),
            program=self._program.view(),
            alarms=self._journal.alarms,
        )

    def events(self, since_s: float) -> list[Event]:
        return self._journal.events(since_s)

    def history(self, tag: str, since_s: float) -> list[HistorySample]:
        return self._history.since(tag, since_s)
