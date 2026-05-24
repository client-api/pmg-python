"""Load PROXMOX_* environment variables exported by client-api/proxmox-docker-action@v1.

PMG has no API tokens, so `PROXMOX_TOKEN_HEADER_VALUE` is optional here.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


class MissingCredentialError(RuntimeError):
    """Raised when a required PROXMOX_* env var is missing."""


@dataclass(frozen=True)
class Credentials:
    url: str
    user: str
    password: str
    insecure: bool

    @classmethod
    def from_env(cls) -> "Credentials":
        url = _required("PROXMOX_URL")
        return cls(
            url=url.rstrip("/"),
            user=_required("PROXMOX_USER"),
            password=_required("PROXMOX_PASSWORD"),
            insecure=os.environ.get("PROXMOX_INSECURE", "").lower() in ("1", "true", "yes"),
        )


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise MissingCredentialError(
            f"{name} is not set. Run client-api/proxmox-docker-action@v1 in CI "
            f"or export it manually for local runs."
        )
    return value
