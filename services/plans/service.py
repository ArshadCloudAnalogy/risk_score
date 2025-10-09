from alembic.util import status
from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.orm import Session
from typing import List
from models.models import User, Plan, plan_products, Product
from models.schema import PlanRequestDAO


class PlanService:

    @staticmethod
    async def get(db_session: Session):

        products = [
            {"product_name": product.name, "price": {"price_m": product.price_m, "price_y": product.price_y}} for
            product in db_session.query(Product).all()]
        plans = [{
            "id": plan.id,
            "name": plan.name,
            "recommended": plan.recommended,
            "description": plan.description,
            "no_of_items": plan.no_of_items,
            "is_free": plan.is_free,
            "created_at": plan.created_at,
            "update_at": plan.update_at,
            "products": products
        } for plan in db_session.query(Plan).all()]

        return plans

    @staticmethod
    async def create(product: PlanRequestDAO, db_session: Session):
        product_data = product.dict()
        products = Plan(**product_data)
        db_session.add(products)
        db_session.commit()
        return products

    @staticmethod
    async def build(payload: PlanRequestDAO):
        return PlanRequestDAO(**payload.dict())

    @staticmethod
    async def build_and_create(payload: PlanRequestDAO, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")

        if await PlanService.is_exist(payload.name, db_session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Plan with name: {payload.name} is already present")

        plan = await PlanService.create(product=await PlanService.build(payload=payload),
                                        db_session=db_session)
        if plan:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"Plan with name: {payload.name} is successfully created")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error while creating Plan with name: {payload.name}.")

    @staticmethod
    async def is_exist(name: str, db_session: Session):
        return db_session.query(Plan).filter(Plan.name == name).first()
