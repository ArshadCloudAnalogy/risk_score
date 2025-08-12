from sqlalchemy import Column, String, Integer, Float, DateTime
from connections.db_connection import Base
from datetime import datetime


class MerchantDB(Base):
    __tablename__ = "merchants"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    legal_entity = Column(String)
    industry = Column(String)
    mid = Column(String)
    bin = Column(String)
    mcc = Column(String)
    ein = Column(String)
    website = Column(String)
    # latest snapshot
    score = Column(Integer)
    tier = Column(String)
    decision = Column(String)
    risk_tags = Column(String)  # JSON list as string
    created_at = Column(DateTime, default=datetime.utcnow)


class ScoreEntry(Base):
    __tablename__ = "scores"
    id = Column(String, primary_key=True, index=True)
    merchant_id = Column(String, index=True)
    score = Column(Integer)
    tier = Column(String)
    decision = Column(String)
    explanation = Column(String)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class WebhookLog(Base):
    __tablename__ = "webhook_logs"
    id = Column(String, primary_key=True, index=True)
    merchant_id = Column(String)
    source = Column(String)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    phone = Column(String)


class Chargeback(Base):
    __tablename__ = "chargebacks"
    id = Column(String, primary_key=True, index=True)
    merchant_id = Column(String)
    chargeback_code = Column(String)
    reason = Column(String)
    amount = Column(Float)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
