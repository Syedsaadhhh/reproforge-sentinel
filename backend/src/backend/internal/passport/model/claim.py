from typing import List

from pydantic import BaseModel, ConfigDict


class ClaimIn(BaseModel):
    model_config = ConfigDict(strict=True)
    claims: List[str]
