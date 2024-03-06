from typing import Optional
from sqlmodel import Field, SQLModel


class RelationTypeBase(SQLModel):
    name: str = Field(max_length=50, unique=True)
    inverse_name: str = Field(max_length=50, unique=True)
    topic: str = Field(max_length=50)
    inverse_topic: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)


class RelationType(RelationTypeBase, table=True):
    __tablename__ = "relation_type"
    id: Optional[int] = Field(default=None, primary_key=True)


class RelationTypeUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50)
    inverse_name: Optional[str] = Field(default=None, max_length=50)
    topic: Optional[str] = Field(default=None, max_length=50)
    inverse_topic: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(max_length=200)

