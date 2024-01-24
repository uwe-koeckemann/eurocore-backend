from typing import Optional, List
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from .aiod_entry import AiOnDemandOrganization
from .robot import Robot
# from .module import ModuleUsage
# from .links import TeamRobotLink



class TeamBase(SQLModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=200)
    tokens: int = Field()


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usages: List["ModuleUsage"] = Relationship(back_populates="team")

class TeamUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tokens: Optional[int] = None
    # robots: Optional[List["Robot"]] = None

    
