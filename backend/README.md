# Backend Plan

Backend owner: Deban

The backend should support the basic ReproForge Sentinel flow:

```text
project → claim → verification run → evidence → score → passport/result
```

## Suggested stack

- FastAPI
- SQLite for very early MVP, PostgreSQL later
- Redis later for cache/job status
- Pydantic schemas

## First routes

```text
GET  /health
POST /projects
POST /claims
POST /verify
GET  /runs/{id}
GET  /passport/{id}
```

## First models

```text
Project
- id
- name
- description
- created_at

Claim
- id
- project_id
- claim_text
- source_type
- created_at

VerificationRun
- id
- claim_id
- status
- verdict
- risk_score
- reproducibility_score
- created_at

EvidenceItem
- id
- run_id
- source
- check
- status
- details
- confidence

Passport
- id
- run_id
- summary
- verdict
- evidence_coverage
- output_json
```

## First verify workflow

1. Receive claim input
2. Parse the claim text
3. Detect sample risk indicators
4. Return score and verdict
5. Store result
6. Return passport-style JSON

Keep it simple first. The goal is a working flow, not a perfect backend.
