from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import SignUpRequest, SignUpResponse, MerchantOnboardRequest
from services.sign_up.services import SignUpService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest, db_session: Session = Depends(get_db)):
    return SignUpService.register_user(payload, db_session)


@router.post("/add/merchant")
async def add_merchant(payload: MerchantOnboardRequest, db_session: Session = Depends(get_db),
                 user: User = Depends(current_user)):
    return SignUpService.add_merchant(payload, user, db_session)
