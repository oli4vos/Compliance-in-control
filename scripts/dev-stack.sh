#!/usr/bin/env bash

set -euo pipefail

compose_args=()
if [[ -f .env.local ]]; then
  compose_args+=(--env-file .env.local)
fi

exec docker compose "${compose_args[@]}" up --build
