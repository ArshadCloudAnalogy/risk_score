from fastapi import APIRouter
from routers.sign_up.routers import router as signup_router
from routers.sign_in.routers import router as signin_router
from routers.forgot_password.routers import router as forgot_password_router
from routers.reset_password.routers import router as reset_password_router

api_router = APIRouter()
api_router.include_router(signup_router)
api_router.include_router(signin_router)
api_router.include_router(forgot_password_router)
api_router.include_router(reset_password_router)
