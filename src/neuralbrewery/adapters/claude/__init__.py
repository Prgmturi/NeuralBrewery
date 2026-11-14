"""The Claude adapter: the model of the agents, through datapizza.

- client.py: the datapizza client for Claude, and the arguments every call
  carries (tokens, effort, fallback on refusals, prompt cache)

The port is datapizza's Client: an agent takes any client of the framework,
so a second provider is another folder next to this one. Its settings,
ClaudeSettings, stay in core/config.
"""
