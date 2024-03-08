from sqlmodel import Field, SQLModel


class ModuleOfferBase(SQLModel):
    team_id: int = Field(foreign_key="entry.id")
    module_id: int = Field(foreign_key="entry.id")
    cost: int = Field()
    integration_support: bool = Field(default=False)
    integration_cost: int = Field(default=0)


class ModuleOffer(ModuleOfferBase, table=True):
    __tablename__ = "module_offer"
    id: int = Field(default=None, primary_key=True)
