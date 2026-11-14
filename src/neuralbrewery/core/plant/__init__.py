"""The plant as the rest of the app sees it: its vocabulary and its ports.

- schemas.py: the vocabulary (Reading, PlantState, Route, CommandResult, Fault)
- protocols.py: the ports (PlantReader, PlantCommander, SimulationControl)

The ports are those of the controller of the plant, not of its single
devices: docs/impianto.md says what the controller knows and does.
"""
