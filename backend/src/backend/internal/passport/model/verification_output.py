from typing import List

from pydantic import BaseModel, ConfigDict, Field

from backend.internal.passport.model import PassportOut


class VerificationOutput(BaseModel):
    model_config = ConfigDict(strict=True)
    passports: List[PassportOut] = Field(default_factory=list)
