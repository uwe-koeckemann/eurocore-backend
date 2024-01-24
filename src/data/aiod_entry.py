from typing import Optional
from sqlmodel import Field, SQLModel


class AiOnDemandAsset(SQLModel, table=True):
    __tablename__ = "aiod_asset"
    id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int


class AiOnDemandPerson(SQLModel, table=True):
    __tablename__ = "aiod_person"
    id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int


class AiOnDemandOrganization(SQLModel, table=True):
    __tablename__ = "aiod_organization"
    id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int
