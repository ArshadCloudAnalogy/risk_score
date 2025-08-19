from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from connections.db_connection import Base
from datetime import datetime
from uuid import uuid4


class MerchantDB(Base):
    __tablename__ = "merchants"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    legal_entity = Column(String)
    industry = Column(String)
    mid = Column(String)
    bin = Column(String)
    mcc = Column(String)
    ein = Column(String)
    website = Column(String)
    risk_tags = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)

    # Relationships
    scores = relationship("ScoreEntry", back_populates="merchant", cascade="all, delete-orphan")
    user = relationship("User", back_populates="merchant")
    webhooks = relationship("WebhookLog", back_populates="merchant", cascade="all, delete-orphan")
    chargebacks = relationship("Chargeback", back_populates="merchant", cascade="all, delete-orphan")

    # Onboarding form (one-to-one sections)
    profile = relationship("MerchantProfile", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    processor_info = relationship("ProcessorInfo", back_populates="merchant", uselist=False,
                                  cascade="all, delete-orphan")
    pricing_plan = relationship("PricingPlan", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    ach_authorization = relationship("AchAuthorization", back_populates="merchant", uselist=False,
                                     cascade="all, delete-orphan")
    signatures = relationship("Signature", back_populates="merchant", uselist=False, cascade="all, delete-orphan")


class ScoreEntry(Base):
    __tablename__ = "scores"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    score = Column(Integer)
    tier = Column(String)
    decision = Column(String)
    risk_tags = Column(String)
    explanation = Column(String)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="scores")


class WebhookLog(Base):
    __tablename__ = "webhook_logs"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    source = Column(String)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="webhooks")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)
    merchant = relationship("MerchantDB", back_populates="user", cascade="all, delete-orphan")


class Chargeback(Base):
    __tablename__ = "chargebacks"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    chargeback_code = Column(String)
    reason = Column(String)
    amount = Column(Float)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    merchant = relationship("MerchantDB", back_populates="chargebacks")


class MerchantProfile(Base):
    __tablename__ = "merchant_profiles"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    dba = Column(String)
    business_address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    contact_name = Column(String)
    contact_title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="profile")


class ProcessorInfo(Base):
    __tablename__ = "processor_info"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    processor_acquirer = Column(String)
    avg_ticket = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="processor_info")


class PricingPlan(Base):
    __tablename__ = "pricing_plans"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    initial_setup_fee = Column(Float)
    module1_name = Column(String)
    module1_fee = Column(Float)
    module2_name = Column(String)
    module2_fee = Column(Float)
    other_name = Column(String)
    other_fee = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="pricing_plan")


class AchAuthorization(Base):
    __tablename__ = "ach_authorizations"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    bank_name = Column(String)
    routing = Column(String)
    account = Column(String)
    authorized_signer = Column(String)
    signed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="ach_authorization")


class Signature(Base):
    __tablename__ = "signatures"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    merchant_signature = Column(String)
    merchant_signed_at = Column(DateTime)
    company_signature = Column(String)
    company_signed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Merchant
    merchant = relationship("MerchantDB", back_populates="signatures")
