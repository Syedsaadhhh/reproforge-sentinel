from datetime import datetime
from typing import List

from backend.internal.passport import RiskLevel, Verdict
from backend.internal.passport.model.amd_proof import AMDProof
from backend.internal.passport.model.evidence_item import EvidenceItem
from backend.internal.passport.model.log_detail import LogDetail
from backend.internal.passport.model.risk_indicator import RiskIndicator
from pydantic import BaseModel, ConfigDict


class PassportOut(BaseModel):
    model_config = ConfigDict(strict=True)
    # Passport Metadata
    passport_id: str
    passport_version: str
    generated_at: datetime
    verification_engine: str

    # Claim Information
    project_id: str
    claim_id: str
    claim_text: str

    # Verification Result
    verdict: Verdict
    summary: str

    # Scores
    risk_level: RiskLevel
    risk_score: int
    reproducibility_score: int
    credibility_score: int
    evidence_coverage: int

    # Evidence
    evidence_items: List[EvidenceItem]
    missing_evidence: List[str]

    risk_indicators: List[RiskIndicator]

    logs: List[LogDetail]

    recommendations: List[str]

    amd_proof: AMDProof


class PassportIn(PassportOut):
    pass
