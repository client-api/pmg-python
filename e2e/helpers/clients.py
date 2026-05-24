"""Client factories for PMG ticket auth (PMG has no API tokens)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from clientapi_pmg import Configuration, Pmg

if TYPE_CHECKING:
    from e2e.helpers.credentials import Credentials


def ticket_client(
    creds: "Credentials",
    *,
    ticket: str,
    csrf: str | None = None,
) -> Pmg:
    cfg = Configuration(host=f"{creds.url}/api2/json")
    cfg.verify_ssl = not creds.insecure
    cfg.api_key["PMGAuthCookie"] = ticket
    if csrf is not None:
        cfg.api_key["CSRFPreventionToken"] = csrf
    return Pmg(cfg)


def issue_ticket(creds: "Credentials", *, password: str | None = None) -> Pmg:
    from clientapi_pmg.models.access_ticket_create_ticket_request import (
        AccessTicketCreateTicketRequest,
    )

    anon = Configuration(host=f"{creds.url}/api2/json")
    anon.verify_ssl = not creds.insecure
    bootstrap = Pmg(anon)

    response = bootstrap.accessTicket.create_ticket(
        AccessTicketCreateTicketRequest(
            username=creds.user,
            password=password if password is not None else creds.password,
        )
    )
    data = response.data
    if data is None or not data.ticket:
        raise RuntimeError(f"ticket login returned no ticket: {response!r}")
    return ticket_client(
        creds,
        ticket=data.ticket,
        csrf=data.csrf_prevention_token,
    )
