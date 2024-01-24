from typing import Union, List, Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select

from data.robot import Robot, RobotBase, RobotUpdate
from data.team import Team, TeamBase, TeamUpdate
from data.module import ModuleUsage, ModuleUsageBase, ModuleUsageUpdate


from data.aiod_entry import AiOnDemandOrganization, AiOnDemandPerson


app = FastAPI()
engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)


################################################################################
# Teams
################################################################################
@app.get("/eurocore/team/get-by-id/{team_id}", tags=["Teams"])
def get_team(team_id):
    with Session(engine) as session:
        results = session.execute(select(Team).where(Team.team_id == team_id))
        try:
            return results.one()["Team"]
        except:
            return {}

    return team


@app.get("/eurocore/team/get-all", response_model=List[Team], tags=["Teams"])
def get_all_teams():
    with Session(engine) as session:
        results = session.exec(select(Team))
        try:
            return results.all()
        except:
            return {}


@app.post("/eurocore/team/create/team", tags=["Teams"])
def create_team(team: Team):
    with Session(engine) as session:
        session.add(team)
        session.commit()
    return {"POST": team}


@app.put("/eurocore/team/update/{team_id}", tags=["Teams"])
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


@app.delete("/eurocore/team/delete/{team_id}", tags=["Teams"])
def delete_team(team_id: int):
    with Session(engine) as session:
        team = session.exec(select(Team).where(Team.team_id == team_id)).one()
        print("TEAM:", team)
        session.delete(team)
        print("DELETED:", team)
        session.commit()
    return {"Deleting team": team_id}

################################################################################
# Module Usage
################################################################################
@app.get("/eurocore/module_usage/get-by-id/{module_usage_id}", tags=["Module Usages"])
def get_module_usage(module_usage_id):
    with Session(engine) as session:
        results = session.execute(select(ModuleUsage).where(ModuleUsage.module_usage_id == module_usage_id))
        try:
            return results.one()["ModuleUsage"]
        except:
            return {}

    return module_usage


@app.get("/eurocore/module_usage/get-all", response_model=List[ModuleUsage], tags=["Module Usages"])
def get_all_module_usages():
    with Session(engine) as session:
        results = session.exec(select(ModuleUsage))
        try:
            return results.all()
        except:
            return {}


@app.post("/eurocore/module_usage/create/module_usage", tags=["Module Usages"])
def create_module_usage(module_usage: ModuleUsage):
    with Session(engine) as session:
        session.add(module_usage)
        session.commit()
    return {"POST": module_usage}


@app.put("/eurocore/module_usage/update/{module_usage_id}", tags=["Module Usages"])
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


@app.delete("/eurocore/module_usage/delete/{module_usage_id}", tags=["Module Usages"])
def delete_module_usage(module_usage_id: int):
    with Session(engine) as session:
        module_usage = session.exec(select(ModuleUsage).where(Module_Usage.module_usage_id == module_usage_id)).one()
        print("MODULE_USAGE:", module_usage)
        session.delete(module_usage)
        print("DELETED:", module_usage)
        session.commit()
    return {"Deleting module_usage": module_usage_id}

################################################################################
# Robots
################################################################################
@app.get("/eurocore/robot/get-by-id/{robot_id}", tags=["Robots"])
def get_robot(robot_id):
    with Session(engine) as session:
        results = session.execute(select(Robot).where(Robot.robot_id == robot_id))
        try:
            return results.one()["Robot"]
        except:
            return {}

    return robot


@app.get("/eurocore/robot/get-all", response_model=List[Robot], tags=["Robots"])
def get_all_robots():
    with Session(engine) as session:
        results = session.exec(select(Robot))
        try:
            return results.all()
        except:
            return {}


@app.post("/eurocore/robot/create/robot", tags=["Robots"])
def create_robot(robot: Robot):
    with Session(engine) as session:
        session.add(robot)
        session.commit()
    return {"POST": robot}


@app.put("/eurocore/robot/update/{robot_id}", tags=["Robots"])
def update_robot(robot_id, robot: RobotUpdate):
    with Session(engine) as session:
        db_robot = session.get(Robot, robot_id)
        if not db_robot:
            raise HTTPException(status_code=404, detail="Robot not found")
        robot_data = robot.dict(exclude_unset=True)
        for key, value in robot_data.items():
            setattr(db_robot, key, value)
        session.add(db_robot)
        session.commit()
        session.refresh(db_robot)
        return db_robot


@app.delete("/eurocore/robot/delete/{robot_id}", tags=["Robots"])
def delete_robot(robot_id: int):
    with Session(engine) as session:
        robot = session.exec(select(Robot).where(Robot.robot_id == robot_id)).one()
        print("ROBOT:", robot)
        session.delete(robot)
        print("DELETED:", robot)
        session.commit()
    return {"Deleting robot": robot_id}

