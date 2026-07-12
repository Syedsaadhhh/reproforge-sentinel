# ReproForge Sentinel

**AI can create technical claims faster than teams can verify them. ReproForge turns those claims into evidence, risk signals, and an auditable Reproducibility Passport.**

ReproForge Sentinel is FrontierOps' Track 3 project for the AMD Developer Hackathon: ACT II.

> We are not building a truth machine. We are building an evidence machine.

## Live deployment

- Frontend: https://reproforge-sentinel.onrender.com/
- API health: https://reproforge-sentinel-backend.onrender.com/health
- Interactive API docs: https://reproforge-sentinel-backend.onrender.com/docs

Deployment verification on July 12, 2026 confirmed that the frontend loads, the API health check reports ReproForge Sentinel v0.2.0 as healthy, and a public `POST /verify` request returns a completed run.

The production interface and verification API are live. AMD/Gemma evidence adapters, proof contracts, capture tooling, and strict runtime-status gates are implemented. Provider or hardware measurements appear only when a successful receipt or telemetry artifact is attached; otherwise the Passport preserves an explicit pending state.

## What it does

A user submits a repository URL, technical claim, target runtime, and policy choices. ReproForge then:

1. evaluates the submitted claim metadata;
2. identifies evidence and policy gaps;
3. creates deterministic risk and reproducibility scores;
4. can use Gemma to explain structured findings when a provider is configured;
5. can attach an AMD-hosted provider receipt or direct ROCm telemetry;
6. seals the result as a machine-readable Reproducibility Passport.

~~~text
Claim
  ↓
Controlled evidence and policy evaluation
  ↓
Risk and reproducibility scoring
  ↓
Evidence narrative (Gemma when configured)
  ↓
Runtime proof (provider receipt or ROCm artifact)
  ↓
Reproducibility Passport
~~~

## Judge flow

The interface has four focused screens:

- Landing — product value and verification flow
- Intake — repository, claim, runtime, and policy input
- Trace — readable verification progress and raw logs
- Passport — verdict, risk signals, evidence, missing proof, hashes, AMD/Gemma provenance, and export controls

Fixture mode is always labeled. Live status is shown only after a successful backend response.

## Architecture

~~~text
React + TanStack judge interface
              │
              ▼
          FastAPI API
 /verify · /runs · /passport
              │
      ┌───────┴────────┐
      ▼                ▼
Policy and risk     Gemma narrator
evaluation          Fireworks preferred
      │                │
      └───────┬────────┘
              ▼
 AMD-hosted provider receipt
 and/or AMD SMI + ROCm telemetry
              │
              ▼
 Reproducibility Passport
 evidence · gaps · risks · hashes · proof
~~~

## AMD and Gemma evidence layer

The repository implements Fireworks/Gemma and direct AMD telemetry adapters behind one proof contract. When a configured provider or hardware run succeeds, the Passport records:

- model provider and model ID;
- Gemma task list;
- run ID and UTC timestamp;
- measured latency and token usage;
- proof status;
- AMD ecosystem status.

Direct AMD hardware evidence is captured with ROCm-backed PyTorch and AMD SMI:

~~~bash
python scripts/amd_capture.py \
  --output artifacts/amd-run.json \
  -- python scripts/amd_smoke.py --size 4096 --repeats 12
~~~

The artifact is accepted as live AMD proof only when ROCm, AMD device identity, AMD SMI telemetry, and the workload all succeed. See docs/AMD_GPU_RUNBOOK.md.

## Quick start with Docker

Requirements: Docker Engine with Docker Compose.

~~~bash
cp .env.example .env
docker compose up --build
~~~

Open:

- Frontend: http://localhost:3000
- API health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

With empty provider keys, the application runs safely in guided fixture/fallback mode.

For a real Fireworks Gemma run, set FIREWORKS_API_KEY and the exact FIREWORKS_MODEL in your local .env file. Never commit that file.

## Local development

Frontend:

~~~bash
npm install
npm run dev
~~~

Backend:

~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
~~~

Set VITE_API_BASE_URL=http://localhost:8000 before building the frontend in backend mode.

## Verification API

| Method | Route | Purpose |
|---|---|---|
| GET | /health | Runtime health |
| POST | /projects | Create a project |
| POST | /claims | Store a project claim |
| POST | /verify | Start controlled verification |
| GET | /runs/{run_id} | Read logs and status |
| GET | /passport/{run_id} | Read the final Passport |

## Accepted real-proof payload

The following is an illustrative schema for an accepted provider-backed result, not fixture output:

~~~json
{
  "runtime_mode": "fireworks",
  "amd_status": "active",
  "gemma_used": true,
  "gemma_tasks": ["evidence_narrative"],
  "model_provider": "fireworks",
  "model_name": "<exact-configured-model-id>",
  "proof_status": "real",
  "run_id": "run_xxxxx",
  "timestamp": "2026-07-12T00:00:00Z",
  "latency_ms": 842,
  "tokens_used": 317
}
~~~

Unknown or unavailable values remain null. The product never fills missing runtime measurements with invented zeroes.

## Tests

~~~bash
npm run lint
npm run build
PYTHONPATH=backend pytest backend/tests -q
docker compose build
~~~

GitHub Actions runs the frontend, backend, and container checks for pull requests and final branches.

## Current truth boundary

The current MVP verifies submitted claim metadata and declared policies. It does not yet clone and execute arbitrary repositories. Guided fixture content is explicitly labeled, and live Gemma or AMD proof appears only after a successful provider response or hardware telemetry capture.

The separate ShadowGuard ML research artifacts remain available under ml-detection. The live API currently uses deterministic policy and evidence-risk rules for predictable judge demonstrations.

## Project structure

~~~text
backend/             FastAPI application and tests
src/                 TanStack/React judge interface
scripts/             AMD smoke and artifact capture tools
docs/                Passport, evidence, and AMD runbooks
ml-detection/        ShadowGuard research and benchmark artifacts
Dockerfile           Frontend container
docker-compose.yml   Full local stack
~~~

## Team FrontierOps

- Syed Muhammad Saad — product direction, integration, and submission
- Deban Kumar — backend and container/runtime support
- Mayank Mishra — scoring and ShadowGuard research
- Nivas — evidence, Passport contract, and AMD/Gemma runtime proof
- Areeba Muhammad — product story, documentation, deck, and demo journey

## License

MIT License. See LICENSE.
