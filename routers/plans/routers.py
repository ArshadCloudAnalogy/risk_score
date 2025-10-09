from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import PlanRequestDAO
from services.plans.service import PlanService
from services.plans.webhook import PlanWebhook
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Plans API"])


@router.get("/get/plans")
async def get_plans(db_session: Session = Depends(get_db)):
    return await PlanService.get(db_session)


@router.post("/add/plans")
async def add_plans(payload: PlanRequestDAO, db_session: Session = Depends(get_db),
                    user: User = Depends(current_user)):
    return await PlanService.build_and_create(payload, user, db_session)


@router.post("/call/plans/webhook")
async def webhook(request: Request, db_session: Session = Depends(get_db)):
    return await PlanWebhook.webhook_services(request, db_session)
