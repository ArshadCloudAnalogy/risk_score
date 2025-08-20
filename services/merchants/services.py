from models.schema import (
    MerchantProfileDAO,
    ScoreSummary, MerchantResponseDAO,
)
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import MerchantDB, User
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException, status
from utils.merchant.common import _as_list, _to_score_summary_list


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
            legal_entity=merchant.legal_entity,
            industry=merchant.industry,
            business_name=merchant.business_name,
            owner_name=merchant.owner_name,
            mid=merchant.mid,
            bin=merchant.bin,
            mcc=merchant.mcc,
            ein=merchant.ein,
            website=merchant.website,
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
        merchants: List[MerchantDB] = (
            db_session.query(MerchantDB)
            .options(
                joinedload(MerchantDB.profile),
                selectinload(MerchantDB.scores),
            )
            .filter(MerchantDB.user_id == user.id)
            .order_by(MerchantDB.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        # Prefer returning [] rather than 404 for list endpoints
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
                    legal_entity=m.legal_entity,
                    industry=m.industry,
                    business_name=m.business_name,
                    owner_name=m.owner_name,
                    mid=m.mid,
                    bin=m.bin,
                    mcc=m.mcc,
                    ein=m.ein,
                    website=m.website,
                    profile=(
                        MerchantProfileDAO.model_validate(m.profile)
                        if m.profile
                        else None
                    ),
                    latest_score=latest,
                )
            )
        return resp
