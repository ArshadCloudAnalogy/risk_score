from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.schema import SignInRequest, SignInResponse
from connections.db_connection import get_db
from services.sign_in.services import SignInService

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/signin", response_model=SignInResponse)
def signin(payload: SignInRequest, db: Session = Depends(get_db)):
    return SignInService.login_user(payload, db)
