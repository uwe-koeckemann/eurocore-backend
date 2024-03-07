import logging
from contextlib import asynccontextmanager
from typing import Union, List, Optional

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Field, SQLModel, Session, create_engine, select

from euro_core_backend.data.relation_type import RelationTypeBase, RelationType
from euro_core_backend.data.relation import Relation
from euro_core_backend.data.team import Team, TeamBase, TeamUpdate
from euro_core_backend.data.module import ModuleUsage, ModuleUsageBase, ModuleUsageUpdate
from euro_core_backend.data.entry_tag_link import EntryTagLink
from euro_core_backend.data.aiod_entry import AiOnDemandAsset, AiOnDemandPerson, AiOnDemandOrganization
from euro_core_backend.routers import tag, entry, relation_type, relation

from euro_core_backend.dependencies import get_session, engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


app = FastAPI(
    dependencies=[Depends(get_session)],
    lifespan=lifespan

)
app.include_router(tag.router)
app.include_router(entry.router)
app.include_router(relation_type.router)
app.include_router(relation.router)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


################################################################################
# Teams
################################################################################
@app.get("/team/get-by-id/{team_id}", tags=["Teams"])
def get_team(team_id):
    with Session(engine) as session:
        results = session.execute(select(Team).where(Team.id == team_id))
        try:
            return results.one()["Team"]
        except:
            return {}
    return team


@app.get("/team/get-all", response_model=List[Team], tags=["Teams"])
def get_all_teams():
    with Session(engine) as session:
        results = session.exec(select(Team))
        try:
            return results.all()
        except:
            return {}


@app.post("/team/create/team", tags=["Teams"])
def create_team(*,
                session: Session = Depends(get_session),
                team: Team):
    session.add(team)
    session.commit()
    return {"POST": team}


@app.put("/team/update/{team_id}", tags=["Teams"])
def update_team(team_id, team: TeamUpdate):
    with Session(engine) as session:
        db_team = session.get(Team, team_id)
        if not db_team:
            raise HTTPException(status_code=404, detail="Team not found")
        team_data = team.dict(exclude_unset=True)
        for key, value in team_data.items():
            setattr(db_team, key, value)
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        return db_team


@app.delete("/team/delete/{team_id}", tags=["Teams"])
def delete_team(team_id: int):
    with Session(engine) as session:
        team = session.exec(select(Team).where(Team.id == team_id)).one()
        print("TEAM:", team)
        session.delete(team)
        print("DELETED:", team)
        session.commit()
    return {"Deleting team": team_id}


################################################################################
# Module Usage
################################################################################
@app.get("/module_usage/get-by-id/{module_usage_id}", tags=["Module Usages"])
def get_module_usage(module_usage_id):
    with Session(engine) as session:
        results = session.execute(select(ModuleUsage).where(ModuleUsage.id == module_usage_id))
        try:
            return results.one()["ModuleUsage"]
        except:
            return {}

    return module_usage


@app.get("/module_usage/get-all", response_model=List[ModuleUsage], tags=["Module Usages"])
def get_all_module_usages():
    with Session(engine) as session:
        results = session.exec(select(ModuleUsage))
        try:
            return results.all()
        except:
            return {}


@app.post("/module_usage/create", tags=["Module Usages"])
def create_module_usage(module_usage: ModuleUsage):
    with Session(engine) as session:
        session.add(module_usage)
        session.commit()
    return {"POST": module_usage}


@app.put("/module_usage/update/{module_usage_id}", tags=["Module Usages"])
def update_module_usage(module_usage_id, module_usage: ModuleUsageUpdate):
    with Session(engine) as session:
        db_module_usage = session.get(ModuleUsage, module_usage_id)
        if not db_module_usage:
            raise HTTPException(status_code=404, detail="ModuleUsage not found")
        module_usage_data = module_usage.dict(exclude_unset=True)
        for key, value in module_usage_data.items():
            setattr(db_module_usage, key, value)
        session.add(db_module_usage)
        session.commit()
        session.refresh(db_module_usage)
        return db_module_usage


@app.delete("/module_usage/delete/{module_usage_id}", tags=["Module Usages"])
def delete_module_usage(module_usage_id: int):
    with Session(engine) as session:
        module_usage = session.exec(select(ModuleUsage).where(ModuleUsage.id == module_usage_id)).one()
        print("MODULE_USAGE:", module_usage)
        session.delete(module_usage)
        print("DELETED:", module_usage)
        session.commit()
    return {"Deleting module_usage": module_usage_id}



################################################################################
# Relation
################################################################################
