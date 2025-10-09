from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User
from models.models import Offer
from models.schema import OfferRequestDAO, OfferRequestModelDAO
import random
import string
from datetime import datetime


class OfferService:

    @staticmethod
    def generate_coupon_id(prefix: str = "F") -> str:
        """
        Generate a random coupon ID in the format: AAAAA-12345-F2025

        Args:
            prefix (str): A single-letter prefix before the year (default: 'F')

        Returns:
            str: The generated coupon ID.
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        numbers = ''.join(random.choices(string.digits, k=5))
        year = datetime.now().year
        coupon_id = f"{letters}-{numbers}-{prefix}{year}"
        return coupon_id

    @staticmethod
    async def build_and_create(offer: OfferRequestDAO, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")

        dao = OfferRequestModelDAO(
            offer_name=offer.offer_name,
            offer_ends=offer.offer_ends,
            offer_description=offer.offer_description,
            offer_starts=offer.offer_starts,
            discount_percent=offer.discount_percent,
            coupon_id=OfferService.generate_coupon_id())
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
