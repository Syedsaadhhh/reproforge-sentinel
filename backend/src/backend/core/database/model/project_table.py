from sqlmodel import Field, SQLModel


class ProjectTable(SQLModel, table=True):
    id: str = Field(primary_key=True, min_length=1)
