from enum import Enum

from sqlalchemy import (
    Column, String, Integer,
    Float, DateTime, ForeignKey, Text)
from sqlalchemy.orm import relationship
from connections.db_connection import Base
from datetime import datetime
from uuid import uuid4


class Role(Enum):
    USER = "user"
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"

class MerchantDB(Base):
    __tablename__ = "merchants"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    legal_entity = Column(String)
    type_of_merchant = Column(String, server_default="moderate", nullable=False)
    industry = Column(String)
    business_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=True)
    mid = Column(String)
    bin = Column(String)
    mcc = Column(String)
    ein = Column(String)
    website = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)

    # Relationships
    scores = relationship("ScoreEntry", back_populates="merchant", cascade="all, delete-orphan")
    user = relationship("User", back_populates="merchant")
    profile = relationship("MerchantProfile", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    processor_info = relationship("ProcessorInfo", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    signatures = relationship("Signature", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    # New relationships
    signatories = relationship("Signatory", back_populates="merchant", cascade="all, delete-orphan")
    ibo_entity = relationship("IboEntity", back_populates="merchant", uselist=False, cascade="all, delete-orphan")
    merchant_accounts = relationship("MerchantAccount", back_populates="merchant", cascade="all, delete-orphan")
    documents = relationship("MerchantDocument", back_populates="merchant", cascade="all, delete-orphan")


class ScoreEntry(Base):
    __tablename__ = "scores"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    score = Column(Integer, nullable=False)
    tier = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    limit_suggestion = Column(String, nullable=True)
    risk_tags = Column(Text, nullable=True)  # JSON string list
    explanation = Column(Text, nullable=True)
    heat_score = Column(Integer, nullable=True)
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
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    role = Column(String, nullable=False, default=Role.USER.value)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)   # <-- NEW FIELD
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
    type_of_merchant = Column(String, server_default="moderate", nullable=False)
    dba = Column(String)
    business_address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    contact_name = Column(String)
    contact_title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("MerchantDB", back_populates="profile")


# --- Signatory (Authorized Representative / Principal) ---
class Signatory(Base):
    __tablename__ = "signatories"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)

    # person details
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    residential_address = Column(String, nullable=True)
    phone_mobile = Column(String, nullable=True)
    phone_business = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ssn_or_national_id = Column(String, nullable=True)

    # uploaded file paths / URLs (store path or s3 url)
    gov_id_front = Column(String, nullable=True)
    gov_id_back = Column(String, nullable=True)

    ownership_percent = Column(Float, nullable=True)
    digital_signature = Column(String, nullable=True)  # path / base64 / e-sign token

    created_at = Column(DateTime, default=datetime.utcnow)
    merchant = relationship("MerchantDB", back_populates="signatories")


# --- IBO Entity (parent organization) ---
class IboEntity(Base):
    __tablename__ = "ibo_entities"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)

    legal_business_name = Column(String, nullable=False)
    dba = Column(String, nullable=True)
    business_type = Column(String, nullable=True)  # LLC, Corp, etc.
    business_address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    ein = Column(String, nullable=True)

    # bank details (optional)
    bank_name = Column(String, nullable=True)
    routing_number = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    account_type = Column(String, nullable=True)

    # kyb documents as references
    articles_of_incorporation = Column(String, nullable=True)
    operating_agreement = Column(String, nullable=True)
    business_license = Column(String, nullable=True)
    proof_of_address = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    merchant = relationship("MerchantDB", back_populates="ibo_entity")


# --- MerchantAccount (MID profile / per-merchant account info) ---
class MerchantAccount(Base):
    __tablename__ = "merchant_accounts"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)

    merchant_legal_name = Column(String, nullable=True)
    dba = Column(String, nullable=True)
    mcc = Column(String, nullable=True)
    processing_type = Column(String, nullable=True)  # E-comm / Retail / MOTO
    average_ticket = Column(Float, nullable=True)
    highest_ticket = Column(Float, nullable=True)
    monthly_processing_volume = Column(Float, nullable=True)
    refund_policy_url = Column(String, nullable=True)
    customer_support_phone = Column(String, nullable=True)
    customer_support_email = Column(String, nullable=True)
    checkout_url = Column(String, nullable=True)
    settlement_bank_name = Column(String, nullable=True)
    settlement_routing_number = Column(String, nullable=True)
    settlement_account_number = Column(String, nullable=True)
    settlement_account_type = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    merchant = relationship("MerchantDB", back_populates="merchant_accounts")


# --- MerchantDocument (generic container for uploaded docs) ---
class MerchantDocument(Base):
    __tablename__ = "merchant_documents"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)

    doc_type = Column(String, nullable=False)  # e.g., 'voided_check', 'kyb', 'refund_policy'
    file_path = Column(String, nullable=False)  # path or URL to file
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("MerchantDB", back_populates="documents")


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

    signer_name = Column(String, nullable=True)
    signed_at = Column(DateTime, nullable=True)
    signature_image = Column(String, nullable=True)  # base64 or path

    merchant = relationship("MerchantDB", back_populates="signatures")
