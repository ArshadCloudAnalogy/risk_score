from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from models.models import User
from models.schema import ProductRequestDAO, ProductResponseDAO
from services.products.service import ProductService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Products API"])


@router.get("/get/products")
async def get_products(db_session: Session = Depends(get_db)):
    return await ProductService.get(db_session)


@router.get("/get/product/{product_id}")
async def get_product(product_id: str, db_session: Session = Depends(get_db)):
    return await ProductService.get_by_id(product_id, db_session)


@router.delete("/delete/product/{product_id}")
async def delete_product(product_id: str, db_session: Session = Depends(get_db)):
    return await ProductService.delete_by_id(product_id, db_session)


@router.post("/add/products", response_model=ProductResponseDAO)
async def add_products(payload: ProductRequestDAO, db_session: Session = Depends(get_db),
                       user: User = Depends(current_user)):
    return await ProductService.build_and_create(payload, user, db_session)
