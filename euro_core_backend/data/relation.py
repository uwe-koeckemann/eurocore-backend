from typing import Optional
from sqlmodel import Field, SQLModel


class Relation(SQLModel, table=True):
    __tablename__ = "relation"
    relation_type_id: Optional[int] = Field(foreign_key="relation_type.id", primary_key=True)
    from_id: Optional[int] = Field(foreign_key="entry.id", primary_key=True)
    to_id: Optional[int] = Field(foreign_key="entry.id", primary_key=True)

