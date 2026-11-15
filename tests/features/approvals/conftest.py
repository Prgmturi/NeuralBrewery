"""Approvals fixtures: the token of the brewer, and the log kept in memory."""

import pytest

from neuralbrewery.core.config import ApprovalSettings, ServerSettings, Settings
from neuralbrewery.features.approvals.api.dependencies import get_proposal_log
from tests.features.approvals.fakes import InMemoryProposalLog

TOKEN = "test-approval-token"
BREWER = {"X-Approval-Token": TOKEN}


@pytest.fixture
def settings() -> Settings:
    """The test settings, with an approval token."""
    return Settings(
        server=ServerSettings(trusted_hosts=["testserver"]),
        approvals=ApprovalSettings(token=TOKEN),
    )


@pytest.fixture
def log() -> InMemoryProposalLog:
    return InMemoryProposalLog()


@pytest.fixture
def app(app, log):
    """The app of tests/conftest.py, its plant in the process, the log in memory."""
    app.dependency_overrides[get_proposal_log] = lambda: log
    return app
