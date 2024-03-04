from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship


class TagBase(SQLModel):
    name: str = Field(max_length=50)


class Tag(TagBase, table=True):
    __tablename__ = "tag"
    id: Optional[int] = Field(default=None, primary_key=True)

