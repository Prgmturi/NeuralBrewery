"""The plant over HTTP: what the controller shows, and the hand of the demo.

- router.py: GET /plant for everyone; the routes of the simulation (move
  the time, inject and clear faults) only when PLANT_SIMULATION_CONTROL is
  on, which staging and production refuse
- schemas.py: what they take and return

A flat feature, like features/auth: no rules and no tables of its own.
"""
