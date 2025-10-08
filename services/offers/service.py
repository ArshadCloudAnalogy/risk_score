from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User
from models.models import Offer
from uuid import uuid4
from models.schema import OfferRequestDAO, OfferRequestModelDAO


class OfferService:

    @staticmethod
    async def build_and_create(offer: OfferRequestDAO, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")

        dao = OfferRequestModelDAO(
            offer_name=offer.offer_name,
            offer_ends=offer.offer_ends,
            offer_starts=offer.offer_starts,
            discount_percent=offer.discount_percent,
            plan_id=offer.plan_id,
            coupon_id=str(uuid4))
        create_offer = await OfferService.create(offer=dao, db_session=db_session)
        if not create_offer:
            raise HTTPException(status_code=404, detail="Error while adding new offer")
        raise HTTPException(status_code=201, detail="Successfully added new offer.")

    @staticmethod
    async def create(offer: OfferRequestModelDAO, db_session: Session):
        offers = Offer(**offer.model_dump())
        db_session.add(offers)
        db_session.commit()
        return offers

    @staticmethod
    async def get(db_session: Session):
        all_offers = db_session.query(Offer).all()
        return all_offers
