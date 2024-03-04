from typing import Optional
from sqlmodel import Field, SQLModel


class RelationTypeBase(SQLModel):
    name: str = Field(max_length=50)
    inverse_name: str = Field(max_length=50)


class RelationType(RelationTypeBase, table=True):
    __tablename__ = "relation_type"
    id: Optional[int] = Field(default=None, primary_key=True)

