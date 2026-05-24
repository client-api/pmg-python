"""SC-01 — /version returns the expected shape."""
from __future__ import annotations

import re

from clientapi_pmg import Pmg


def test_version_returns_release_and_version(pmg: Pmg) -> None:
    response = pmg.version.version()
    data = response.data
    assert data is not None
    assert data.release, "release missing"
    assert data.version, "version missing"
    assert data.repoid, "repoid missing"
    assert re.match(r"^\d", str(data.release)), data.release
