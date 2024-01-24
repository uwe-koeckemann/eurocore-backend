from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from .team import Team
from .aiod_entry import AiOnDemandAsset

class ModuleUsageBase(SQLModel):
    bought: bool = Field()
    using: bool = Field()
    base_asset: int = Field(foreign_key="aiod_asset.asset_id")  # link to external AIoD asset
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="usages")
    
class ModuleUsage(ModuleUsageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ModuleUsageUpdate(SQLModel):
    bought: Optional[bool] = None
    using: Optional[bool] = None
    base_asset: Optional[int] = None
    team_id: Optional[int] = None
