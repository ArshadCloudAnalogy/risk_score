from sqlalchemy.orm import Session
from models.models import User
from models.schema import ResetPasswordRequest, ResetPasswordResponse
from fastapi import HTTPException
from passlib.hash import bcrypt
from datetime import datetime


class ResetPasswordService:
    @staticmethod
    def reset_password(payload: ResetPasswordRequest, db_session: Session):
        try:
            user = db_session.query(User).filter(User.reset_token == payload.reset_token).first()
            if not user:
                raise HTTPException(status_code=404, detail="Invalid reset token")

            if not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
                raise HTTPException(status_code=400, detail="Reset token expired")
            user.password = bcrypt.hash(payload.new_password)

            user.reset_token = None
            user.reset_token_expiry = None

            db_session.commit()
            return ResetPasswordResponse(message="Password has been reset successfully")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong.")
