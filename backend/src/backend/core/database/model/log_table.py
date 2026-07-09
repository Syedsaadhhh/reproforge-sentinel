from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.core.database.model.passport_table import PassportTable


class LogTable(SQLModel, table=True):
    id: int = Field(primary_key=True)
    passport_id: str = Field(foreign_key="passporttable.passport_id", min_length=1)
    step: str = Field(nullable=False, min_length=1)
    status: str = Field(nullable=False, min_length=1)
    output: str = Field(nullable=False, min_length=1)

    passport: PassportTable = Relationship(back_populates="logs")
