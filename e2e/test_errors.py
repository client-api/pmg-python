"""SC-41 — input validation (PMG has no API tokens, so SC-42 omitted)."""
from __future__ import annotations

import pytest

from clientapi_pmg import Pmg
from clientapi_pmg.models.access_users_create_users_request import (
    AccessUsersCreateUsersRequest,
)
from clientapi_pmg.models.pmg_role_enum import PmgRoleEnum


def test_invalid_password_length_rejected(pmg: Pmg) -> None:
    """SC-41 — invalid input (password too short) is caught client- or server-side."""
    with pytest.raises(Exception) as excinfo:
        pmg.accessUsers.create_users(
            AccessUsersCreateUsersRequest(
                userid="e2e-tooshort@pmg",
                password="abc",
                role=PmgRoleEnum.AUDIT,
            )
        )
    assert excinfo.type.__name__ in {"ValidationError", "BadRequestException", "ApiException"}, excinfo.value
