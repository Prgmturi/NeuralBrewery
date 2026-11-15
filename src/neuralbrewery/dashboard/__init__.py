"""The brewer's dashboard: one Streamlit page over the API, for the demo.

A client of the API, as curl is: it talks HTTP to the API and imports
nothing of the app, no port, adapter or feature (import contracts in
pyproject.toml). Approving stays code of the API, behind the approval
token. Its own image installs only the dashboard group of pyproject.toml:
the image of the API carries neither Streamlit nor what it brings.
"""
