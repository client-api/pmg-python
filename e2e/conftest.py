"""Shared pytest fixtures for the PMG E2E suite.

PMG uses ticket auth only — no API tokens (SC-12/13/42 don't apply).
"""
from __future__ import annotations

from typing import Iterator

import pytest

from clientapi_pmg import Pmg
from e2e.helpers.clients import issue_ticket
from e2e.helpers.credentials import Credentials, MissingCredentialError
from e2e.helpers.fixtures import cleanup_e2e


@pytest.fixture(scope="session")
def creds() -> Credentials:
    try:
        return Credentials.from_env()
    except MissingCredentialError as exc:
        pytest.skip(str(exc))


@pytest.fixture(scope="session")
def pmg(creds: Credentials) -> Pmg:
    """PMG client authenticated via ticket (no API tokens on PMG)."""
    return issue_ticket(creds)


@pytest.fixture(scope="session", autouse=True)
def _session_cleanup(creds: Credentials, pmg: Pmg) -> Iterator[None]:
    cleanup_e2e(pmg)
    yield
    cleanup_e2e(pmg)
