"""The devices of the plant: what stands between the process and the controller.

- sensors.py: the 4-20 mA transmitters and the wireless hydrometer
- actuators.py: pumps, valves, heaters, the drive of the agitator
- safety.py: the thermostats and K1, wired outside the controller
- field.py: all of them together, as the controller is wired to them

Noise, tolerances and faults live here: the process does not know how it
is measured, and the controller knows only the signals.
"""
