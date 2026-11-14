"""The simulated plant, in three layers that never skip each other.

- process.py: liquids, temperatures, fermentation. The true values.
- devices/: sensors and actuators, with their tolerances and their faults.
- controller/: a small PLC. It reads signals, never a true value.

Between devices and controller, signals.py is the only way. Around the
three: layout.py (what is installed), faults.py, simulator.py (one
calculation step), starts.py (brew day, fermentation), adapter.py (the
three ports of core/plant, in process). The plant itself is described in
docs/impianto.md.

Plain Python, with no FastAPI, httpx or SQLAlchemy: tests and evals run the
plant in process, and the same seed with the same actions gives the same
state. Contracts in pyproject.toml check the imports, and
tests/test_package.py what is really loaded.
"""
