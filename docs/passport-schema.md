# Reproducibility Passport Specification

## Overview

The **Reproducibility Passport** is the primary output of **ReproForge Sentinel**.

It summarizes the verification process by showing:

- What technical claim was submitted
- What evidence was collected
- What evidence was missing
- What risks were detected
- How reproducible the claim is
- The final verification verdict

The Passport is **not** a guarantee that a repository or workflow is completely safe or completely true.

Instead, it provides a transparent, evidence-based assessment that explains **what was checked, what was found, and why a particular verdict was reached.**

---

# Passport Structure

Every Passport should contain the following sections.

## 1. Passport Metadata

Basic information about the verification report.

| Field | Description |
|--------|-------------|
| passport_id | Unique Passport identifier |
| passport_version | Passport schema version |
| generated_at | Timestamp when the Passport was created |
| verification_engine | Version of ReproForge Sentinel |

---

## 2. Claim Information

Information about the submitted claim.

| Field | Description |
|--------|-------------|
| project_id | Project identifier |
| claim_id | Claim identifier |
| claim_text | Original technical claim |

---

## 3. Verification Result

The overall result of the verification process.

| Field | Description |
|--------|-------------|
| verdict | Final verification result |
| summary | Human-readable explanation |

---

## 4. Scores

The Passport reports multiple independent scores.

| Field | Description |
|--------|-------------|
| risk_level | Low / Medium / High / Blocked |
| risk_score | Repository risk score |
| reproducibility_score | Ability to reproduce the claim |
| credibility_score | Trustworthiness of available evidence |
| evidence_coverage | Percentage of required evidence found |

---

## 5. Evidence

All collected evidence supporting the verdict.

Each evidence item should follow the Evidence Schema.

Example fields:

- evidence_id
- category
- source
- check
- status
- confidence
- severity
- reason

---

## 6. Missing Evidence

Lists important artifacts that were expected but not found.

Examples:

- Dataset
- Evaluation script
- Model weights
- Dockerfile
- Installation guide

---

## 7. Risk Indicators

Every detected risk should be listed separately.

Each indicator contains:

- indicator
- severity
- score contribution
- explanation

---

## 8. Verification Logs

Execution logs generated during verification.

Examples:

- Static scan
- Dependency analysis
- Repository inspection
- Sandbox execution
- Evidence collection

---

## 9. Recommendations

Suggestions for improving reproducibility or reducing risk.

Example recommendations:

- Provide dataset download link
- Add evaluation script
- Include model weights
- Pin dependency versions
- Remove exposed secrets

---

## 10. AMD Verification Layer

Future support for AMD hardware verification.

Fields:

- execution mode
- runtime target
- telemetry status
- GPU information (future)

---

# Complete JSON Example

```json
{
  "passport_id": "RF-PASS-001",
  "passport_version": "1.0",
  "generated_at": "2026-07-05T18:45:00Z",
  "verification_engine": "ReproForge Sentinel v1.0",

  "project_id": "PROJECT-001",
  "claim_id": "CLAIM-001",

  "claim_text": "This repository achieves 95% accuracy.",

  "verdict": "partially_verified",

  "summary": "The repository contains implementation artifacts, but the claimed accuracy could not be independently verified because the dataset and evaluation script are missing.",

  "risk_level": "medium",
  "risk_score": 35,
  "reproducibility_score": 42,
  "credibility_score": 74,
  "evidence_coverage": 60,

  "evidence_items": [
    {
      "evidence_id": "EV-001",
      "category": "documentation",
      "source": "README.md",
      "check": "Accuracy claim verification",
      "status": "verified",
      "confidence": 0.94,
      "severity": "low",
      "reason": "README contains the claimed accuracy."
    }
  ],

  "missing_evidence": [
    "dataset",
    "evaluation_script",
    "model_weights"
  ],

  "risk_indicators": [
    {
      "indicator": "missing_dataset",
      "severity": "medium",
      "points": 20,
      "reason": "No dataset or download instructions were found."
    }
  ],

  "logs": [
    {
      "step": "static_repository_scan",
      "status": "completed",
      "output": "Dataset not found."
    }
  ],

  "recommendations": [
    "Provide dataset download link.",
    "Include evaluation script.",
    "Document benchmark methodology."
  ],

  "amd_gemma_proof": {
  "runtime_mode": "mock",
  "amd_status": "pending",
  "gemma_used": false,
  "gemma_tasks": [],
  "model_provider": "local_mock",
  "model_name": null,
  "proof_status": "mock",
  "latency_ms": null,
  "tokens_used": null,
  "run_id": null,
  "timestamp": null
  }
}
> **Note:** The values shown above are illustrative. During actual verification, `model_name`, `run_id`, `latency_ms`, `tokens_used`, and `timestamp` must be populated from the live Fireworks/AMD runtime instead of hardcoded values.
### Real Runtime Example (Illustrative)

```json
"amd_gemma_proof": {
  "runtime_mode": "fireworks",
  "amd_status": "active",
  "gemma_used": true,
  "gemma_tasks": [
    "claim_parser",
    "passport_writer"
  ],
  "model_provider": "fireworks",
  "model_name": "<configured_fireworks_model_id>",
  "proof_status": "real",
  "latency_ms": 143,
  "tokens_used": 512,
  "run_id": "run_xxxxx",
  "timestamp": "2026-07-07T10:30:45Z"
}
```
```

---
## Enum Definitions

### Verdict

| Value | Meaning |
|--------|---------|
| verified | Sufficient evidence supports the claim |
| partially_verified | Some evidence exists, but important artifacts are missing |
| not_verified | The claim cannot be confirmed |
| high_risk | Significant risks were detected |
| blocked | Verification was blocked due to safety concerns |

---

### Risk Level

| Value | Meaning |
|--------|---------|
| low | Minimal execution risk |
| medium | Moderate execution risk |
| high | Significant execution risk |
| blocked | Repository or workflow should not be executed |

---

### AMD Proof Mode

| Value | Meaning |
|--------|---------|
| mock | Simulated verification (MVP mode) |
| runtime | Verified using actual AMD/ROCm hardware |

---

### Credit Status

| Value | Meaning |
|--------|---------|
| pending | AMD resources not yet available |
| available | AMD resources available |
| completed | Verification completed on AMD hardware |

# Verdict Values

| Verdict | Meaning |
|----------|---------|
| `verified` | Sufficient evidence was found and the claim was successfully verified. |
| `partially_verified` | Some evidence exists, but important supporting artifacts are missing. |
| `not_verified` | The claim cannot be confirmed using the available evidence. |
| `high_risk` | The repository or workflow contains significant security or execution risks. |
| `blocked` | Verification was stopped because executing the repository or workflow would be unsafe. |

---

# Design Principles

The Reproducibility Passport should always be:

- Transparent
- Explainable
- Evidence-driven
- Machine-readable
- Human-readable
- Traceable
- Easy to audit

Every score and verdict shown in the Passport must be supported by collected evidence. The Passport summarizes the verification process—it does not make unsupported claims or guarantee absolute safety.
## Important rule

The Passport should not overclaim.

It should always show the reason behind the verdict.
