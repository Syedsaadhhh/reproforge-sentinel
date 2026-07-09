import re
from datetime import datetime
from typing import List, cast

from backend.internal.passport import AMDProofMode, CreditStatus, RiskLevel, Verdict
from backend.internal.passport.model import (
    AMDProof,
    ClaimIn,
    EvidenceItem,
    LogDetail,
    PassportIn,
    PassportOut,
    RiskIndicator,
    VerificationOutput,
)
from backend.internal.passport.repository import get_passport_by_id, insert_passport


async def verify_service(claimData: ClaimIn) -> VerificationOutput:
    claims = _parse_claims(claimData=claimData)
    evidences = _collect_evidence(claims=claims)
    results: List[PassportOut] = [cast(PassportOut, None) for _ in range(len(claims))]
    for index, claim in enumerate(claims):
        risk_level = RiskLevel.LOW
        risk_score = 0
        verdict = Verdict.VERIFIED
        if _is_contain_risky_command(text=claim):
            risk_level = RiskLevel.HIGH
            risk_score = 70
        if _is_contain_perventage_claim(text=claim) and "eval_file" not in evidences:
            verdict = Verdict.PARTIALLY_VERIFIED
        results[index] = PassportOut(
            passport_id="stub",
            passport_version="0.0.1",
            generated_at=datetime.now(),
            verification_engine="reproforge-stub",
            project_id="stub",
            claim_id="stub",
            claim_text=claim,
            verdict=verdict,
            summary="Stub verification result",
            risk_level=risk_level,
            risk_score=risk_score,
            reproducibility_score=0,
            credibility_score=0,
            evidence_coverage=0,
            evidence_items=[],
            missing_evidence=[],
            risk_indicators=[],
            logs=[],
            recommendations=[],
            amd_proof=AMDProof(
                mode=AMDProofMode.MOCK,
                credit_status=CreditStatus.PENDING,
                runtime_target="",
            ),
        )

        await insert_passport(passport_detail=cast(PassportIn, results[index]))
    return VerificationOutput(passports=results)


def _parse_claims(claimData: ClaimIn):
    return claimData.claims


def _is_contain_risky_command(text: str):
    regex = re.compile(
        r"\bsudo\b|\bcurl\b.*?\|\s*(?:bash|sh)\b",
        re.IGNORECASE,
    )
    return bool(regex.search(text))


def _is_contain_perventage_claim(text: str):
    regex = re.compile(
        r"\b(?:100|[1-9]?\d)(?:\.\d+)?%",
        re.IGNORECASE,
    )
    return bool(regex.search(text))


def _collect_evidence(claims: List[str]):
    return []


def _validate_evidence():
    return []


def _scan_risk():
    return []


def _calculate_score():
    return 42.7


async def get_passport_service(passport_id: int) -> PassportOut:
    passport_detail = await get_passport_by_id(passport_id=passport_id)
    if passport_detail is None:
        raise ValueError(f"Passport with id {passport_id} not found")
    return PassportOut(
        passport_id=passport_detail.passport_id,
        passport_version=passport_detail.passport_version,
        generated_at=passport_detail.generated_at,
        verification_engine=passport_detail.verification_engine,
        project_id=passport_detail.project_id,
        claim_id=passport_detail.claim_id,
        claim_text=passport_detail.claim_text,
        verdict=passport_detail.verdict,
        summary=passport_detail.summary,
        risk_level=passport_detail.risk_level,
        risk_score=passport_detail.risk_score,
        reproducibility_score=passport_detail.reproducibility_score,
        credibility_score=passport_detail.credibility_score,
        evidence_coverage=passport_detail.evidence_coverage,
        evidence_items=[
            EvidenceItem(
                evidence_id=tableDetail.evidence_id,
                category=tableDetail.category,
                source=tableDetail.source,
                check=tableDetail.check,
                status=tableDetail.status,
                confidence=tableDetail.confidence,
                severity=tableDetail.severity,
                reason=tableDetail.reason,
                timestamp=tableDetail.timestamp,
                extra_metadata=tableDetail.extra_metadata,
            )
            for tableDetail in passport_detail.evidence_items
        ],
        missing_evidence=passport_detail.missing_evidence,
        risk_indicators=[
            RiskIndicator(
                indicator=indicatorDetail.indicator,
                severity=indicatorDetail.severity,
                points=indicatorDetail.points,
                reason=indicatorDetail.reason,
            )
            for indicatorDetail in passport_detail.risk_indicators
        ],
        logs=[
            LogDetail(step=logDetail.step, status=logDetail.status, output=logDetail.output)
            for logDetail in passport_detail.logs
        ],
        recommendations=passport_detail.recommendations,
        amd_proof=AMDProof(
            mode=passport_detail.amd_proof_mode,
            credit_status=passport_detail.amd_proof_credit_status,
            runtime_target=passport_detail.amd_proof_runtime_target,
        ),
    )
