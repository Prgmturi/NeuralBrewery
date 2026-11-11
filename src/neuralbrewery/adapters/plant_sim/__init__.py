"""The simulated plant: its model, its instruments, its interlocks, its faults.

Plain Python, with no FastAPI, httpx or SQLAlchemy: tests and evals run the
plant in process, and the same seed with the same actions gives the same
state. A contract in pyproject.toml checks the imports, and
tests/test_package.py what is really loaded.

Empty for now: the model arrives with milestone M1 of docs/decisioni.md.
"""
