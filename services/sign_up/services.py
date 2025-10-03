import json

from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from models.models import MerchantDB, MerchantProfile, ScoreEntry, User
from models.schema import (
    BankBehavior,
    MerchantOnboardRequest,
    MerchantResponse,
    SignUpRequest,
    SignUpResponse,
)
from services.calculation.services import Calculation


class SignUpService:
    @staticmethod
    def register_user(payload: SignUpRequest, db_session: Session) -> SignUpResponse:
        isExist = db_session.query(User).filter(User.email == payload.email).one_or_none()
        if isExist:
            raise HTTPException(detail="You're already register please try login.", status_code=403)
        hashed_password = bcrypt.hash(payload.password)
        new_user = User(first_name=payload.first_name, last_name=payload.last_name,
                        email=payload.email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return SignUpResponse(message="User registered successfully", user_id=new_user.id)

    @staticmethod
    def add_merchant(payload: MerchantOnboardRequest, user: User,
                     db_session: Session) -> MerchantResponse | HTTPException:

        merchant = db_session.query(MerchantDB).filter(
            MerchantDB.business_name == payload.business_profile.business_name,
            MerchantDB.industry == payload.industry).one_or_none()
        if merchant:
            return MerchantResponse(message="Merchant exists",
                                    merchant_id=merchant.id,
                                    merchant_profile=merchant.profile.id)
        merchant = MerchantDB(
            user_id=user.id,
            business_name=payload.business_profile.business_name,
            type_of_merchant=payload.type_of_merchant,
            owner_name=payload.business_profile.owner_name,
            legal_entity=payload.legal_entity,
            industry=payload.industry,
            mid=payload.mid,
            bin=payload.bin,
            mcc=payload.mcc,
            ein=payload.ein,
            website=payload.website,
        )

        # Gates
        g1 = Calculation.gate_age_income(bool(payload.self_employed), float(payload.annual_income or 0),
                                         payload.verified_income)
        g2 = Calculation.gate_identity_fraud(float(payload.device_risk_score or 0), float(payload.fraud_score or 0))
        g3 = Calculation.gate_creditworthiness(payload.fico_score)
        bb = BankBehavior(**(payload.bank_behaviour.dict() if payload.bank_behaviour else {}))
        g4 = Calculation.gate_bank_behaviour(bb)
        ind_pts, ind_tags, heat = Calculation.industry_rules(payload.industry, payload.keywords)

        result = Calculation.combine_gates(g1, g2, g3, g4, ind_pts, ind_tags)

        result["limit_suggestion"] = "$3,000" if result["tier"] == "Warm" else "$5,000" if result["tier"] == "Hot" else "$0"
        db_session.add(merchant)
        db_session.commit()
        db_session.refresh(merchant)

        snap = ScoreEntry(
            merchant_id=merchant.id,
            score=result["score"],
            tier=result["tier"],
            decision=result["decision"],
            limit_suggestion=result["limit_suggestion"],
            risk_tags=json.dumps(result["risk_tags"]),
            explanation=json.dumps(result["explanation"]),
            heat_score=heat,
        )
        db_session.add(snap)
        db_session.commit()

        merchant_profile = MerchantProfile(
            merchant_id=merchant.id,
            dba=payload.business_profile.dba,
            type_of_merchant=payload.type_of_merchant,
            business_address=payload.business_profile.business_address,
            city=payload.business_profile.city,
            state=payload.business_profile.state,
            zip_code=payload.business_profile.zip_code,
            contact_name=payload.business_profile.contact_name,
            contact_title=payload.business_profile.contact_title,
        )
        db_session.add(merchant_profile)
        db_session.commit()

        # after creating merchant_profile and committing...
        # create signatories, ibo_entity, merchant_accounts and documents if present

        if payload.signatories:
            _create_or_update_signatories(db_session, merchant, payload.signatories)

        if payload.ibo_entity:
            _create_or_update_ibo(db_session, merchant, payload.ibo_entity)

        if payload.merchant_accounts:
            _create_or_update_merchant_accounts(db_session, merchant, payload.merchant_accounts)

        # handle generic documents list (list of URLs/paths)
        if payload.documents:
            for doc_url in payload.documents:
                md = MerchantDocument(merchant_id=merchant.id, doc_type="misc", file_path=doc_url)
                db_session.add(md)

        db_session.commit()
        db_session.refresh(merchant)


        db_session.refresh(merchant_profile)
        return MerchantResponse(message="Successfully Added the merchant details",
                                merchant_id=merchant.id,
                                merchant_profile=merchant_profile.id)

    @staticmethod
    def register_root(payload: SignUpRequest, db_session: Session) -> SignUpResponse:
        is_user = db_session.query(User).filter_by(role="super_admin").first()
        if is_user:
            raise HTTPException(status_code=403, detail="You are already a super admin")

        hashed_password = bcrypt.hash(payload.password)
        new_user = User(first_name=payload.first_name, last_name=payload.last_name,
                        email=payload.email, password=hashed_password, role="super_admin")
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return SignUpResponse(message="User registered successfully", user_id=new_user.id)

    @staticmethod
    def register_admin(payload: SignUpRequest, user: User, db_session: Session) -> SignUpResponse:

        if user.role != "super_admin":
            raise HTTPException(status_code=403, detail="You are not a super admin")

        hashed_password = bcrypt.hash(payload.password)
        new_user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=hashed_password,
            role="admin",
            created_by=user.id   # <-- track creator
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return SignUpResponse(message="User registered successfully", user_id=new_user.id)
