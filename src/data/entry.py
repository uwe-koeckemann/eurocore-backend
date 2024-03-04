from typing import Optional
from sqlmodel import Field, SQLModel


class EntryBase(SQLModel):
    name: str = Field(max_length=100)
    url: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=500)


class Entry(EntryBase, table=True):
    __tablename__ = "entry"
    id: Optional[int] = Field(default=None, primary_key=True)


class EntryUpdate(SQLModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
