"""The queue of proposals, their approval, and the audit of every step.

- domain/: the rules in plain Python. The guardrail checks a proposal
  against the panel before it enters; only a proposal waiting for the
  brewer is approved or rejected; an approved one is pressed once, by the
  executor, and its answer is written.
- persistence/: the table approval_events, to which events are only
  added. A proposal's status is its last event.
- api/: the routes of the brewer (approve and reject need the approval
  token), the executor, the only code that holds PlantCommander, and the
  inbox that agents and the MCP server propose through.
"""
