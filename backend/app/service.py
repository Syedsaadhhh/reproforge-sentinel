import hashlib
import json
import uuid
from datetime import datetime, timezone

from .amd import collect_amd_proof
from .gemma import explain_evidence
from .models import ClaimInput, LogLine, Passport, RunStatus


RUNS: dict[str, RunStatus] = {}
PASSPORTS: dict[str, Passport] = {}


def _sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, default=str).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _scan(claim: ClaimInput) -> tuple[list[dict], list[str], list[str]]:
    text = f"{claim.claim_text} {claim.repo_url}".lower()
    signals: list[dict] = []
    blocked: list[str] = []
    if any(token in text for token in ("95%", "92.4%", "accuracy", "benchmark", "pass@1")):
        signals.append({
            "id": "sig-metric",
            "severity": "high",
            "label": "Metric requires independent reproduction",
            "detail": "The claim contains a quantitative result but no sealed run result was supplied.",
        })
    if any(token in text for token in ("safe", "production ready", "secure")):
        signals.append({
            "id": "sig-safety",
            "severity": "medium",
            "label": "Broad safety claim",
            "detail": "Safety language requires a declared threat model and policy evidence.",
        })
    if "exec_pipe_deny" in claim.policies:
        blocked.append("shell exec policy: curl|bash and wget|bash")
    missing = ["Independent sealed execution output", "Dataset and seed provenance"]
    return signals, missing, blocked


async def verify(claim: ClaimInput) -> Passport:
    run_id = f"run_{uuid.uuid4().hex[:10]}"
    passport_id = f"pp_{uuid.uuid4().hex[:18]}"
    generated_at = datetime.now(timezone.utc).isoformat()
    RUNS[run_id] = RunStatus(run_id=run_id, status="running", step=0, logs=[])

    signals, missing, blocked = _scan(claim)
    risk = min(0.95, 0.18 + len(signals) * 0.27 + len(blocked) * 0.08)
    reproducibility = max(0.05, 0.82 - len(missing) * 0.19 - len(signals) * 0.12)
    verdict = "partial" if (signals or missing) else "verified"

    gemma = await explain_evidence(claim.claim_text, signals, missing)
    amd = collect_amd_proof()
    fireworks_confirmed = bool(gemma["used"] and gemma["provider"] == "fireworks")
    amd_active = amd["status"] == "LIVE_ROCM_VERIFIED" or fireworks_confirmed
    proof_status = "real" if gemma["used"] else "pending"

    logs = [
        LogLine(t="00:00", line=f"sentinel: accepted claim for {claim.repo_url}", step=0),
        LogLine(t="00:01", line=f"policy-engine: {len(signals)} evidence-risk signals detected", step=1),
        LogLine(t="00:02", line=f"policy: {len(blocked)} action classes blocked", step=2),
        LogLine(t="00:03", line=f"gemma: proof_status={proof_status}", step=3),
        LogLine(t="00:04", line=f"amd: status={amd['status']}", step=4),
        LogLine(t="00:05", line=f"passport: {passport_id} sealed · verdict={verdict}", step=5),
    ]

    evidence = [
        {
            "id": "ev-claim",
            "kind": "artifact",
            "label": "Submitted claim",
            "detail": claim.claim_text,
            "hash": _sha256(claim.claim_text),
        },
        {
            "id": "ev-policy",
            "kind": "log",
            "label": "Policy evaluation",
            "detail": f"{len(blocked)} action classes blocked",
            "hash": _sha256(blocked),
        },
    ]
    if gemma["used"]:
        evidence.append({
            "id": "ev-gemma",
            "kind": "artifact",
            "label": "Gemma inference receipt",
            "detail": f"{gemma['provider']} · {gemma['model']} · {gemma['tokens_used']} tokens",
            "hash": _sha256(gemma),
        })
    if amd["telemetry"].get("available"):
        evidence.append({
            "id": "ev-amd",
            "kind": "artifact",
            "label": "AMD SMI telemetry",
            "detail": amd["telemetry"].get("source", "amd-smi"),
            "hash": _sha256(amd["telemetry"]),
        })

    hashes = {
        "execution_hash": _sha256(logs),
        "environment_hash": _sha256(claim.runtime_target),
        "log_hash": _sha256([log.model_dump() for log in logs]),
    }
    if amd["telemetry"].get("available"):
        hashes["amd_telemetry_hash"] = _sha256(amd["telemetry"])

    passport = Passport(
        passport_id=passport_id,
        run_id=run_id,
        created_at=generated_at,
        claim_text=claim.claim_text,
        repo_url=str(claim.repo_url),
        claim_type=claim.claim_type,
        runtime_target=claim.runtime_target,
        verdict=verdict,
        shadowguard_result={
            "risk_score": risk,
            "reproducibility_score": reproducibility,
            "policy_version": "shadowguard/2026.07-strict",
            "blocked_actions": blocked,
        },
        signals_found=signals,
        evidence_items=evidence,
        missing_evidence=missing,
        gemma_explanation=gemma["text"],
        amd_gemma_proof={
            "gemma_used": gemma["used"],
            "gemma_task": "evidence_narrative" if gemma["used"] else None,
            "gemma_tasks": ["evidence_narrative"] if gemma["used"] else [],
            "model_provider": gemma["provider"],
            "model_name": gemma["model"],
            "runtime_mode": gemma["runtime_mode"],
            "amd_status": "active" if amd_active else "pending",
            "amd_proof_status": amd["status"],
            "proof_status": proof_status,
            "fireworks_confirmed": fireworks_confirmed,
            "run_id": run_id if proof_status == "real" else None,
            "timestamp": generated_at if proof_status == "real" else None,
            "latency_ms": gemma["latency_ms"],
            "tokens_used": gemma["tokens_used"],
            "amd_telemetry": amd["telemetry"],
        },
        hashes=hashes,
        security_notes=[
            "No repository code was executed by this API stage.",
            "Live hardware proof is shown only after a successful provider response or AMD SMI telemetry.",
        ],
    )
    PASSPORTS[run_id] = passport
    RUNS[run_id] = RunStatus(run_id=run_id, status="complete", step=5, logs=logs)
    return passport
