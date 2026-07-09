from pydantic import BaseModel, ConfigDict


class RiskIndicator(BaseModel):
    model_config = ConfigDict(strict=True)
    indicator: str
    severity: str
    points: int
    reason: str
