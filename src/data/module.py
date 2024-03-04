from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from .team import Team


class ModuleUsageBase(SQLModel):
    bought: bool = Field()
    using: bool = Field()
    base_asset: int = Field(foreign_key="aiod_asset.id")  # link to external AIoD asset


class ModuleUsage(ModuleUsageBase, table=True):
    __tablename__ = "module_usage"
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="usages")


class ModuleUsageUpdate(SQLModel):
    bought: Optional[bool] = None
    using: Optional[bool] = None
    base_asset: Optional[int] = None
    team_id: Optional[int] = None
