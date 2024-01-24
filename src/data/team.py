from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from .aiod_entry import AiOnDemandOrganization
from .robot import Robot


class TeamBase(SQLModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=200)
    tokens: int = Field()


class Team(TeamBase, table=True):
    team_id: Optional[int] = Field(default=None, primary_key=True)
    robots: List["Robot"] = Relationship()

class TeamUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tokens: Optional[int] = None
    robots: Optional[List["Robot"]] = None
