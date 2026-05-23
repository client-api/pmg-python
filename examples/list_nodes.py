"""Example: list cluster nodes.

Run with:
    PMG_HOST=https://pmg.example.com:8006 \\
    PMG_TOKEN='PMGAPIToken=root@pam!auto=...' \\
    python examples/list_nodes.py
"""

from __future__ import annotations

import os

from clientapi_pmg.configuration import Configuration
from clientapi_pmg.pmg import Pmg


def main() -> None:
    config = Configuration(host=f"{os.environ.get('PMG_HOST', 'https://localhost:8006')}/api2/json")
    # OpenAPI auth-scheme name (NOT the `Authorization` header name).
    # The full `PMGAPIToken=…` string goes in here; no api_key_prefix.
    config.api_key["PMGApiToken"] = os.environ.get("PMG_TOKEN", "")

    pmg = Pmg(config)
    response = pmg.nodes.get_nodes()
    nodes = getattr(response, "data", None) or []
    print(f"Found {len(nodes)} node(s):")
    for node in nodes:
        print(
            f"  - {getattr(node, 'node', None)} "
            f"(status={getattr(node, 'status', None)}, "
            f"cpu={getattr(node, 'cpu', None)}, "
            f"mem={getattr(node, 'mem', None)}/{getattr(node, 'maxmem', None)})",
        )


if __name__ == "__main__":
    main()
