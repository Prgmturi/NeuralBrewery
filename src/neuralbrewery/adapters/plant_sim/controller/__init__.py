"""The controller of the plant: a small PLC, simulated.

- measurements.py: from a signal to a measure with its quality
- regulation.py: on/off temperature regulation
- journal.py: the alarms active now, and the log of what happened
- history.py: the short history of readings and commands
- controller.py: the scan cycle, the commands, the interlocks

It knows the plant only through signals.py. An import contract in
pyproject.toml keeps this package away from the process and the devices:
the controller cannot read a true value, not even by mistake.
"""
