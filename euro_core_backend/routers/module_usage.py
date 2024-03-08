from fastapi import APIRouter

from typing import List
from fastapi import Depends
from sqlmodel import Session, select

from euro_core_backend import helpers
from euro_core_backend.data.module_usage import ModuleUsage
from euro_core_backend.dependencies import get_session


router = APIRouter(
    prefix="/module-usage",
    tags=["Module Usages"],
    dependencies=[Depends(get_session)],
    responses={404: {"description": "End-point does not exist"}},
)


@router.get("/get/{usage_id}")
def get_usage(*, session: Session = Depends(get_session),
              usage_id: int):
    return helpers.get_by_id(session, usage_id, ModuleUsage)


@router.get("/get-all", response_model=List[ModuleUsage])
def get_all_usages(*, session: Session = Depends(get_session)):
    return session.exec(select(ModuleUsage)).all()


@router.post("/create", response_model=ModuleUsage)
def create_usage(*, session: Session = Depends(get_session),
                 usage: ModuleUsage):
    return helpers.create(session, usage, ModuleUsage)


@router.put("/update")
def update_usage(*, session: Session = Depends(get_session),
                 usage: ModuleUsage):
    return helpers.update(session, usage, ModuleUsage)


@router.delete("/delete/{usage_id}")
def delete_usage(*, session: Session = Depends(get_session),
                 usage_id: int):
    return helpers.delete(session, usage_id, ModuleUsage)
