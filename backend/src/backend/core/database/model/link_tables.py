from sqlmodel import Field, SQLModel


class PassportEvidenceLink(SQLModel, table=True):
    passport_id: str = Field(
        primary_key=True, foreign_key="passporttable.passport_id", min_length=1
    )
    evidence_id: str = Field(
        primary_key=True, foreign_key="evidencetable.evidence_id", min_length=1
    )
