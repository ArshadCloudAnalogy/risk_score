from models.schema import (
    MerchantProfileDAO,
    MerchantResponse,
    BankBehavior,
    ScoreSummary, MerchantResponseDAO, UserResponse, UserMerchantResponse, MerchantOnboardRequest, APIResponse
)
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import MerchantDB, MerchantProfile, ScoreEntry, User
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException, status
from utils.merchant.common import _as_list, _to_score_summary_list
from sqlalchemy import inspect
from services.calculation.services import Calculation
import json

class MerchantService:

    @staticmethod
    def get_merchant_by_id(merchant_id: str, user: User, db_session: Session):
        merchant: MerchantDB | None = (
            db_session.query(MerchantDB)
            .options(joinedload(MerchantDB.profile), selectinload(MerchantDB.scores))
            .filter(MerchantDB.id == merchant_id, MerchantDB.user_id == user.id)
            .one_or_none()
        )

        if merchant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found"
            )

        # find latest score by created_at
        latest = None
        if merchant.scores:
            latest_row = max(
                merchant.scores, key=lambda s: s.created_at or datetime.min
            )
            latest = ScoreSummary(
                score=latest_row.score,
                tier=latest_row.tier,
                decision=latest_row.decision,
                limit_suggestion=latest_row.limit_suggestion,
                risk_tags=_as_list(latest_row.risk_tags),
                explanation=latest_row.explanation,
                heat_score=latest_row.heat_score,
                created_at=latest_row.created_at,
            )

        resp = MerchantResponseDAO(
            id=merchant.id,
            legal_entity=merchant.legal_entity,
            industry=merchant.industry,
            business_name=merchant.business_name,
            owner_name=merchant.owner_name,
            mid=merchant.mid,
            bin=merchant.bin,
            mcc=merchant.mcc,
            ein=merchant.ein,
            website=merchant.website,
            user_details=UserResponse.from_orm(user),
            profile=(
                MerchantProfileDAO.model_validate(merchant.profile)
                if merchant.profile
                else None
            ),
            latest_score=latest,
        )
        return resp

    @staticmethod
    def list_merchants_response(db_session, user: User, limit: int = 100, offset: int = 0) -> List[MerchantResponseDAO]:

        if not user.role in ["admin", "super_admin"]:
            raise HTTPException(detail="You are not authorised to perform this action", status_code=401)

        merchants: List[MerchantDB] = (
            db_session.query(MerchantDB)
            .options(
                joinedload(MerchantDB.profile),
                selectinload(MerchantDB.scores),
            )
            .order_by(MerchantDB.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not merchants:
            return []

        resp: List[MerchantResponseDAO] = []
        for m in merchants:
            latest = None
            if m.scores:
                latest_row = max(m.scores, key=lambda s: s.created_at or datetime.min)
                latest = _to_score_summary_list(latest_row)
            resp.append(
                MerchantResponseDAO(
                    id=m.id,
                    legal_entity=m.legal_entity,
                    industry=m.industry,
                    business_name=m.business_name,
                    owner_name=m.owner_name,
                    user_details=UserMerchantResponse.from_orm(m.user),
                    profile=(
                        MerchantProfileDAO.model_validate(m.profile)
                        if m.profile
                        else None
                    ),
                    latest_score=latest,
                )
            )
        return resp

    # @staticmethod
    # def update_merchant(merchant_id: int, payload: MerchantOnboardRequest, user: User, db_session: Session):
    #     merchant = db_session.query(MerchantDB).filter(
    #         MerchantDB.id == merchant_id,
    #         MerchantDB.user_id == user.id 
    #     ).first()
        
    #     if not merchant:
    #         raise HTTPException(status_code=404, detail="Merchant not found")

    #     merchant.legal_entity = payload.legal_entity or merchant.legal_entity
    #     merchant.industry = payload.industry or merchant.industry
    #     merchant.mid = payload.mid or merchant.mid
    #     merchant.bin = payload.bin or merchant.bin
    #     merchant.mcc = payload.mcc or merchant.mcc
    #     merchant.ein = payload.ein or merchant.ein
    #     merchant.website = payload.website or merchant.website
    #     merchant.keywords = payload.keywords or merchant.keywords

    #     profile = db_session.query(MerchantProfile).filter(
    #         MerchantProfile.merchant_id == merchant_id
    #     ).first()
        
    #     if profile and payload.business_profile:
    #         bp = payload.business_profile
    #         profile.dba = bp.dba or profile.dba
    #         profile.owner_name = bp.owner_name or profile.owner_name
    #         profile.business_name = bp.business_name or profile.business_name
    #         profile.business_address = bp.business_address or profile.business_address
    #         profile.city = bp.city or profile.city
    #         profile.state = bp.state or profile.state
    #         profile.zip_code = bp.zip_code or profile.zip_code
    #         profile.contact_name = bp.contact_name or profile.contact_name
    #         profile.contact_title = bp.contact_title or profile.contact_title

    #     if any_field_changed:  # Implement your logic here
    #         g1 = Calculation.gate_age_income(bool(payload.self_employed), float(payload.annual_income or 0),
    #                                         payload.verified_income)
    #         g2 = Calculation.gate_identity_fraud(float(payload.device_risk_score or 0), float(payload.fraud_score or 0))
    #         g3 = Calculation.gate_creditworthiness(payload.fico_score)
    #         bb = BankBehavior(**(payload.bank_behaviour.dict() if payload.bank_behaviour else {}))
    #         g4 = Calculation.gate_bank_behaviour(bb)
    #         ind_pts, ind_tags, heat = Calculation.industry_rules(payload.industry, payload.keywords)

    #         result = Calculation.combine_gates(g1, g2, g3, g4, ind_pts, ind_tags)
    #         result["limit_suggestion"] = "$3,000" if result["tier"] == "Warm" else "$5,000" if result["tier"] == "Hot" else "$0"

    #         # Create new score entry
    #         score_entry = ScoreEntry(
    #             merchant_id=merchant.id,
    #             score=result["score"],
    #             tier=result["tier"],
    #             decision=result["decision"],
    #             limit_suggestion=result["limit_suggestion"],
    #             risk_tags=json.dumps(result["risk_tags"]),
    #             explanation=json.dumps(result["explanation"]),
    #             heat_score=heat,
    #         )
    #         db_session.add(score_entry)

    #     db_session.commit()
    #     db_session.refresh(merchant)

    #     return APIResponse(
    #         message="Merchant updated successfully",
    #         status="success",
    #         data={"merchant_id": merchant_id}
    #     )

    @staticmethod
    def delete_merchant(merchant_id: str, user: User, db_session: Session):
        if user.role not in ["admin", "super_admin"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorised to perform this action"
            )

        merchant: MerchantDB | None = (
            db_session.query(MerchantDB)
            .filter(MerchantDB.id == merchant_id)
            .one_or_none()
        )

        if merchant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )

        db_session.delete(merchant)
        db_session.commit()

        return APIResponse(
            message="Merchant deleted successfully",
            status="success",
            data={"merchant_id": merchant_id}
        )
