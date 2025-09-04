from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, Text
from sqlalchemy.orm import relationship
from connections.db_connection import Base

class BankConnection(Base):
    __tablename__ = "bank_connections"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    provider = Column(String, default="quiltt/finicity")     # namespaced
    connection_id = Column(String, index=True)               # Quiltt connection identifier
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    raw = Column(Text)                                       # JSON string for provider payloads

    merchant = relationship("MerchantDB", back_populates="bank_connections")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    connection_id = Column(String, ForeignKey("bank_connections.id"), index=True, nullable=False)
    provider_account_id = Column(String, index=True)
    name = Column(String)
    mask = Column(String)
    type = Column(String)
    subtype = Column(String)
    currency = Column(String, default="USD")
    current_balance = Column(Float)
    available_balance = Column(Float)
    institution_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    account_id = Column(String, ForeignKey("bank_accounts.id"), index=True, nullable=False)
    provider_txn_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String, default="USD")
    posted_at = Column(DateTime, index=True)
    description = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
