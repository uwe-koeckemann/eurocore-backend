from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from .entry_tag_link import EntryTagLink


class EntryBase(SQLModel):
    name: str = Field(max_length=100, unique=True)
    url: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=500)


class Entry(EntryBase, table=True):
    __tablename__ = "entry"
    id: Optional[int] = Field(default=None, primary_key=True)

    tags: List["Tag"] = Relationship(back_populates="entries", link_model=EntryTagLink)


class EntryUpdate(SQLModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
