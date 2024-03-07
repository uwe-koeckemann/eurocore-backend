from fastapi import APIRouter

from typing import List
from fastapi import Depends
from sqlmodel import Session, select

from euro_core_backend import helpers
from euro_core_backend.data.relation import Relation
from euro_core_backend.dependencies import get_session

router = APIRouter(
    prefix="/relation",
    tags=["Relations"],
    dependencies=[Depends(get_session)],
    responses={404: {"description": "End-point does not exist"}},
)


@router.get("/get-by-type", response_model=List[Relation])
def get_by_type(*, session: Session = Depends(get_session),
                relation_type_id: int) -> List[Relation]:
    return session.exec(select(Relation).where(Relation.relation_type_id == relation_type_id)).all()


@router.get("/get-outgoing", response_model=List[Relation])
def get_by_type(*, session: Session = Depends(get_session),
                source_entry_id: int) -> List[Relation]:
    return session.exec(select(Relation).where(Relation.from_id == source_entry_id)).all()


@router.get("/get-incoming", response_model=List[Relation])
def get_by_type(*, session: Session = Depends(get_session),
                target_entry_id: int) -> List[Relation]:
    return session.exec(select(Relation).where(Relation.to_id == target_entry_id)).all()


@router.post("/create", response_model=Relation)
def create_tag(*, session: Session = Depends(get_session),
               relation: Relation):
    return helpers.create(session, relation, Relation)


@router.delete("/delete")
def delete_relation(*, session: Session = Depends(get_session),
                    relation: Relation):
    db_data = Relation.model_validate(relation)
    session.delete(db_data)
    session.commit()
    return db_data
