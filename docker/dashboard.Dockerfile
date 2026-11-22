# =============================================================================
# The brewer's dashboard, in an image of its own
# =============================================================================
# Only the dashboard group of pyproject.toml (Streamlit, httpx,
# pydantic-settings) and the code of src/neuralbrewery/dashboard/. The image
# of the API (docker/Dockerfile) stays without Streamlit and what it brings:
# numpy, pandas and pyarrow, about 300 MB that the API never imports, and
# more packages for its scan to watch. compose.yaml builds this one for the
# demo; CI does not publish it.
#
# The same base image as the API's, by tag and by digest, the same Debian
# fixes and the same uv (tests/test_dashboard_image.py): a new base moves
# in both files at once, by hand. CI scans this image too.
# =============================================================================

FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS builder

WORKDIR /app

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

# --only-group dashboard: that group alone, without the dependencies of the
#   API, which the dashboard does not import (an import contract checks it).
# --no-install-project: the dashboard is a few files, copied below.
RUN uv sync --locked --only-group dashboard --no-install-project


FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS runtime

WORKDIR /app

# PYTHONPATH: the package neuralbrewery is not installed here; its empty
#   __init__.py and the dashboard are enough.
# STREAMLIT_*: all interfaces inside the container, since compose publishes
#   the port on 127.0.0.1 only; the address the browser uses, localhost,
#   which also stops Streamlit from asking a service on the internet for
#   the public address of the machine, to print it; no question at the
#   start; no usage statistics sent to Streamlit; no watching of files
#   that never change.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_SERVER_ADDRESS=localhost \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# The same Debian fixes as the API's image, zlib1g and the C library, until
# the base brings them (docker/Dockerfile)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade \
       zlib1g libc6 libc-bin \
    && rm -rf /var/lib/apt/lists/*

# As in the API's image, the user owns nothing: code and packages are root's
RUN useradd --no-create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /app/.venv /app/.venv
COPY src/neuralbrewery/__init__.py src/neuralbrewery/__init__.py
COPY src/neuralbrewery/dashboard src/neuralbrewery/dashboard

USER appuser

EXPOSE 8501

# Streamlit's own probe; urllib, since the slim image has no curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5)"]

CMD ["streamlit", "run", "src/neuralbrewery/dashboard/app.py"]
