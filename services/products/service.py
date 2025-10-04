from alembic.util import status
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.models import User, Product
from models.schema import ProductRequestDAO, ProductResponseDAO


class ProductService:

    @staticmethod
    async def create(product: ProductRequestDAO, db_session: Session):
        products = Product(name=product.name, description=product.description)
        db_session.add(products)
        db_session.commit()
        return products

    @staticmethod
    async def build(payload: ProductRequestDAO):
        return ProductRequestDAO(**payload.dict())

    @staticmethod
    async def build_and_create(payload: ProductRequestDAO, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")

        if await ProductService.is_exist(payload.name, db_session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Product with name: {payload.name} is already present")

        product = await ProductService.create(product=await ProductService.build(payload=payload),
                                              db_session=db_session)

        return ProductResponseDAO.from_orm(product)

    @staticmethod
    async def is_exist(name: str, db_session: Session):
        return db_session.query(Product).filter(Product.name == name).first()

    @staticmethod
    async def get(db_session: Session):
        return db_session.query(Product).all()

    @staticmethod
    async def get_by_id(product_id: str, db_session: Session):
        products = db_session.query(Product).filter(Product.id == product_id).one_or_none()
        if not products:
            return {}
        return products

    @staticmethod
    async def delete_by_id(product_id: str, db_session: Session):
        product = db_session.query(Product).filter(Product.id == product_id).first()
        db_session.delete(product)
        db_session.commit()
        raise HTTPException(status_code=200, detail=f"Successfully deleted the prodict: {product.name}")
