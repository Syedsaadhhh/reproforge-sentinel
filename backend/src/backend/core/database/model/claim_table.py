from datetime import datetime

from sqlmodel import Field, SQLModel


class ClaimTable(SQLModel, table=True):
    claim_id: str = Field(primary_key=True, min_length=1)
    project_id: str = Field(foreign_key="projecttable.id", min_length=1)
    claim_text: str = Field(nullable=False, min_length=1)
    created_at: datetime = Field(nullable=False)
