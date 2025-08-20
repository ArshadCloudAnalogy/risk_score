from sqlalchemy.orm import Session
from models.models import User


class MerchantService:

    @staticmethod
    def get_merchant_by_id(merchant_id: str, user: User, db_session: Session):
        ...
