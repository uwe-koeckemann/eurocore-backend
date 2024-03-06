from typing import Optional
from sqlmodel import Field, SQLModel


class EntryTagLink(SQLModel, table=True):
    __tablename__ = "entry_tag_link"
    entry_id: Optional[int] = Field(
        default=None, foreign_key="entry.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
