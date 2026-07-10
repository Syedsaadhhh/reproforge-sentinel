# Reproducibility Passport Schema Draft

The Passport is the main output of ReproForge Sentinel.

It should explain what was claimed, what was checked, what evidence was found, what risks appeared, and what verdict was given.

## Basic JSON shape

```json
{
  "passport_id": "rf-pass-001",
  "project_id": "project-001",
  "claim_id": "claim-001",
  "claim_text": "This repo gives 95% accuracy.",
  "verdict": "not_verified",
  "risk_level": "medium",
  "reproducibility_score": 42,
  "risk_score": 35,
  "evidence_coverage": 40,
  "summary": "The claim could not be verified because the dataset and evaluation script were missing.",
  "evidence_items": [
    {
      "source": "README.md",
      "check": "claim extraction",
      "status": "found",
      "confidence": "high",
      "details": "README claims 95% accuracy but does not link dataset or evaluation script."
    }
  ],
  "risk_indicators": [
    {
      "indicator": "missing_dataset",
      "severity": "medium",
      "points": 20,
      "reason": "No dataset path or download instruction was found."
    }
  ],
  "logs": [
    {
      "step": "static_scan",
      "status": "completed",
      "output": "No dataset file found."
    }
  ],
  "amd_proof": {
    "mode": "mock",
    "credit_status": "pending",
    "runtime_target": "ROCm / AMD GPU when available"
  }
}
```

## Verdict values

| Verdict | Meaning |
|---|---|
| `verified` | Enough evidence was found and the check passed |
| `partially_verified` | Some evidence exists, but important proof is missing |
| `not_verified` | The claim cannot be confirmed from available evidence |
| `high_risk` | The repo/workflow has risky indicators |
| `blocked` | The system should not run the repo/workflow |

## Important rule

The Passport should not overclaim.

It should always show the reason behind the verdict.
