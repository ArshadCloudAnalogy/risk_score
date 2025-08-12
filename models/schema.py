from dataclasses import field
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SignUpRequest(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=6)


class SignUpResponse(BaseModel):
    message: str
    user_id: int


class SignInRequest(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    message: str
    token: str


class ForgotPasswordRequest(BaseModel):
    email: str


class VerifyOTPRequest(BaseModel):
    email: str = None
    otp_code: str = None


class VerifyOTPResponse(BaseModel):
    message: str


class VerifyOTPResponseDAO(BaseModel):
    message: str
    expire_token: str


class ForgotPasswordResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    message: str


class BankBehavior(BaseModel):
    overdrafts_6mo: int = Field(0, ge=0)
    avg_balance: float = Field(0, ge=0)
    nsf_fees: int = Field(0, ge=0)


class ScoreExplanation(BaseModel):
    credit_weight: int
    fraud_penalty: int
    bank_score: int
    industry_risk_penalty: int


class ScoreResponse(BaseModel):
    score: int
    tier: str
    decision: str
    risk_tags: List[str] = field(default_factory=list)
    explanation: ScoreExplanation


class MerchantOnboardRequest(BaseModel):
    name: str
    legal_entity: Optional[str] = None
    industry: str
    mid: Optional[str] = None
    bin: Optional[str] = None
    mcc: Optional[str] = None
    ein: Optional[str] = None
    website: Optional[str] = None
    # minimal signals for initial score (can be enriched later)
    fico_score: Optional[int] = Field(None, ge=300, le=850)
    fraud_score: Optional[float] = Field(0.0, ge=0.0, le=1.0)
    bank_behavior: Optional[BankBehavior] = None
    keywords: List[str] = field(default_factory=list)


class MerchantResponse(BaseModel):
    id: str
    name: str
    industry: str
    mid: Optional[str] = None
    bin: Optional[str] = None
    mcc: Optional[str] = None
    score: Optional[int] = None
    tier: Optional[str] = None
    decision: Optional[str] = None
    risk_tags: List[str] = field(default_factory=list)


class ExperianWebhook(BaseModel):
    merchant_id: str
    alert_type: str
    fraud_score: float
    timestamp: Optional[datetime] = None


class FinicityWebhook(BaseModel):
    merchant_id: str
    overdraft_alert: bool = False
    low_balance: bool = False
    verified_income: Optional[float] = None
    avg_balance: Optional[float] = None
    timestamp: Optional[datetime] = None


class ChargebackRequest(BaseModel):
    merchant_id: str
    chargeback_code: str
    reason: str
    amount: float
    source: str
    timestamp: Optional[datetime] = None


class ChargebackResponse(BaseModel):
    id: str
    merchant_id: str
    chargeback_code: str
    reason: str
    amount: float
    source: str
    timestamp: datetime
