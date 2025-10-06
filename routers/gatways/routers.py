from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from models.models import User
from connections.db_connection import get_db
from models.schema import GatewayRequestDAO
from services.gateways.services import GatewayService
from utils.authentication import current_user

router = APIRouter(prefix="/api/v1", tags=["Gateways API"])


@router.post("/add/gateway", status_code=status.HTTP_201_CREATED)
async def add_gateways(payload: GatewayRequestDAO,
                       user: User = Depends(current_user),
                       db_session: Session = Depends(get_db)):
    return await GatewayService.build_and_create(payload, user, db_session)


@router.get("/list/gateway", status_code=status.HTTP_200_OK)
async def get_gateways(db_session: Session = Depends(get_db)):
    return GatewayService.get(db_session, to_dao=True)


@router.delete("/delete/gateway/{gateway_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gateways(gateway_id: str, user: User = Depends(current_user), db_session: Session = Depends(get_db)):
    return await GatewayService.delete(gateway_id, user, db_session)


@router.patch("/update/gateway/{gateway_id}", status_code=status.HTTP_200_OK)
async def update_gateway(gateway_id: str, user: User = Depends(current_user), db_session: Session = Depends(get_db)):
    return await GatewayService.update(gateway_id, user, db_session)
