from fastapi import APIRouter

from typing import List
from fastapi import Depends
from sqlmodel import Session, select

from euro_core_backend import helpers
from euro_core_backend.data.module_offer import ModuleOffer, ModuleOfferBase
from euro_core_backend.dependencies import get_session


router = APIRouter(
    prefix="/module-offer",
    tags=["Module Offers"],
    dependencies=[Depends(get_session)],
    responses={404: {"description": "End-point does not exist"}},
)


@router.get("/get/{offer_id}")
def get_offer(*, session: Session = Depends(get_session),
              offer_id: int):
    return helpers.get_by_id(session, offer_id, ModuleOffer)


@router.get("/get-all", response_model=List[ModuleOffer])
def get_all_offers(*, session: Session = Depends(get_session)):
    return session.exec(select(ModuleOffer)).all()


@router.post("/create", response_model=ModuleOffer)
def create_offer(*, session: Session = Depends(get_session),
                 offer: ModuleOfferBase):
    return helpers.create(session, offer, ModuleOffer)


@router.put("/update")
def update_offer(*, session: Session = Depends(get_session),
                 offer: ModuleOffer):
    return helpers.update(session, offer, ModuleOffer)


@router.delete("/delete/{offer_id}")
def delete_offer(*, session: Session = Depends(get_session),
                 offer_id: int):
    return helpers.delete(session, offer_id, ModuleOffer)
