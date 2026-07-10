# ReproForge Sentinel API

FastAPI backend for the claim → evidence → risk → Passport flow.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Set the frontend variable `VITE_API_BASE_URL=http://localhost:8000`.

## Proof behaviour

- With no `GEMMA_API_KEY`, the evidence narrative is deterministic and labelled `fixture_until_backend`.
- With a valid key, the adapter calls the official Gemini API Gemma 4 model and marks proof real only after a successful response.
- AMD proof becomes `LIVE_ROCM_VERIFIED` only when `amd-smi metric --json` succeeds. Missing hardware or tooling stays pending.

The backend does not yet clone or execute arbitrary repositories. Its current job is to establish the real API/data/proof pipeline safely.
