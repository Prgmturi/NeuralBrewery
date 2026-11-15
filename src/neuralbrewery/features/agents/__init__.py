"""The agents: they read the plant, judge, and propose. They never command.

- plant_agent.py: the plant agent, on datapizza; diagnoses an alarm
- tools.py: its tools, which read the plant, and the one that hands in the
  diagnosis
- diagnosis.py: what it answers, which the evals check, and how a run went
- mcp_server.py: the MCP server of the app, at /mcp: the same reading
  tools, and one that proposes an action

An agent receives a PlantReader and a datapizza Client, never a command:
rule 1 of AGENTS.md. A proposal goes into the queue through the
ProposalInbox port (core/approvals), and only the brewer's approval sends
it to the executor (features/approvals).

A flat feature, like features/auth: no tables of its own. The rules that
need no LLM, the watcher's, live in core/plant/watcher.py.
"""
