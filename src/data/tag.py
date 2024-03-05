from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from .entry import Entry
from .entry_tag_link import EntryTagLink


class TagBase(SQLModel):
    name: str = Field(max_length=50, unique=True)


class Tag(TagBase, table=True):
    __tablename__ = "tag"
    id: Optional[int] = Field(default=None, primary_key=True)

    entries: List[Entry] = Relationship(back_populates="tags", link_model=EntryTagLink)
