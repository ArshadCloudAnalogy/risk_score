from sqlalchemy.orm import Session
from models.models import User
from models.schema import ForgotPasswordRequest, ForgotPasswordResponse
from fastapi import HTTPException, status
import secrets
import datetime


class ForgotPasswordService:
    @staticmethod
    def generate_reset_token(payload: ForgotPasswordRequest, db: Session) -> ForgotPasswordResponse:
        user = db.query(User).filter(User.email == payload.email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

        reset_token = secrets.token_urlsafe(32)
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        user.reset_token = reset_token
        user.reset_token_expiry = expiry_time
        db.commit()

        # In real apps: Send this via email/SMS instead
        return ForgotPasswordResponse(
            message="Reset token generated. Please check your email.",
            reset_token=reset_token
        )
