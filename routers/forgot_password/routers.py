from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.schema import ForgotPasswordRequest, ForgotPasswordResponse

from services.forgot_password.services import ForgotPasswordService

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(payload: ForgotPasswordRequest, db_session: Session = Depends(get_db)):
    return ForgotPasswordService.generate_reset_token(payload, db_session)
