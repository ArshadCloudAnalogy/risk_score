from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import MerchantOnboardRequest
from services.merchants.services import MerchantService
from services.sign_up.services import SignUpService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Merchant API"])


@router.get("/get/merchant")
async def get_merchant(merchant_id: str, db_session: Session = Depends(get_db),
                       user: User = Depends(current_user)):
    return MerchantService.get_merchant_by_id(merchant_id, user, db_session)


@router.post("/add/merchant")
async def add_merchant(payload: MerchantOnboardRequest, db_session: Session = Depends(get_db),
                       user: User = Depends(current_user)):
    return SignUpService.add_merchant(payload, user, db_session)


@router.get("/get/merchants")
async def get_merchants(
        limit: int = Query(100, ge=1, le=500),
        offset: int = Query(0, ge=0),
        user: User = Depends(current_user),
        db=Depends(get_db),
):
    return MerchantService.list_merchants_response(
        db, user, limit=limit, offset=offset
    )
