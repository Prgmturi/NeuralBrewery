"""The second provider of the agents: an API that copies OpenAI's, through datapizza.

- client.py: datapizza's OpenAI-like client, with the errors translated and
  Gemini's thought signatures kept, and the arguments every call carries

Gemini on its free tier by default; the same code reaches Groq or a local
model. Its settings, OpenAICompatSettings, stay in core/config.
"""
