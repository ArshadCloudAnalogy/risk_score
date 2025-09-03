import os
import jwt
from jwt import PyJWTError
from fastapi import status, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, selectinload

from models.models import User
from connections.db_connection import get_db 

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

ERROR_EMAIL_PASSWORD_IS_INCORRECT = "Please login with the correct email and password."

security = HTTPBearer(auto_error=False)


class AuthService:

    @staticmethod
    def verify_token(token: str) -> str:
        """Decode JWT and return email."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return email
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def verify(token: str, db: Session) -> User:
        """Verify JWT and fetch User with relationships."""
        token = token.split()[-1]  # strip "Bearer "
        email = AuthService.verify_token(token)

        # Eager load merchant (avoid DetachedInstanceError)
        user_instance = (
            db.query(User)
            .options(selectinload(User.merchant))
            .filter(User.email == email)
            .one_or_none()
        )

        if not user_instance:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or token invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_instance


async def current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
) -> User:
    """Return the currently authenticated user."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    user = await AuthService.verify(token=token, db=db)
    return user
