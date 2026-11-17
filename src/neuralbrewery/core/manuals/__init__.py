"""The manuals of the components as the rest of the app sees them.

- schemas.py: a passage of a manual (ManualPassage), plain Python
- protocols.py: ManualSearch, the one way the plant agent reads the manuals

adapters/manuals implements the search, bootstrap.py hands it to the agent
when MANUALS_ENABLED is on. It reads text, and reaches neither the plant
nor the queue.
"""
