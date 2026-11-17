"""The search over the manuals of the components, for the plant agent.

- index.py: reads data/manuals/text/ once, cuts it into passages and
  ranks them with BM25 (ManualIndex, the ManualSearch port of core/manuals)

Plain Python, like the simulated plant: no FastAPI, httpx or SQLAlchemy,
and nothing of the plant or of the queue. It reads text and answers with
text, the same every time. A contract in pyproject.toml checks the imports.
"""
