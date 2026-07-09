from backend.core import app_dependency
from backend.core.database import PassportTable
from backend.internal.passport.model import PassportIn


async def get_passport_by_id(passport_id: int):
    async with app_dependency.get_db_session() as session:
        passport_detail = await session.get(PassportTable, passport_id)
    return passport_detail


async def insert_passport(passport_detail: PassportIn):
    async with app_dependency.get_db_session() as session:
        new_passport: PassportTable = PassportTable(
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
            evidence_items=passport_detail.evidence_items,
            missing_evidence=passport_detail.missing_evidence,
            risk_indicators=passport_detail.risk_indicators,
            logs=passport_detail.logs,
            recommendations=passport_detail.recommendations,
            amd_proof_mode=passport_detail.amd_proof.mode,
            amd_proof_credit_status=passport_detail.amd_proof.credit_status,
            amd_proof_runtime_target=passport_detail.amd_proof.runtime_target,
        )

        session.add(new_passport)
        await session.commit()
    return new_passport.passport_id
