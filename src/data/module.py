from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

from .aiod_entry import AiOnDemandAsset

class ModuleUsageBase(SQLModel):
    bought: bool = Field(default=None)
    using: bool = Field(default=None)
    base_asset: int = Field(default=None, foreign_key="aiod_asset.asset_id")  # link to external AIoD asset
    
class ModuleUsage(ModuleUsageBase, table=True):
    module_usage_id: Optional[int] = Field(default=None, primary_key=True)

class ModuleUsageUpdate(SQLModel):
    bought: Optional[str] = None
    using: Optional[str] = None
    base_asset: Optional[int] = None
