from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import OfferRequestDAO
from services.offers.service import OfferService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Offers API"])


@router.post("/add/offers", status_code=status.HTTP_201_CREATED)
async def add_offers(payload: OfferRequestDAO,
                     user: User = Depends(current_user), db_session: Session = Depends(get_db)):
    return await OfferService.build_and_create(payload, user, db_session)


@router.get("/get/offer", status_code=status.HTTP_200_OK)
async def get_offers(db_session: Session = Depends(get_db)):
    return await OfferService.get(db_session)
