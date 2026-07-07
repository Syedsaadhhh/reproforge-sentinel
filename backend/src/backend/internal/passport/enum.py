from enum import StrEnum, auto


class Verdict(StrEnum):
    VERIFIED = auto()
    PARTIALLY_VERIFIED = auto()
    NOT_VERIFIED = auto()
    HIGH_RISK = auto()
    BLOCKED = auto()


class RiskLevel(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    BLOCKED = auto()


class AMDProofMode(StrEnum):
    MOCK = auto()
    RUNTIME = auto()


class CreditStatus(StrEnum):
    PENDING = auto()
    AVAILABLE = auto()
    COMPLETED = auto()


class EvidenceCategory(StrEnum):
    DOCUMENTATION = auto()
    DATASET = auto()
    DEPENDENCY = auto()
    EXECUTION = auto()
    SECURITY = auto()
    PERFORMANCE = auto()
    MODEL = auto()


class EvidenceStatus(StrEnum):
    VERIFIED = auto()
    PARTIALLY_VERIFIED = auto()
    MISSING = auto()
    FAILED = auto()
    WARNING = auto()
    NOT_APPLICABLE = auto()


class EvidenceSeverity(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()
