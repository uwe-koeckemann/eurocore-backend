from typing import Optional, List
from sqlmodel import Field, SQLModel

from .aiod_entry import AiOnDemandOrganization

class RobotBase(SQLModel):
    name: str = Field(max_length=100)
    url: str = Field(max_length=200)
    manufactured_by: Optional[int] = Field(default=None, foreign_key="aiod_organization.id") 
    tutorial: Optional[str] = None 
    release_year: Optional[int] = None


class Robot(RobotBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class RobotUpdate(SQLModel):
    name: Optional[str] = None
    url: Optional[str] = None
    manufactured_by: Optional[int] = None
    tutorial: Optional[str] = None
    release_year: Optional[int] = None
