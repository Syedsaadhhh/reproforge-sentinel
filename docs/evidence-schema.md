# Evidence Schema

## Overview

An evidence item is a single verifiable artifact collected during claim verification.

Evidence is used to support or contradict a technical claim. Every evidence item should be traceable, explainable, and machine-readable so that the final Reproducibility Passport can justify its verdict.

---

# Evidence Structure

Each evidence item contains the following fields.

| Field | Type | Description |
|--------|------|-------------|
| evidence_id | String | Unique identifier for the evidence |
| category | Enum | Type of evidence (Documentation, Dataset, Security, Dependency, Execution, etc.) |
| source | String | File, command, or system that produced the evidence |
| check | String | Verification step performed |
| status | Enum | Verified, Failed, Missing, Warning, Not Applicable |
| confidence | Float (0–1) | Confidence in the verification result |
| severity | Enum | Low, Medium, High, Critical |
| reason | String | Human-readable explanation |
| timestamp | DateTime | When the evidence was collected |
| metadata | Object | Optional additional information |

---
## Enum Definitions

### Category

| Value | Description |
|-------|-------------|
| documentation | README, guides, documentation |
| dataset | Dataset files or dataset links |
| dependency | requirements.txt, package.json, environment.yml |
| execution | Build, install, execution, runtime logs |
| security | Secrets, dangerous commands, permissions |
| performance | Accuracy, benchmarks, latency |
| model | Model weights, checkpoints, model cards |
| configuration | Dockerfile, YAML, config files |
| other | Any evidence that doesn't fit the above categories |

### Status

| Value | Description |
|-------|-------------|
| verified | Evidence supports the claim |
| partially_verified | Evidence exists but is incomplete |
| missing | Required evidence was not found |
| failed | Evidence contradicts the claim |
| warning | Evidence requires manual review |
| not_applicable | Verification does not apply |

### Severity

| Value | Description |
|-------|-------------|
| low | Minimal impact |
| medium | Moderate impact |
| high | Significant impact |
| critical | Critical issue requiring immediate attention |

# Example

```json
{
  "evidence_id": "EV-001",
  "category": "documentation",
  "source": "README.md",
  "check": "Installation instructions exist",
  "status": "verified",
  "confidence": 0.98,
  "severity": "low",
  "reason": "README contains installation and usage instructions.",
  "timestamp": "2026-07-05T18:45:00Z",
  "metadata": {
    "line_count": 132
  }
}
```

---

# Evidence Categories

ReproForge currently supports the following evidence categories.

## Documentation

Examples

- README
- Installation Guide
- Usage Guide
- Architecture Diagram

---

## Dependency

Examples

- requirements.txt
- package.json
- environment.yml
- Dockerfile

---

## Dataset

Examples

- Dataset exists
- Dataset link
- Dataset checksum
- Dataset version

---

## Execution

Examples

- Installation completed
- Build successful
- Tests executed
- Runtime logs

---

## Security

Examples

- Secrets detected
- Dangerous shell commands
- Network calls
- Privileged execution

---

## Performance

Examples

- Accuracy report
- Benchmark results
- Latency measurements
- Resource utilization

---

## Model

Examples

- Model weights
- Model card
- Configuration
- Checkpoints

---

# Evidence Status

Every evidence item should have one status.

| Status | Meaning |
|----------|---------|
| Verified | Evidence supports the claim |
| Failed | Evidence contradicts the claim |
| Missing | Required evidence was not found |
| Warning | Evidence exists but needs manual review |
| Not Applicable | Check does not apply |

---

# Design Principles

Every evidence item should be:

- Traceable
- Explainable
- Reproducible
- Timestamped
- Machine-readable
- Easy to display inside the Reproducibility Passport

---

# Relationship with Passport

Multiple evidence items are collected during verification.

These evidence items are combined by the Scoring Engine to produce:

- Risk Level
- Reproducibility Score
- Credibility Score
- Final Verdict

The Passport never invents conclusions—it summarizes the collected evidence.
