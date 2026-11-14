"""The agents: they read the plant, judge, and propose. They never command.

- plant_agent.py: the plant agent, on datapizza; diagnoses an alarm
- tools.py: its tools, which read the plant, and the one that hands in the
  diagnosis
- diagnosis.py: what it answers, which the evals check, and how a run went

An agent receives a PlantReader and a datapizza Client, never a command:
rule 1 of AGENTS.md. A proposed command is text in the diagnosis, and no
code executes it (the approvals and the executor come with M4).

A flat feature, like features/auth: no HTTP and no tables yet. The rules
that need no LLM, the watcher's, live in core/plant/watcher.py.
"""
