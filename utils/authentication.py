import os
from fastapi import status, HTTPException, Security
from models.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError

from connections.db_connection import SessionLocal

db_session = SessionLocal()

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ERROR_EMAIL_PASSWORD_IS_INCORRECT = "Please login with this correct email and password instead."

security = HTTPBearer(auto_error=False)


class AuthService:

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                return {
                    "errors": ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                    "error_code": 402,
                    "http_error_code": 402
                }
            return email
        except PyJWTError:
            return {
                "errors": ERROR_EMAIL_PASSWORD_IS_INCORRECT,
                "error_code": 402,
                "http_error_code": 402
            }

    @staticmethod
    async def verify(token: str):
        """Given a JWT it finds the current loggedIn session and returns the user id"""
        try:
            token = token.split()[-1]
            email = AuthService.verify_token(token)
            user_instance = db_session.query(User).filter(User.email == email).one_or_none()
            return user_instance
        except Exception as _:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Bearer token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        finally:
            db_session.close()


async def current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    user = await AuthService.verify(token=token)  # will raise 401 if invalid
    return user
