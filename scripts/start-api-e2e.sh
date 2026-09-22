#!/usr/bin/env bash
set -euo pipefail

if [[ -x "services/api/.venv/bin/python" ]]; then
  exec services/api/.venv/bin/python services/api/scripts/run_e2e_server.py
fi

exec python3 services/api/scripts/run_e2e_server.py
