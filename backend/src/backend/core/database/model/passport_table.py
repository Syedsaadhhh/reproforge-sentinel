from datetime import datetime
from typing import List

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from backend.core.database.model.evidence_table import EvidenceTable
from backend.core.database.model.link_tables import PassportEvidenceLink
from backend.core.database.model.log_table import LogTable
from backend.core.database.model.risk_indicator_table import RiskIndicatorTable
from backend.internal.passport import CreditStatus
from backend.internal.passport.enum import AMDProofMode, RiskLevel, Verdict


class PassportTable(SQLModel, table=True):
    # Passport Metadata
    passport_id: str = Field(primary_key=True, min_length=1)
    passport_version: str = Field(nullable=False, min_length=1)
    generated_at: datetime = Field(nullable=False)
    verification_engine: str = Field(nullable=False, min_length=1)

    # Claim Information
    project_id: str = Field(index=True, foreign_key="projecttable.id", min_length=1)
    claim_id: str = Field(nullable=False, min_length=1)
    claim_text: str = Field(nullable=False, min_length=1)

    # Verification Result
    verdict: Verdict = Field(nullable=False)
    summary: str = Field(nullable=False, min_length=1)

    # Scores
    risk_level: RiskLevel = Field(nullable=False)
    risk_score: int = Field(nullable=False, ge=0)
    reproducibility_score: int = Field(nullable=False, ge=0)
    credibility_score: int = Field(nullable=False, ge=0)
    evidence_coverage: int = Field(nullable=False, ge=0)

    # Evidence
    evidence_items: List[EvidenceTable] = Relationship(
        back_populates="passports", link_model=PassportEvidenceLink
    )
    missing_evidence: List[str] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=list,
    )

    risk_indicators: List[RiskIndicatorTable] = Relationship(back_populates="passport")

    logs: List[LogTable] = Relationship(back_populates="passport")

    recommendations: List[str] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=list,
    )

    amd_proof_mode: AMDProofMode
    amd_proof_credit_status: CreditStatus
    amd_proof_runtime_target: str
