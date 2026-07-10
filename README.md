# ReproForge Sentinel

ReproForge Sentinel is an AI claim-to-evidence verification system.

The goal is simple: when a repo, AI agent, model card, or developer makes a technical claim, ReproForge checks what evidence exists, what looks risky, what is missing, and what verdict can be given honestly.

We are not building a truth machine. We are building an evidence machine.

---

## Problem

AI tools and developers can now produce technical claims very quickly.

Examples:

- “This repo gives 95% accuracy.”
- “This agent can safely modify config files.”
- “This model runs on AMD or ROCm.”
- “This script detects phishing links.”
- “This project is production ready.”

The problem is that these claims are often hard to trust. A repo may be missing its dataset, have unsafe commands, fake metrics, broken dependencies, or no clear proof.

ReproForge Sentinel turns those claims into a clear evidence report.

---

## Core Idea

The system takes a claim and produces a Reproducibility Passport.

```text
Claim
  ↓
Evidence Check
  ↓
Repo / Workflow Risk Scan
  ↓
Verification Run or Controlled Result
  ↓
Score + Verdict
  ↓
Reproducibility Passport
```

The final passport does not say “100% safe” or “100% true.”

It says:

> Based on these checks, this claim is verified, partially verified, not verified, high risk, or blocked.

---

## MVP Scope

For the hackathon MVP, we will start with a small controlled benchmark of repo and workflow cases.

Example cases:

| Case | Example claim | Expected result |
|---|---|---|
| Clean repo | “This script runs successfully.” | Verified |
| Missing dependency | “This repo works out of the box.” | Not verified |
| Fake accuracy claim | “This model gives 95% accuracy.” | Not enough evidence |
| Missing dataset | “This model can be reproduced.” | Not verified |
| Risky install | “This setup script is safe.” | High risk |
| Agent action | “This agent can safely edit config.” | Needs approval / blocked |
| Dummy secret | “This repo is production ready.” | High risk |

This lets us build a stable demo without depending on random GitHub repos.

---

## Risk Scoring

Repo safety is not treated as a final guarantee. It is treated as a risk assessment based on visible signals.

Possible indicators:

- Dangerous shell commands
- `sudo` or admin-level commands
- `curl | bash` or `wget | bash`
- File deletion or system file access
- Exposed dummy secrets or API keys
- Suspicious install scripts
- Unknown or risky dependencies
- Network calls
- Missing dataset
- Missing evaluation script
- Claimed result does not match available evidence

Risk levels:

| Score range | Level |
|---|---|
| 0-20 | Low |
| 21-40 | Medium |
| 41-70 | High |
| 71+ | Blocked |

This score is a heuristic trust assessment, not a mathematical guarantee of safety.

---

## Evidence Validity

Every evidence item should be traceable.

Each evidence item should include:

- Source file or command
- What was checked
- Timestamp
- Hash/checksum if possible
- Raw output or logs
- Confidence level
- Short reason

This makes the passport easier to trust because the user can see why the verdict was given.

---

## System Architecture

```text
User / Judge / Developer
        │
        ▼
ReproForge Dashboard
Claim input + Passport view
        │
        ▼
FastAPI Backend
Projects / Claims / Verify / Passport
        │
        ├── Claim Parser
        │      Extracts what is being claimed
        │
        ├── Risk Scanner
        │      Finds risky commands, secrets, unsafe patterns
        │
        ├── Evidence Collector
        │      Collects files, logs, metadata, outputs
        │
        ├── Scoring Engine
        │      Creates risk score and reproducibility score
        │
        └── Passport Generator
               Produces final report/result
        │
        ▼
Database + Cache
PostgreSQL / SQLite for MVP, Redis later
        │
        ▼
AMD / ROCm Proof Layer
Mock first, real telemetry when credits are available
```

---

## Planned Backend Flow

```text
Project created
      │
      ▼
Claim added
      │
      ▼
Verification request
      │
      ▼
Parse claim
      │
      ▼
Scan risk indicators
      │
      ▼
Collect evidence
      │
      ▼
Calculate score
      │
      ▼
Return passport/result
```

Basic API routes:

```text
GET  /health
POST /projects
POST /claims
POST /verify
GET  /runs/{id}
GET  /passport/{id}
```

---

## Team Roles

| Member | Main focus |
|---|---|
| Saad | Product direction, coordination, pitch, demo story |
| Deban | Backend, API flow, database structure |
| Mayank | Agentic/data part, benchmark cases, scoring logic |
| Nivas | Evidence validity, passport flow, visual explanation |
| Areeba | Research, documentation, simple UI/wireframe support |

---

## Branch Flow

```text
main
  Stable final work only

 dev
  Combined working version

 backend/deban
  Backend and API work

 scoring/mayank
  Scoring logic and benchmark cases

 evidence/nivas
  Evidence validity and passport flow

 docs-ui/areeba
  Research, docs, UI/wireframe support

 product/saad
  Product direction, pitch, demo story
```

Rules:

- Do not push directly to `main`.
- Work in your own branch first.
- Merge into `dev` after review.
- Only stable work goes from `dev` to `main`.
- Do not upload `.env`, API keys, credentials, `.venv`, or large zip files.

---

## First Build Targets

### Backend

- Clean FastAPI structure
- Project model
- Claim model
- Verification run model
- Passport/result output
- Simple README for backend setup

### Scoring

- 10-15 sample benchmark cases
- Score indicators
- Verdict rules
- Low/Medium/High/Blocked mapping

### Evidence

- Evidence JSON format
- Trace fields
- Example evidence items
- Passport explanation flow

### Docs and UI

- Simple problem explanation
- Judge-friendly demo flow
- Claim input screen sketch
- Result/passport screen sketch

---

## Current Status

This project is in early MVP planning and build setup.

The first goal is not to build a perfect full product. The first goal is to create a working flow:

```text
Claim in → Evidence checked → Risk scored → Passport out
```

Once that works, we can improve the UI, add stronger backend logic, connect real repo scanning, and later add AMD/ROCm execution proof if credits become available.

---

## Short Pitch

AI can generate technical claims faster than humans can verify them.

ReproForge Sentinel helps teams check those claims by turning them into evidence, risk signals, scores, and a clear Reproducibility Passport.

It does not ask users to blindly trust AI output. It shows what was checked, what was missing, and why the final verdict was given.


---

## Judge-demo frontend

The Lovable-generated TanStack Start frontend is integrated on the `agent/lovable-mvp-integration` branch.

- Four screens: Judge Landing, Claim Intake, Live Sandbox Trace, Reproducibility Passport
- Guided fixture mode by default, always labelled
- Backend mode through `VITE_API_BASE_URL`
- Client contracts: `POST /verify`, `GET /runs/{run_id}`, `GET /passport/{run_id}`
- Intake state flows into the trace and Passport
- Raw-log inspection, JSON export, browser PDF export, and run-specific share links
- AMD/ROCm and Gemma proof remain explicitly unverified until backend confirmation

Run `npm install && npm run dev` after the frontend files are present. Use `npm run build` and `npm run lint` for validation.
