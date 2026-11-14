"""On/off temperature regulation, one loop for each vessel."""

from dataclasses import dataclass

BAND_C = 0.5
# At this setpoint the kettle is held at the boil. No other vessel can be
# set this high: the highest setpoints are in layout.py.
BOIL_SETPOINT_C = 100.0
BOIL_POWER_PCT = 75.0


@dataclass
class Loop:
    setpoint_c: float | None = None  # None: off
    heater_pct: float = 0.0
    cooling: bool = False  # only the fermenter has something to cool with

    def follow(self, temp_c: float | None) -> None:
        """Decide heater and cooling from the control probe; None stops both."""
        setpoint_c = self.setpoint_c
        if setpoint_c is None or temp_c is None:
            self.heater_pct, self.cooling = 0.0, False
        elif setpoint_c >= BOIL_SETPOINT_C:
            # A boil wants steady power: full to get there, then less to hold
            # it. Switched on and off, it would stop every few seconds.
            boiling = temp_c >= setpoint_c - BAND_C
            self.heater_pct = BOIL_POWER_PCT if boiling else 100.0
        else:
            # Inside the band nothing changes: the output does not chatter
            if temp_c < setpoint_c - BAND_C:
                self.heater_pct = 100.0
            elif temp_c >= setpoint_c:
                self.heater_pct = 0.0
            if temp_c > setpoint_c + BAND_C:
                self.cooling = True
            elif temp_c <= setpoint_c:
                self.cooling = False
