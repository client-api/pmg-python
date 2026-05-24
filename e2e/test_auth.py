"""SC-10, SC-11, SC-14 — authentication (PMG: no API tokens, so SC-12/13 omitted)."""
from __future__ import annotations

import pytest

from clientapi_pmg import Configuration, Pmg
from clientapi_pmg.exceptions import ApiException
from clientapi_pmg.models.access_ticket_create_ticket_request import (
    AccessTicketCreateTicketRequest,
)
from e2e.helpers.clients import issue_ticket, ticket_client
from e2e.helpers.credentials import Credentials


def test_ticket_login_returns_ticket_and_csrf(creds: Credentials) -> None:
    """SC-10 — POST /access/ticket yields ticket + CSRFPreventionToken."""
    anon = Configuration(host=f"{creds.url}/api2/json")
    anon.verify_ssl = not creds.insecure
    pmg = Pmg(anon)

    response = pmg.accessTicket.create_ticket(
        AccessTicketCreateTicketRequest(username=creds.user, password=creds.password)
    )
    data = response.data
    assert data is not None
    assert data.ticket, "ticket missing"
    assert data.csrf_prevention_token, "CSRFPreventionToken missing"


def test_invalid_password_raises_401(creds: Credentials) -> None:
    """SC-11 — wrong password ⇒ 401."""
    with pytest.raises(ApiException) as excinfo:
        issue_ticket(creds, password="definitely-not-the-password")
    assert excinfo.value.status == 401, excinfo.value


def test_ticket_write_without_csrf_is_rejected(creds: Credentials) -> None:
    """SC-14 — ticket auth writes require CSRFPreventionToken header."""
    anon = Configuration(host=f"{creds.url}/api2/json")
    anon.verify_ssl = not creds.insecure
    bootstrap = Pmg(anon)
    ticket_response = bootstrap.accessTicket.create_ticket(
        AccessTicketCreateTicketRequest(username=creds.user, password=creds.password)
    )
    ticket = ticket_response.data.ticket
    assert ticket

    no_csrf = ticket_client(creds, ticket=ticket, csrf=None)

    # GETs work without CSRF.
    response = no_csrf.accessUsers.get_users()
    assert getattr(response, "data", None) is not None

    from clientapi_pmg.models.access_users_create_users_request import (
        AccessUsersCreateUsersRequest,
    )
    from clientapi_pmg.models.pmg_role_enum import PmgRoleEnum

    with pytest.raises(ApiException) as excinfo:
        no_csrf.accessUsers.create_users(
            AccessUsersCreateUsersRequest(
                userid="e2e-csrf-probe@pmg",
                password="not-a-real-secret-1234",
                role=PmgRoleEnum.AUDIT,
                comment="should fail without CSRF",
            )
        )
    assert excinfo.value.status == 401, excinfo.value
