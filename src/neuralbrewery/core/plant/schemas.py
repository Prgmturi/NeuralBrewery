"""The vocabulary of the plant: what its controller tells, and what it is told.

Agents, the watcher and the executor speak only these words, whatever
adapter is underneath: nothing here says HTTP, MQTT or OPC UA. A reading
has the shape of an OPC UA value (value, quality, time), so a real
controller would need a new adapter, not a new vocabulary.

A tag is the short name on the drawing of the plant: "TT1", "EV9", "R2".
The list is in docs/impianto.md. Texts meant for the brewer (reasons,
alarm texts) are in Italian, as the brewer is.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# The plant
# ---------------------------------------------------------------------------


class Vessel(StrEnum):
    HLT = "HLT"  # hot liquor tank: the hot water
    MASH = "MASH"  # mash tun
    BOIL = "BOIL"  # kettle
    FERM = "FERM"  # fermenter


class Route(StrEnum):
    """The only ways liquid may move. No free combination of valves."""

    HLT_TO_MASH = "hlt_to_mash"
    HLT_TO_BOIL = "hlt_to_boil"
    MASH_RECIRC = "mash_recirc"
    MASH_TO_BOIL = "mash_to_boil"
    BOIL_TO_FERM = "boil_to_ferm"


# ---------------------------------------------------------------------------
# What the controller tells
# ---------------------------------------------------------------------------


class Quality(StrEnum):
    GOOD = "good"
    BAD = "bad"  # the instrument or its signal is faulty: there is no value
    STALE = "stale"  # no news for too long: the value is the last one received


class Reading(_Frozen):
    """One measure, as the controller has it."""

    tag: str
    value: float | None  # None when there is nothing to trust
    unit: str
    quality: Quality
    reason: str = ""  # why the quality is not good
    current_ma: float | None = None  # the signal itself, for a 4-20 mA instrument
    sim_time_s: float  # simulated time of the measure: how fresh it is


class PumpState(_Frozen):
    commanded_on: bool  # a pump gives nothing back


class ValveState(_Frozen):
    """Command and end contacts: a valve is faulty when they disagree."""

    commanded_open: bool
    open_contact: bool
    closed_contact: bool


class HeaterState(_Frozen):
    commanded_pct: float  # a heater gives nothing back


class ContactorState(_Frozen):
    closed: bool  # nobody commands K1: the thermostats open it


class DriveState(_Frozen):
    """The agitator: what its drive is told, and what the drive answers."""

    commanded_run: bool
    running: bool
    frequency_hz: float
    current_a: float
    fault_code: int | None  # 11 is F11 in the manual of the drive


class Devices(_Frozen):
    """Every actuator by tag: the command and, where one exists, the feedback.

    Never the real effect: a heater with a broken element stays "commanded
    at 100 %", and the fault shows only in the temperature.
    """

    pumps: dict[str, PumpState]
    valves: dict[str, ValveState]
    heaters: dict[str, HeaterState]
    safety_contactor: ContactorState  # K1
    agitator: DriveState  # M1


class Regulation(_Frozen):
    setpoint_c: float | None  # None: off
    probe: str  # the probe regulation reads now


class Transfer(_Frozen):
    route: Route
    requested_l: float | None  # None: a recirculation, which runs until stopped
    done_l: float  # counted on the measured level of the source


class AlarmCode(StrEnum):
    # These report a fact and end with it
    SIGNAL_FAULT = "signal_fault"
    HYDROMETER_SILENT = "hydrometer_silent"
    DRIVE_FAULT = "drive_fault"
    SAFETY_OPEN = "safety_open"
    # These come with something the controller stopped: they stay until the
    # brewer re-arms, with reset or with a new command on the same thing
    CONTROL_PROBE_FAULT = "control_probe_fault"
    HEATER_BLOCKED = "heater_blocked"
    AGITATOR_BLOCKED = "agitator_blocked"
    VALVE_NOT_REACHED = "valve_not_reached"
    TRANSFER_NO_PROGRESS = "transfer_no_progress"
    TRANSFER_STOPPED = "transfer_stopped"


class Alarm(_Frozen):
    code: AlarmCode
    tag: str  # an instrument, an actuator, a vessel or a route
    text: str
    since_s: float


class EventKind(StrEnum):
    ALARM_RAISED = "alarm_raised"
    ALARM_CLEARED = "alarm_cleared"
    COMMAND = "command"  # accepted ones only
    TRANSFER_DONE = "transfer_done"


class Event(_Frozen):
    seq: int  # grows by one: two events of the same instant stay in order
    sim_time_s: float
    kind: EventKind
    code: str  # the alarm code, or the name of the command
    tag: str
    text: str


class HistorySample(_Frozen):
    """A reading as it was, or the mean of a command since the sample before."""

    sim_time_s: float
    value: float | None


class PlantState(_Frozen):
    """What the controller knows at one instant. Not what is true."""

    sim_time_s: float
    readings: dict[str, Reading]
    devices: Devices
    regulation: dict[Vessel, Regulation]
    transfer: Transfer | None
    alarms: tuple[Alarm, ...]


# ---------------------------------------------------------------------------
# What the controller answers to a command
# ---------------------------------------------------------------------------


class CommandCode(StrEnum):
    OK = "ok"
    ROUTE_BUSY = "route_busy"
    INVALID_QUANTITY = "invalid_quantity"
    SOURCE_LOW = "source_low"
    NO_ROOM = "no_room"
    LEVEL_UNKNOWN = "level_unknown"
    LEVEL_LOW = "level_low"
    SETPOINT_OUT_OF_RANGE = "setpoint_out_of_range"
    WORT_NOT_MOVING = "wort_not_moving"
    PROBE_FAULT = "probe_fault"
    DRIVE_FAULT = "drive_fault"


class CommandResult(_Frozen):
    """Accepted or refused. A refusal is an answer, not an error."""

    accepted: bool
    code: CommandCode
    reason: str = ""


# ---------------------------------------------------------------------------
# What a test or an eval does to the plant
# ---------------------------------------------------------------------------


class FaultKind(StrEnum):
    # The instrument lies: the plant is fine
    PROBE_BROKEN = "probe_broken"  # PT100 with a broken wire
    PROBE_OFFSET = "probe_offset"  # value: the degrees it is off by
    SIGNAL_CABLE_BROKEN = "signal_cable_broken"
    LEVEL_STUCK = "level_stuck"  # value: where, or nothing for where it is now
    LEVEL_FOAM = "level_foam"
    HYDROMETER_BATTERY_LOW = "hydrometer_battery_low"
    HYDROMETER_WIFI_LOST = "hydrometer_wifi_lost"
    # The plant is faulty: the instruments tell the truth
    PUMP_BLOCKED = "pump_blocked"
    VALVE_STUCK = "valve_stuck"  # where it is now
    SSR_SHORTED = "ssr_shorted"  # the relay of a heater: always on
    HEATER_OPEN = "heater_open"  # the element of a heater: never on
    GLYCOL_FAILED = "glycol_failed"
    DRIVE_FAULT = "drive_fault"  # value: the fault code of the drive
    FERMENTATION_STUCK = "fermentation_stuck"


class Fault(_Frozen):
    kind: FaultKind
    target: str  # a tag; "CHILLER" for the glycol, "FERM" for the fermentation
    value: float | None = None
