from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import PlanRequestDAO
from services.merchants.services import MerchantService
from services.plans.service import PlanService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Plans API"])


@router.get("/get/plans")
async def get_plans(merchant_id: str, db_session: Session = Depends(get_db),
                    user: User = Depends(current_user)):
    return MerchantService.get_merchant_by_id(merchant_id, user, db_session)


@router.post("/add/plans")
async def add_plans(payload: PlanRequestDAO, db_session: Session = Depends(get_db),
                    user: User = Depends(current_user)):
    return await PlanService.build_and_create(payload, user, db_session)
