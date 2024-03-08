from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class ModuleUsageBase(SQLModel):
    consumer_team_id: int = Field(foreign_key="entry.id")
    module_offer_id: int = Field(foreign_key="module_offer.id")
    bought: bool = Field(default=False)
    bought_support: bool = Field(default=False)
    using: bool = Field(default=False)
    rating: Optional[int] = Field(default=None)
    review: Optional[str] = Field(default=None, max_length=500)


class ModuleUsage(ModuleUsageBase, table=True):
    __tablename__ = "module_usage"
    id: Optional[int] = Field(default=None, primary_key=True)


class ModuleUsageUpdate(SQLModel):
    consumer_team_id: Optional[int] = None
    module_offer_id: Optional[int] = None
    bought: Optional[bool] = None
    bought_support: Optional[bool] = None
    using: Optional[bool] = None
    rating: Optional[int] = Field(default=None)
    review: Optional[str] = Field(default=None)
