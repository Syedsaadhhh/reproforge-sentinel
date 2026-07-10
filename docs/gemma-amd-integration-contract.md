# Gemma + AMD Integration Contract

This document defines how ReproForge Sentinel should show Gemma and AMD usage in the MVP.

## Goal

ReproForge should not mention AMD/Gemma only in the pitch. It should show them inside the product flow and final Passport.

## Where Gemma is used

Use Gemma through Fireworks from the backend for one or more of these tasks:

1. `risk_explanation`
   - turn scoring signals into a short explanation

2. `evidence_summary`
   - explain what evidence was found and what is missing

3. `passport_narrative`
   - write the final Passport summary

For MVP, the fastest and strongest task is:

```text
risk_explanation
```

## Where AMD is used

AMD appears through:

- AMD Developer Cloud credit received
- Fireworks AI models hosted on AMD hardware
- optional AMD GPU/ROCm runtime if we spin up a cloud instance
- Passport proof fields showing the runtime path honestly

If we do not capture real ROCm telemetry, do not say `LIVE_ROCM_VERIFIED`.

## Environment variables

Use backend `.env` only:

```text
FIREWORKS_API_KEY=
FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1
GEMMA_MODEL=
AMD_PROOF_MODE=fireworks
```

Never put API keys in frontend or GitHub.

## Backend output object

Every `/verify` response should include:

```json
{
  "amd_gemma_proof": {
    "gemma_used": true,
    "gemma_task": "risk_explanation",
    "model_provider": "fireworks",
    "model_family": "gemma",
    "model_name": "gemma-configured-model",
    "runtime_mode": "fireworks",
    "amd_proof_status": "AMD_PATH_CONFIGURED",
    "proof_status": "real_api_call",
    "latency_ms": null,
    "tokens_used": null
  }
}
```

## Honest status rules

Use these statuses:

- `LIVE_ROCM_VERIFIED` only if real ROCm telemetry is captured
- `AMD_PATH_CONFIGURED` if AMD/Fireworks path is configured but no ROCm telemetry is captured
- `AMD_AWARE_SIMULATED` if using fixture/mock telemetry
- `AMD_UNAVAILABLE` if no AMD/Fireworks path is active

## Demo wording

Good:

> Gemma via Fireworks explains risk signals and Passport reasoning. AMD proof status shows the runtime path honestly.

Avoid:

> Fully AMD verified.
> Hardware signature proven.
> ROCm telemetry verified.

unless actually implemented.
