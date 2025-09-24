import base64
from sqlalchemy.orm import Session
from models.models import User
from models.schema import UserResponse, ProfessionalDetailsResponse
from fastapi import UploadFile


class ProfileService:

    @staticmethod
    def me(user: User):
        merchant = user.merchant[0] if user.merchant else None
        professional_details = None
        if merchant:
            professional_details = ProfessionalDetailsResponse(
                company=merchant.business_name,
                department=merchant.industry,
                join_date=merchant.created_at,
                bio=user.bio,
            )

        return UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            location=user.location,
            profile_image=user.profile_image,
            professional_details=professional_details,
        )

    @staticmethod
    async def update_profile(
        db: Session,
        user: User,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        location: str = None,
        bio: str = None,
        profile_image: UploadFile = None,
    ):
        update_fields = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "location": location,
            "bio": bio,
        }
        for field, value in update_fields.items():
            if value not in (None, ""):
                setattr(user, field, value)

        if profile_image:
            image_bytes = await profile_image.read()
            encoded_string = base64.b64encode(image_bytes).decode("utf-8")
            user.profile_image = encoded_string

        if user.merchant:
            merchant = user.merchant[0]
            db.add(merchant)

        db.add(user)
        db.commit()
        db.refresh(user)

        return ProfileService.me(user)
