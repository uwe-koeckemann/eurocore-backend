from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from euro_core_backend.data.module_usage import ModuleUsage
from euro_core_backend.data.module_offer import ModuleOffer


class TeamTokens(SQLModel, table=True):
    __tablename__ = "team_tokens"
    id: int = Field(default=None, foreign_key="entry.id", primary_key=True)
    tokens: int = Field(default=0)
