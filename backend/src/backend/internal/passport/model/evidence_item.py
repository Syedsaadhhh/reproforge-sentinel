from dataclasses import field
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel

from backend.internal.passport.enum import EvidenceCategory, EvidenceSeverity, EvidenceStatus


class EvidenceItem(BaseModel):
    evidence_id: str
    category: EvidenceCategory
    source: str
    check: str
    status: EvidenceStatus
    confidence: float
    severity: EvidenceSeverity
    reason: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
