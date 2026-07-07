from pydantic import BaseModel


class RiskIndicator(BaseModel):
    indicator: str
    severity: str
    points: int
    reason: str
