"""Test fixture cleanup primitives for PMG."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clientapi_pmg import Pmg

log = logging.getLogger(__name__)

E2E_PREFIX = "e2e-"


def cleanup_e2e(pmg: "Pmg") -> None:
    _cleanup_users(pmg)


def _cleanup_users(pmg: "Pmg") -> None:
    try:
        response = pmg.accessUsers.get_users()
    except Exception as exc:
        log.debug("user list failed during cleanup: %r", exc)
        return
    for user in getattr(response, "data", None) or []:
        userid = getattr(user, "userid", "") or ""
        if userid.startswith(E2E_PREFIX):
            try:
                pmg.accessUsers.delete_users(userid=userid)
            except Exception as exc:
                log.debug("delete_users(%s) failed: %r", userid, exc)
