from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class ClaimInput(BaseModel):
    repo_url: HttpUrl
    claim_text: str = Field(min_length=8, max_length=4000)
    claim_type: str = "benchmark_result"
    runtime_target: str = "linux/x86_64 · ROCm · AMD"
    policies: list[str] = Field(default_factory=list)
    verification_mode: Literal["fast", "deep"] = "deep"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=1000)


class Project(ProjectCreate):
    id: str
    created_at: str


class ClaimCreate(ClaimInput):
    project_id: str


class ClaimRecord(ClaimCreate):
    id: str
    created_at: str


class RunHandle(BaseModel):
    run_id: str
    status: Literal["queued", "running", "complete", "failed"]


class LogLine(BaseModel):
    t: str
    line: str
    step: int


class RunStatus(BaseModel):
    run_id: str
    status: Literal["queued", "running", "complete", "failed"]
    step: int
    logs: list[LogLine]


class RiskSignal(BaseModel):
    id: str
    severity: Literal["low", "medium", "high", "critical"]
    label: str
    detail: str


class EvidenceItem(BaseModel):
    id: str
    kind: Literal["file", "log", "hash", "network", "artifact"]
    label: str
    detail: str
    hash: str | None = None


class ShadowGuardResult(BaseModel):
    risk_score: float
    reproducibility_score: float
    policy_version: str
    blocked_actions: list[str]


class AmdGemmaProof(BaseModel):
    gemma_used: bool
    gemma_task: str | None = None
    gemma_tasks: list[str] = Field(default_factory=list)
    model_provider: str
    model_family: str = "gemma"
    model_name: str | None = None
    runtime_mode: str
    amd_status: Literal["pending", "active"] = "pending"
    amd_proof_status: str
    proof_status: Literal[
        "mock",
        "pending",
        "real",
        "fixture_until_backend",
        "real_api_call",
    ]
    fireworks_confirmed: bool = False
    run_id: str | None = None
    timestamp: str | None = None
    latency_ms: int | None = None
    tokens_used: int | None = None
    amd_telemetry: dict = Field(default_factory=dict)


class Passport(BaseModel):
    passport_id: str
    run_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    claim_text: str
    repo_url: str
    claim_type: str
    runtime_target: str
    verdict: Literal["verified", "unverified", "blocked", "partial"]
    shadowguard_result: ShadowGuardResult
    signals_found: list[RiskSignal]
    evidence_items: list[EvidenceItem]
    missing_evidence: list[str]
    gemma_explanation: str
    amd_gemma_proof: AmdGemmaProof
    hashes: dict[str, str]
    security_notes: list[str]
