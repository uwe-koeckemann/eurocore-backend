from typing import Optional
from sqlmodel import Field, SQLModel


class AiOnDemandAsset(SQLModel, table=True):
    __tablename__ = "aiod_asset"
    asset_id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int


class AiOnDemandPerson(SQLModel, table=True):
    __tablename__ = "aiod_person"
    person_id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int


class AiOnDemandOrganization(SQLModel, table=True):
    __tablename__ = "aiod_organization"
    org_id: Optional[int] = Field(default=None, primary_key=True)
    aiod_id: int
