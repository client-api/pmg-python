# E2E tests for `clientapi_pmg`

Live-server pytest suite against a real Proxmox Mail Gateway instance.

## Quick start (local)

```bash
docker compose up -d
sleep 20

export PROXMOX_URL=https://localhost:8006
export PROXMOX_USER=root@pam
export PROXMOX_PASSWORD=proxmox123
export PROXMOX_INSECURE=1

pip install -e .
pip install 'pytest>=8' 'pytest-timeout>=2.3' requests
pytest e2e/ -v
```

PMG does not have API tokens — `PROXMOX_TOKEN_HEADER_VALUE` is unused.

## Scenario index

PMG-applicable subset (no API tokens → SC-12/13/42 omitted):

| File | Scenarios |
|---|---|
| `test_version.py` | SC-01 |
| `test_auth.py` | SC-10 (ticket login), SC-11 (invalid pw), SC-14 (CSRF on writes) |
| `test_crud.py` | SC-30, SC-31 (user CRUD) |
| `test_errors.py` | SC-41 (input validation) |
| `test_types.py` | SC-50 (int64 uptime/time), SC-51 (nullable) |

Storage CRUD, ISO upload, VM/CT lifecycle, and oneOf discriminator scenarios
are PVE-specific and live in `pve-python/e2e/`.
