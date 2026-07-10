# Final 24h Execution Plan

Deadline target: 11 July, 9 PM PST.

## Current status

Done:
- Evidence and Passport docs merged into `dev`
- UI/UX docs completed
- Fireworks credits received
- AMD Developer Cloud credit received
- Scoring files shared in WhatsApp

Pending:
- Mayank scoring files need to be pushed to GitHub
- Deban backend `/verify` needs to return Passport JSON
- Gemma/Fireworks call needs to be connected through backend
- Lovable/frontend needs to consume mock/backend Passport JSON
- README, Docker, demo URL, public repo, and submission assets need final polish

## Priority order

### 1. Put scoring files in GitHub
Owner: Mayank / Saad

Required files:
- `scoring/shadowguard.py`
- `scoring/shadowguard_results.json`
- `scoring/shadowguard_results.csv`
- `scoring/synthetic_benchmark_cases.json`
- `scoring/model_report.md`
- `scoring/requirements.txt`

Do not rely on WhatsApp files for final submission.

### 2. Backend MVP
Owner: Deban

Minimum endpoint:

```text
POST /verify
```

It should return Passport-style JSON with:
- claim
- risk_score
- risk_level
- verdict
- reason
- evidence_items
- missing_evidence
- signals_found
- amd_gemma_proof

### 3. Gemma/Fireworks integration
Owner: Saad + Deban

Use Gemma through Fireworks from backend only.

Do not put API keys in frontend or GitHub.

Use `.env`:

```text
FIREWORKS_API_KEY=
FIREWORKS_BASE_URL=
GEMMA_MODEL=
```

First useful Gemma task:
- risk explanation
- evidence summary
- Passport narrative

### 4. AMD proof
Owner: Saad + Deban

For the demo, show AMD use honestly:

```json
{
  "amd_proof_status": "AMD_PATH_CONFIGURED",
  "runtime_mode": "fireworks",
  "model_family": "Gemma",
  "model_provider": "Fireworks",
  "proof_status": "real_api_call"
}
```

If no live AMD GPU droplet is used, do not say ROCm telemetry is verified.

### 5. Frontend/Lovable
Owner: Saad

Build four screens:
- Judge Landing
- Claim Intake
- Live Sandbox Trace
- Reproducibility Passport

Frontend can use mock JSON first, then connect to backend when ready.

### 6. Submission hardening
Owner: Saad

Required:
- public GitHub repo before submission
- Docker/containerized app
- README with setup and usage
- demo URL
- video presentation
- slide deck
- cover image

## Final demo line

ReproForge uses Gemma via Fireworks to explain claim risk and evidence, then issues a Passport with scoring, evidence, and AMD/Fireworks proof status.
