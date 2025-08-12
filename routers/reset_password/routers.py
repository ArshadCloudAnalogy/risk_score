from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.schema import ResetPasswordResponse, ResetPasswordRequest
from services.reset_password.services import ResetPasswordService

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/reset-password", response_model=ResetPasswordResponse)
def forgot_password(payload: ResetPasswordRequest, db_session: Session = Depends(get_db)):
    return ResetPasswordService.reset_password(payload, db_session)
