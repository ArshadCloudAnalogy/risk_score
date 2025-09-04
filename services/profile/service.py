from models.models import User
from models.schema import UserResponse, ProfessionalDetailsResponse


class ProfileService:

    @staticmethod
    def me(user: User):
        merchant = user.merchant[0] if user.merchant else None
        print(user.merchant)
        professional_details = None
        if merchant:
            professional_details = ProfessionalDetailsResponse(
                company=merchant.business_name,     
                department=merchant.industry,       
                join_date=merchant.created_at,      
                bio=user.bio                        
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
            professional_details=professional_details
        )

