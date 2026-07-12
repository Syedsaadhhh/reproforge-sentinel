#!/usr/bin/env bash
set -euo pipefail

echo "> Building images..."
docker compose build

echo "> Starting services..."
docker compose up -d

echo "> Waiting for health checks (20s)..."
sleep 20

echo "> Backend health..."
curl -fsS http://localhost:8000/health | jq .

echo "> Backend API smoke test..."
curl -fsS -X POST http://localhost:8000/verify \
  -H "content-type: application/json" \
  -d '{
    "repo_url": "https://github.com/example/reproforge-case",
    "claim_text": "This benchmark achieves 95% accuracy safely.",
    "claim_type": "benchmark_result",
    "runtime_target": "linux/x86_64 · ROCm · AMD-aware pending",
    "policies": ["egress_deny", "exec_pipe_deny", "fs_readonly"],
    "verification_mode": "deep"
  }' | jq .

echo "> Frontend reachable..."
curl -fsS http://localhost:4173 | head -n 1

echo "> Container status..."
docker compose ps

echo "> Tearing down..."
docker compose down

echo "Smoke test passed."
