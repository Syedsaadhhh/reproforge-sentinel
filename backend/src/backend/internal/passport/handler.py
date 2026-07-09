from fastapi import APIRouter

from backend.internal.passport.model import ClaimIn, PassportOut, VerificationOutput
from backend.internal.passport.service import get_passport_service, verify_service

passport_router = APIRouter(prefix="/passport", tags=["Passport"])


@passport_router.post("/verify")
async def verify(inputData: ClaimIn) -> VerificationOutput:
    return await verify_service(claimData=inputData)


@passport_router.get("/{id}")
async def get_passport(id: int) -> PassportOut:
    return await get_passport_service(passport_id=id)
