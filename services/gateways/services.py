from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User
from models.models import PaymentGateway
from models.schema import GatewayRequestDAO, GatewayResponseDAO


class GatewayService:

    @staticmethod
    def get(db_session: Session, to_dao: bool = False):
        instance = db_session.query(PaymentGateway).filter(PaymentGateway.status == True).one_or_none()
        if to_dao:
            return GatewayResponseDAO.from_orm(instance)
        return instance

    @staticmethod
    async def create(gateway: GatewayRequestDAO, user: User, db_session: Session):
        gate = PaymentGateway(name=gateway.name,
                              api_key=gateway.api_key,
                              publishable_key=gateway.publishable_key,
                              webhook=gateway.webhook,
                              user_id=user.id,
                              status=True)
        db_session.add(gate)
        db_session.commit()
        return gate

    @staticmethod
    async def build_and_create(payload: GatewayRequestDAO, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")

        gateways = GatewayService.get(db_session)
        gateways.__setattr__('status', False)
        db_session.commit()
        isCreated = await GatewayService.create(payload, user, db_session)
        if not isCreated:
            raise HTTPException(status_code=404, detail="Error while adding new payment gateways")
        raise HTTPException(status_code=201, detail="Successfully added new payment gateway.")

    @staticmethod
    async def delete(gateway_id, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")
        DB_exist = db_session.query(PaymentGateway).filter(PaymentGateway.id == gateway_id).one_or_none()
        if DB_exist.status:
            raise HTTPException(status_code=403, detail="You can't delete the default payment gateway")
        db_session.delete(DB_exist)
        db_session.commit()
        raise HTTPException(status_code=200, detail="Successfully deleted the requested payment gateway")

    @staticmethod
    async def update(gateway_id, user: User, db_session: Session):
        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not authorised to perform this action")
        DB_exist = db_session.query(PaymentGateway).filter(PaymentGateway.id == gateway_id).one_or_none()
        if not DB_exist:
            raise HTTPException(status_code=404, detail="No such payment gateway exists")
        gateways = GatewayService.get(db_session)
        gateways.__setattr__('status', False)
        DB_exist.status = True
        db_session.commit()
        raise HTTPException(status_code=200, detail="Updated the payment gateway")
