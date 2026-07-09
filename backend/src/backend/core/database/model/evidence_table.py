from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from backend.core.database.model.link_tables import PassportEvidenceLink
from backend.internal.passport import EvidenceCategory, EvidenceStatus
from backend.internal.passport.enum import EvidenceSeverity

if TYPE_CHECKING:
    from backend.core.database.model.passport_table import PassportTable


class EvidenceTable(SQLModel, table=True):
    evidence_id: str = Field(primary_key=True, min_length=1)
    category: EvidenceCategory = Field(nullable=False)
    source: str = Field(nullable=False, min_length=1)
    check: str = Field(nullable=False, min_length=1)
    status: EvidenceStatus = Field(nullable=False)
    confidence: float = Field(nullable=False, ge=0)
    severity: EvidenceSeverity = Field(nullable=False)
    reason: str = Field(nullable=False)
    timestamp: datetime = Field(nullable=False)
    extra_metadata: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=dict,
    )

    passports: List[PassportTable] = Relationship(
        back_populates="evidence_items", link_model=PassportEvidenceLink
    )
