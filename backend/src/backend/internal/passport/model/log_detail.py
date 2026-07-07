from pydantic import BaseModel


class LogDetail(BaseModel):
    step: str
    status: str
    output: str
