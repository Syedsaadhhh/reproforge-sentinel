# ReproForge Sentinel API

FastAPI backend for the claim → evidence → risk → Reproducibility Passport flow.

## Run locally

~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
~~~

On Windows, activate the environment with .venv\Scripts\activate.

## Run with Docker

From the repository root:

~~~bash
cp .env.example .env
docker compose up --build
~~~

API health: http://localhost:8000/health

## Environment

- FIREWORKS_API_KEY and FIREWORKS_MODEL activate the preferred AMD-hosted Fireworks Gemma path.
- GEMMA_API_KEY and GEMMA_MODEL activate the optional Google Gemini API fallback.
- ALLOWED_ORIGINS configures browser origins allowed by FastAPI.

Never put provider keys in frontend variables or commit them to GitHub.

## Proof behavior

- A successful provider response produces proof_status=real with the exact provider, model, task list, run ID, timestamp, latency and token usage.
- No key or an API failure produces proof_status=pending with deterministic fallback text and no invented metrics.
- Fireworks-confirmed inference marks the AMD ecosystem path active because the event provides Fireworks inference on AMD-hosted infrastructure.
- Direct hardware proof becomes LIVE_ROCM_VERIFIED only after amd-smi telemetry succeeds.
- The backend records evidence hashes for successful provider receipts and live AMD telemetry.

## API

- GET /health
- POST /projects
- POST /claims
- POST /verify
- GET /runs/{run_id}
- GET /passport/{run_id}

## Current scope

The API evaluates submitted claim metadata and declared policies. It does not yet clone or execute arbitrary repositories. This limitation is intentional and visible in every generated Passport.
