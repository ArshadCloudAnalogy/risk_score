from models.schema import SignUpRequest, SignUpResponse, MerchantOnboardRequest, MerchantResponse
from sqlalchemy.orm import Session
from models.models import User, MerchantDB, MerchantProfile
from passlib.hash import bcrypt


class SignUpService:
    @staticmethod
    def register_user(payload: SignUpRequest, db_session: Session) -> SignUpResponse:
        hashed_password = bcrypt.hash(payload.password)
        new_user = User(first_name=payload.first_name, last_name=payload.last_name,
                        email=payload.email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return SignUpResponse(message="User registered successfully", user_id=new_user.id)

    @staticmethod
    def add_merchant(payload: MerchantOnboardRequest, user: User, db_session: Session) -> MerchantResponse:
        merchant = MerchantDB(
            user_id=user.id,
            legal_entity=payload.legal_entity,
            industry=payload.industry,
            mid=payload.mid,
            bin=payload.bin,
            mcc=payload.mcc,
            ein=payload.ein,
            website=payload.website,
        )
        db_session.add(merchant)
        db_session.commit()
        db_session.refresh(merchant)
        merchant_profile = MerchantProfile(
            merchant_id=merchant.id,
            dba=payload.business_profile.dba,
            business_address=payload.business_profile.business_address,
            city=payload.business_profile.city,
            state=payload.business_profile.state,
            zip_code=payload.business_profile.zip_code,
            contact_name=payload.business_profile.contact_name,
            contact_title=payload.business_profile.contact_title,
        )
        db_session.add(merchant_profile)
        db_session.commit()
        db_session.refresh(merchant_profile)
        return MerchantResponse(message="Successfully Added the merchant details",
                                merchant_id=merchant.id,
                                merchant_profile=merchant_profile.id)
