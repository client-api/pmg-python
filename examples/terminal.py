"""Example: open a terminal session against a QEMU VM.

Run with:
    PMG_HOST=https://pmg.example.com:8006 \\
    PMG_TOKEN='PMGAPIToken=root@pam!auto=...' \\
    PMG_NODE=orca PMG_VMID=100 \\
    python examples/terminal.py

Requires: pip install websocket-client
"""

from __future__ import annotations

import os
import sys
import time

from clientapi_pmg.configuration import Configuration
from clientapi_pmg.pmg import Pmg
from clientapi_pmg.websocket import QemuTarget


def main() -> None:
    config = Configuration(host=f"{os.environ.get('PMG_HOST', 'https://localhost:8006')}/api2/json")
    # `PMGApiToken` is the OpenAPI auth-scheme name the REST client keys
    # by; the *header* it lands on is `Authorization`. Put the full
    # `PMGAPIToken=…` string in here (no `api_key_prefix`).
    config.api_key["PMGApiToken"] = os.environ.get("PMG_TOKEN", "")

    pmg = Pmg(config)
    target = QemuTarget(
        node=os.environ.get("PMG_NODE", "pmg1"),
        vmid=int(os.environ.get("PMG_VMID", "100")),
    )

    print(f"Opening terminal on {target.node}:qemu/{target.vmid}...")
    session = pmg.connect_terminal(
        target,
        on_message=lambda text: sys.stdout.write(text),
        on_close=lambda code, reason: print(f"\n[closed: {code} {reason}]"),
        on_error=lambda exc: print(f"\n[error: {exc}]"),
    )

    session.resize(120, 32)
    session.send("uname -a\n")

    time.sleep(5)
    session.close()


if __name__ == "__main__":
    main()
