from fastapi import APIRouter
from routers.sign_up.routers import router as signup_router
from routers.sign_in.routers import router as signin_router
from routers.forgot_password.routers import router as forgot_password_router
from routers.reset_password.routers import router as reset_password_router
from routers.merchant.routers import router as merchant_router
from routers.profile.routers import router as profile_routers
from routers.plans.routers import router as plans_routers
from routers.products.routers import router as products_routers

api_router = APIRouter()
api_router.include_router(signup_router)
api_router.include_router(signin_router)
api_router.include_router(forgot_password_router)
api_router.include_router(reset_password_router)
api_router.include_router(profile_routers)
api_router.include_router(plans_routers)
api_router.include_router(products_routers)

# merchants
api_router.include_router(merchant_router)
