from models.schema import SignUpRequest, SignUpResponse
from sqlalchemy.orm import Session
from models.models import User
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
