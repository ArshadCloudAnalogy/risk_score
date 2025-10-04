from alembic.util import status
from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.orm import Session
from typing import List
from models.models import User, Plan, plan_products
from models.schema import PlanRequestDAO


class PlanService:

    @staticmethod
    async def create(product: PlanRequestDAO, db_session: Session):
        product_data = product.dict(exclude={"product_ids"})
        products = Plan(**product_data)
        db_session.add(products)
        db_session.commit()
        return products

    @staticmethod
    async def build(payload: PlanRequestDAO):
        print(PlanRequestDAO(**payload.dict()))
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

        entities = [{"product_id": item, "plan_id": plan.id} for item in payload.product_ids]
        await PlanService.add_prodict_plan(entities, db_session)
        if plan:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"Plan with name: {payload.name} is successfully created")

        return plan

    @staticmethod
    async def is_exist(name: str, db_session: Session):
        return db_session.query(Plan).filter(Plan.name == name).first()

    @staticmethod
    async def add_prodict_plan(entities: List[dict], db_session: Session):
        stmt = insert(plan_products).values(entities)
        db_session.execute(stmt)
        db_session.commit()
