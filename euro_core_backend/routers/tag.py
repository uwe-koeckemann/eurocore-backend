from fastapi import APIRouter

from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from euro_core_backend import helpers
from euro_core_backend.dependencies import get_session
from euro_core_backend.data.tag import TagBase, Tag

router = APIRouter(
    prefix="/tag",
    tags=["Tags"],
    dependencies=[Depends(get_session)],
    responses={404: {"description": "End-point does not exist"}},
)


@router.get("/get/{tag_id}")
def get_tag(*, session: Session = Depends(get_session),
            tag_id: int):
    return helpers.get_by_id(session, tag_id, Tag)


@router.get("/get-by-name/{name}", response_model=Tag)
def get_tag_by_name(*, session: Session = Depends(get_session),
                    name: str):
    return helpers.get_by_name(session, name, Tag)


@router.get("/get-all", response_model=List[Tag])
def get_all_tags(*, session: Session = Depends(get_session)):
    results = session.exec(select(Tag))
    return results.all()


@router.post("/create", response_model=Tag)
def create_tag(*, session: Session = Depends(get_session),
               tag: TagBase):
    return helpers.create(session, tag, Tag)

@router.put("/update")
def update_tag(*, session: Session = Depends(get_session),
               tag: Tag):
    return helpers.update(session, tag, Tag)


@router.delete("/delete/{tag_id}")
def delete_tag(*, session: Session = Depends(get_session),
               tag_id: int):
    return helpers.delete(session, tag_id, Tag)
