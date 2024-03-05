import logging
from typing import Union, List, Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select

from data.entry import EntryBase, Entry, EntryUpdate
from data.tag import TagBase, Tag
from data.relation_type import RelationTypeBase, RelationType
from data.relation import RelationBase, Relation, RelationUpdate
from data.team import Team, TeamBase, TeamUpdate
from data.module import ModuleUsage, ModuleUsageBase, ModuleUsageUpdate

from data.aiod_entry import AiOnDemandOrganization, AiOnDemandPerson

logger = logging.getLogger(__name__)

app = FastAPI()
engine = create_engine("sqlite:///database.db", echo=True)
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
def create_team(team: Team):
    with Session(engine) as session:
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
# Tag
################################################################################
@app.get("/tag/{tag_id}", tags=["Tag"])
def get_tag(tag_id: int):
    with Session(engine) as session:
        results = session.execute(select(Tag).where(Tag.id == tag_id))
        try:
            return results.one()["ModuleUsage"]
        except:
            return {}


@app.get("/tag/get-all", response_model=List[Tag], tags=["Tag"])
def get_all_tags():
    with Session(engine) as session:
        results = session.exec(select(Tag))
        try:
            return results.all()
        except:
            return {}


@app.post("/tag/create", tags=["Tag"])
def create_tag(tag: TagBase):
    with Session(engine) as session:
        new_tag = Tag(name=tag.name)
        session.add(new_tag)
        session.commit()
    return {"POST": new_tag}


@app.put("/tag/update/{tag_id}", tags=["Tag"])
def update_tag(tag_id: int, tag: Tag):
    with Session(engine) as session:
        db_tag = session.get(Tag, tag_id)
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        tag_data = tag.dict(exclude_unset=True)
        for key, value in tag_data.items():
            setattr(db_tag, key, value)
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        return db_tag


@app.delete("/tag/delete/{tag_id}", tags=["Tag"])
def delete_tag(tag_id: int):
    with Session(engine) as session:
        tag = session.exec(select(Tag).where(Tag.id == tag_id)).one()
        # TODO: Only allow for unused tags or delete all usages (maybe split into two end-points)
        session.delete(tag)
        session.commit()
    return {"Deleting tag": tag_id}


# TODO: Replace tag by another everywhere and delete original


################################################################################
# RelationType
################################################################################
@app.get("/relation_type/get_by_id/{relation_type_id}", tags=["Relation Type"])
def get_relation_type(relation_type_id: int):
    with Session(engine) as session:
        results = session.execute(select(RelationType).where(RelationType.id == relation_type_id))
        try:
            return results.one()["RelationType"]
        except:
            return {}


@app.get("/relation_type/get-all", response_model=List[RelationType], tags=["Relation Type"])
def get_all_relation_types():
    with Session(engine) as session:
        results = session.exec(select(RelationType))
        print(results)
        try:
            return results.all()
        except:
            return {}


@app.post("/relation_type/create", tags=["Relation Type"])
def create_relation_type(relation_type: RelationTypeBase):
    with Session(engine) as session:
        new_relation_type = RelationType(
            name=relation_type.name,
            inverse_name=relation_type.inverse_name,
            topic=relation_type.topic,
            inverse_topic=relation_type.inverse_topic,
            description=relation_type.description)
        session.add(new_relation_type)
        session.commit()
    return {"POST": new_relation_type}


@app.put("/relation_type/update/{relation_type_ida}", tags=["Relation Type"])
def update_relation_type(relation_type_ida: int, relation_type: RelationType):
    with Session(engine) as session:
        db_relation_type = session.get(RelationType, relation_type_ida)
        if not db_relation_type:
            raise HTTPException(status_code=404, detail="relation_type not found")
        relation_type_data = relation_type.dict(exclude_unset=True)
        for key, value in relation_type_data.items():
            setattr(db_relation_type, key, value)
        session.add(db_relation_type)
        session.commit()
        session.refresh(db_relation_type)
        return db_relation_type


@app.delete("/relation_type/delete/{relation_type_idb}", tags=["Relation Type"])
def delete_module_usage(relation_type_idb: int):
    with Session(engine) as session:
        relation_type = session.exec(select(RelationType).where(RelationType.id == relation_type_idb)).one()
        # TODO: Only allow for unused relation_types
        session.delete(relation_type)
        session.commit()
    return {"Deleting relation_type": relation_type_idb}


# TODO: Replace relation_type by another everywhere and delete original

################################################################################
# Entry
################################################################################
@app.get("/entry/{entry_id}", tags=["Entry"])
def get_entry(entry_id: int):
    with Session(engine) as session:
        results = session.execute(select(Entry).where(Entry.id == entry_id))
        try:
            return results.one()["ModuleUsage"]
        except:
            return {}


@app.get("/entry/get-all", response_model=List[Entry], tags=["Entry"])
def get_all_entries():
    with Session(engine) as session:
        results = session.exec(select(Entry))
        try:
            return results.all()
        except:
            return {}


@app.post("/entry/create", tags=["Entry"])
def create_entry(entry: Entry):
    with Session(engine) as session:
        tags = []
        for in_tag in entry.tags:

            tag = session.exec(select(Tag).where(Tag.name == in_tag.name)).first()
            logger.info(f"{in_tag}")
            logger.info(f"{tag}")
            logger.info(f"{type(tag)}")
            tags.append(tag)

        new_entry = Entry(
            name=entry.name,
            url=entry.url,
            description=entry.description,
            tags=[]
        )
        session.add(new_entry)
        session.commit()
    return {"POST": new_entry}


@app.put("/entry/update/{entry_id}", tags=["Entry"])
def update_entry(entry_id: int, entry: Entry):
    with Session(engine) as session:
        db_entry = session.get(Entry, entry_id)
        if not db_entry:
            raise HTTPException(status_code=404, detail="entry not found")
        entry_data = entry.dict(exclude_unset=True)
        for key, value in entry_data.items():
            setattr(db_entry, key, value)
        session.add(db_entry)
        session.commit()
        session.refresh(db_entry)
        return db_entry


@app.delete("/entry/delete/{entry_id}", tags=["Entry"])
def delete_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.exec(select(Entry).where(Entry.id == entry_id)).one()
        # TODO: Only allow for unlinked entries or also delete all links
        session.delete(entry)
        session.commit()
    return {"Deleting entry": entry_id}


################################################################################
# Relation
################################################################################
@app.get("/relation/{relation_id}", tags=["Relation"])
def get_relation(relation_id: int):
    with Session(engine) as session:
        results = session.execute(select(Relation).where(Relation.id == relation_id))
        try:
            return results.one()["ModuleUsage"]
        except:
            return {}


@app.get("/relation/get-all", response_model=List[Relation], tags=["Relation"])
def get_all_entries():
    with Session(engine) as session:
        results = session.exec(select(Relation))
        try:
            return results.all()
        except:
            return {}


@app.put("/relation/update/{relation_id}", tags=["Relation"])
def update_relation(relation_id: int, relation: Relation):
    with Session(engine) as session:
        db_relation = session.get(Relation, relation_id)
        if not db_relation:
            raise HTTPException(status_code=404, detail="relation not found")
        relation_data = relation.dict(exclude_unset=True)
        for key, value in relation_data.items():
            setattr(db_relation, key, value)
        session.add(db_relation)
        session.commit()
        session.refresh(db_relation)
        return db_relation


@app.delete("/relation/delete/{relation_id}", tags=["Relation"])
def delete_relation(relation_id: int):
    with Session(engine) as session:
        relation = session.exec(select(Relation).where(Relation.id == relation_id)).one()
        # TODO: Only allow for unlinked entries or also delete all links
        session.delete(relation)
        session.commit()
    return {"Deleting relation": relation_id}
