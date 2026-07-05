# Evidence Validity

## Overview

Evidence Validity defines how ReproForge Sentinel determines whether collected evidence can be trusted to support or contradict a technical claim.

The purpose of this document is to ensure that every verification result is based on transparent, traceable, and explainable evidence rather than assumptions.

ReproForge is **not** a truth engine. It is an evidence verification system. Therefore, every verdict must be backed by one or more valid evidence items.

---

# What is Evidence?

An evidence item is any verifiable artifact collected during the verification process.

Examples include:

- README.md
- requirements.txt
- Dockerfile
- Dataset
- Model weights
- Evaluation script
- Test results
- Execution logs
- Security scan results
- Dependency information

Each evidence item contributes to the final verification decision.

---

# Evidence Quality Criteria

For evidence to be considered valid, it should satisfy the following principles.

## 1. Traceable

The evidence must identify where it came from.

Examples:

- README.md
- requirements.txt
- execution log
- Docker build output

---

## 2. Verifiable

The evidence should be independently checkable.

Example:

A README stating "95% accuracy" is not enough.

A benchmark report or evaluation script provides verifiable evidence.

---

## 3. Explainable

Every evidence item should include a short explanation describing why it supports or contradicts the claim.

Example:

```
Dataset not found.

The repository references a dataset but does not provide
a download link or source.
```

---

## 4. Reproducible

Another user should be able to perform the same verification and obtain similar results.

---

## 5. Timestamped

Every evidence item should record when it was collected.

This improves transparency and auditability.

---

# Evidence Status

Every collected evidence item is assigned one of the following statuses.

| Status | Meaning |
|---------|---------|
| Verified | Evidence supports the claim. |
| Partially Verified | Evidence exists but is incomplete. |
| Missing | Required evidence could not be found. |
| Failed | Evidence contradicts the claim. |
| Warning | Evidence requires manual review. |
| Not Applicable | The verification step does not apply. |

---

# Confidence Level

Each evidence item includes a confidence score between **0.0** and **1.0**.

Example:

| Confidence | Interpretation |
|------------|----------------|
| 0.90 – 1.00 | Very High Confidence |
| 0.70 – 0.89 | High Confidence |
| 0.40 – 0.69 | Moderate Confidence |
| Below 0.40 | Low Confidence |

The confidence score reflects the reliability of the collected evidence and the certainty of the verification process.

---

# Evidence Lifecycle

Every evidence item follows the same lifecycle.

```
Evidence Discovered
        │
        ▼
Evidence Collected
        │
        ▼
Evidence Validated
        │
        ▼
Evidence Stored
        │
        ▼
Used for Risk Scoring
        │
        ▼
Included in Passport
```

---

# Design Principles

Evidence in ReproForge Sentinel should always be:

- Traceable
- Explainable
- Verifiable
- Reproducible
- Timestamped
- Machine-readable
- Easy to audit

---

# Relationship with the Reproducibility Passport

The Reproducibility Passport does not generate conclusions on its own.

Instead, it summarizes the verified evidence collected during analysis.

Every score, warning, recommendation, and final verdict shown in the Passport must be supported by one or more evidence items.

This ensures that users can understand **what was checked, what was found, what was missing, and why the final verdict was given.**
