from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.core.database.model.passport_table import PassportTable


class RiskIndicatorTable(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    passport_id: str = Field(foreign_key="passporttable.passport_id", nullable=False)
    indicator: str = Field(nullable=False, min_length=1)
    severity: str = Field(nullable=False, min_length=1)
    points: int = Field(nullable=False, ge=0)
    reason: str = Field(nullable=False, min_length=1)

    passport: PassportTable = Relationship(back_populates="risk_indicators")
