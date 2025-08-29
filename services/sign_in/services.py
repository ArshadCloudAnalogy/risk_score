import jwt
import datetime
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import User
from models.schema import SignInRequest, SignInResponse
from passlib.hash import bcrypt

class SignInService:
    @staticmethod
    def login_user(payload: SignInRequest, db: Session) -> SignInResponse:
        user = db.query(User).filter(User.email == payload.email).first()

        if not user or not bcrypt.verify(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        payload_data = {
            "user_id": str(user.id),
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        secret_key = os.getenv("JWT_SECRET", "secret_key")
        token = jwt.encode(payload_data, secret_key, algorithm="HS256")

        return SignInResponse(message="Login successful", token=token)
