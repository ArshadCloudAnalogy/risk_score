from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.schema import SignUpRequest, SignUpResponse
from services.sign_up.services import SignUpService
from models.models import User
from utils.authentication import current_user
from typing import List
from models.schema import UserResponse

router = APIRouter(prefix="/api/v1", tags=["User API"])


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest, db_session: Session = Depends(get_db)):
    return SignUpService.register_user(payload, db_session)

@router.post("/signup/admin", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest, db_session: Session = Depends(get_db),
                user: User = Depends(current_user)):

    return SignUpService.register_admin(payload, user, db_session)

@router.post("/signup/root", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED
)
async def signup_root(payload: SignUpRequest, db_session: Session = Depends(get_db)):
    return SignUpService.register_root(payload, db_session)


@router.get("/super-admin/admins", response_model=List[UserResponse])
async def list_admins(db_session: Session = Depends(get_db), user: User = Depends(current_user)):
    if user.role != "super_admin":
        raise HTTPException(status_code=403, detail="You are not authorised to perform this action")
    admins = db_session.query(User).filter(User.created_by == user.id).all()

    return admins
