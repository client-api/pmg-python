"""SC-50 / SC-51 — type-correctness checks on the generated SDK."""
from __future__ import annotations

import typing

from clientapi_pmg import Pmg
from clientapi_pmg.models.nodes_status_status_response_data import (
    NodesStatusStatusResponseData,
)


def test_int64_fields_are_python_int() -> None:
    """SC-50 — uptime / time round-trip as `int`, not `float`."""
    hints = typing.get_type_hints(NodesStatusStatusResponseData)
    for field in ("uptime", "time"):
        annotation = hints[field]
        members = typing.get_args(annotation) or (annotation,)
        assert any(m is int or getattr(m, "__name__", "") == "StrictInt" for m in members), (
            f"{field} annotation is {annotation!r} — must include int"
        )


def test_nullable_fields_deserialize_to_none(pmg: Pmg) -> None:
    """SC-51 — Optional fields that the server omits arrive as `None`."""
    users = pmg.accessUsers.get_users().data or []
    assert users, "expected at least one user"
    # `firstname` is Optional[str] on the response model; default-seeded root
    # has no firstname set.
    omitted = [u for u in users if getattr(u, "firstname", None) is None]
    assert omitted, "no user had a None firstname — model may be coercing Optional fields"
