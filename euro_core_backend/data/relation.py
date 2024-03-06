from typing import Optional
from sqlmodel import Field, SQLModel


class RelationBase(SQLModel):
    from_id: Optional[int] = Field(foreign_key="entry.id")
    to_id: Optional[int] = Field(foreign_key="entry.id")
    relation_type_id: Optional[int] = Field(foreign_key="relation_type.id")


class Relation(RelationBase, table=True):
    __tablename__ = "relation"
    id: Optional[int] = Field(default=None, primary_key=True)


class RelationUpdate(SQLModel):
    from_id: Optional[int] = Field(default=None, foreign_key="entry.id")
    to_id: Optional[int] = Field(default=None, foreign_key="entry.id")
    relation_type_id: Optional[int] = Field(default=None, foreign_key="relation_type.id")
