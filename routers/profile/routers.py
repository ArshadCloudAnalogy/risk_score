from fastapi import APIRouter, Depends
from models.models import User
from services.profile.service import ProfileService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Profile API"])


@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return ProfileService.me(user)
