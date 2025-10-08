from enum import Enum

from sqlalchemy import (
    Column, String, Integer,
    Float, DateTime, ForeignKey, Text, Table, Boolean)
from sqlalchemy.dialects.postgresql import TEXT
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
    webhooks = relationship("WebhookLog", back_populates="merchant", cascade="all, delete-orphan")
    chargebacks = relationship("Chargeback", back_populates="merchant", cascade="all, delete-orphan")
    # bank_connections = relationship("BankConnection", back_populates="merchant", cascade="all, delete-orphan")

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
    created_by = Column(String, ForeignKey("users.id"), nullable=True)  # <-- NEW FIELD
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


plan_products = Table("plan_products", Base.metadata,
                      Column("plan_id", String(50), ForeignKey("plans.id"), primary_key=True),
                      Column("product_id", String(50), ForeignKey("products.id"), primary_key=True)
                      )


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))

    name = Column(String(20), nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)

    plans = relationship("Plan", secondary=plan_products, back_populates="products")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String(20), nullable=False)
    description = Column(TEXT, nullable=True)
    minimum_selected = Column(String(5), nullable=False)
    price_m = Column(String(20), nullable=True)
    price_y = Column(String(20), nullable=True)
    no_of_items = Column(String(20), nullable=False)
    is_free = Column(Boolean, nullable=False, default=False)
    duration = Column(DateTime, nullable=True)
    recommended = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", secondary=plan_products, back_populates="plans")
    discount = relationship("Discount", back_populates="plans")


class PaymentGateway(Base):
    __tablename__ = "payment_gateways"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String(15), nullable=False)
    api_key = Column(TEXT, nullable=False)
    publishable_key = Column(TEXT, nullable=False)
    webhook = Column(String(250), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    status = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Offer(Base):
    __tablename__ = "offers"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    coupon_id = Column(String(50), nullable=True)
    offer_name = Column(String(10), nullable=False)
    offer_starts = Column(DateTime, nullable=False)
    offer_ends = Column(DateTime, nullable=False)
    discount_percent = Column(String(10), nullable=False)
    is_applied = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)


class Discount(Base):
    __tablename__ = "discount"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)

    plans = relationship("Plan", back_populates="discount")
