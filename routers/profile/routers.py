from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session

from models.models import User
from models.schema import UserResponse
from services.profile.service import ProfileService
from utils.authentication import current_user
from connections.db_connection import get_db  # <-- make sure you already have this in your project

router = APIRouter(prefix="/api/v1", tags=["Profile API"])


@router.get("/user/me", response_model=UserResponse)
async def me(user: User = Depends(current_user)):
    return ProfileService.me(user)


@router.put("/user/edit", response_model=UserResponse)
async def update_me(
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone: str = Form(None),
    location: str = Form(None),
    bio: str = Form(None),
    profile_image: UploadFile = File(None),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return await ProfileService.update_profile(
        db=db,
        user=user,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        location=location,
        bio=bio,
        profile_image=profile_image,
    )
