"""What the page offers, and what it shows, in the brewer's words.

The names are the API's: the buttons of the panel and the faults of the
plant (docs/impianto.md). The dashboard imports nothing of the app, so it
keeps its own copy, and a test compares it with the app's.
"""

# The buttons that take no argument: the brewer proposes these from the
# page, start_program and resume_program above all. Those with a route or
# a setpoint come from the agent, or from an MCP client.
PROPOSABLE = (
    "start_program",
    "resume_program",
    "confirm_step",
    "pause_program",
    "abort_program",
    "reset",
    "stop_route",
    "stop_all",
)

FAULT_KINDS = (
    "probe_broken",
    "probe_offset",
    "signal_cable_broken",
    "level_stuck",
    "level_foam",
    "hydrometer_battery_low",
    "hydrometer_wifi_lost",
    "pump_blocked",
    "valve_stuck",
    "ssr_shorted",
    "heater_open",
    "glycol_failed",
    "drive_fault",
    "fermentation_stuck",
)

PROGRAM = {
    "idle": "fermo",
    "running": "in corso",
    "waiting_confirm": "in attesa di conferma",
    "paused": "in pausa",
    "done": "finito",
    "aborted": "annullato",
}

# The status of a proposal: the kind of its last event
STATUS = {
    "proposed": "in attesa",
    "blocked": "bloccata dal guardrail",
    "approved": "approvata",
    "rejected": "rifiutata",
    "executed": "eseguita",
    "execution_failed": "esecuzione fallita",
}

EVENT = {
    "proposed": "proposta",
    "blocked": "bloccata",
    "approved": "approvata",
    "rejected": "rifiutata",
    "executed": "eseguita",
    "execution_failed": "esecuzione fallita",
}

FAULT_TYPE = {
    "measurement": "guasto di misura",
    "process": "guasto di processo",
}


def clock(seconds: float) -> str:
    """Simulated seconds as hours, minutes and seconds: 0:10:00."""
    whole = int(seconds)
    return f"{whole // 3600}:{whole % 3600 // 60:02d}:{whole % 60:02d}"
