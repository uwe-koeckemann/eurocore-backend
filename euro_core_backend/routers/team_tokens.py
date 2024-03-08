from fastapi import APIRouter

from typing import List
from fastapi import Depends
from sqlmodel import Session, select

from euro_core_backend import helpers
from euro_core_backend.dependencies import get_session
from euro_core_backend.data.team_tokens import TeamTokens

router = APIRouter(
    prefix="/team-tokens",
    tags=["Team Tokens"],
    dependencies=[Depends(get_session)],
    responses={404: {"description": "End-point does not exist"}},
)


@router.get("/get/{team_id}")
def get_team(*, session: Session = Depends(get_session),
             team_id: int):
    return helpers.get_by_id(session, team_id, TeamTokens)


@router.get("/get-all", response_model=List[TeamTokens])
def get_all_teams(*, session: Session = Depends(get_session)):
    return session.exec(select(TeamTokens)).all()


@router.post("/create", response_model=TeamTokens)
def create_team(*, session: Session = Depends(get_session),
                team: TeamTokens):
    return helpers.create(session, team, TeamTokens)


@router.put("/update")
def update_team(*, session: Session = Depends(get_session),
                team: TeamTokens):
    return helpers.update(session, team, TeamTokens)


@router.delete("/delete/{team_id}")
def delete_team(*, session: Session = Depends(get_session),
                team_id: int):
    return helpers.delete(session, team_id, TeamTokens)
