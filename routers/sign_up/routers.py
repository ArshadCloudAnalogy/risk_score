from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.schema import SignUpRequest, SignUpResponse
from services.sign_up.services import SignUpService

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest, db_session: Session = Depends(get_db)):
    return SignUpService.register_user(payload, db_session)
