from pydantic import BaseModel

from backend.internal.passport import AMDProofMode, CreditStatus


class AmdProof(BaseModel):
    mode: AMDProofMode
    credit_status: CreditStatus
    runtime_target: str
