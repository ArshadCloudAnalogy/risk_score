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
    user_id: str

class SignUpErrorResponse(BaseModel):
    message: str


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


class MerchantProfileRequest(BaseModel):
    dba: Optional[str] = None
    business_address: Optional[str] = None
    owner_name: str
    business_name: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None


class MerchantOnboardRequest(BaseModel):
    legal_entity: Optional[str] = None
    industry: str
    fico_score: int
    self_employed: bool
    verified_income: str
    mid: Optional[str] = None
    bin: Optional[str] = None
    mcc: Optional[str] = None
    ein: Optional[str] = None
    website: Optional[str] = None
    fico_score: Optional[int] = Field(None, ge=300, le=850)
    self_employed: Optional[bool] = None
    annual_income: Optional[float] = None
    verified_income: Optional[float] = None
    bank_behaviour: Optional[BankBehavior] = None
    device_risk_score: Optional[float] = Field(0, ge=0, le=1)
    fraud_score: Optional[float] = Field(0, ge=0, le=1)
    keywords: List[str]
    business_profile: Optional[MerchantProfileRequest] = None


class MerchantResponse(BaseModel):
    message:str
    merchant_id: str
    merchant_profile: str


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


class ScoreSummary(BaseModel):
    score: int
    tier: str
    decision: str
    limit_suggestion: Optional[str] = None
    risk_tags: List[str] = []
    explanation: Optional[str] = None
    heat_score: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MerchantProfileDAO(BaseModel):
    dba: Optional[str] = None
    business_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None

    model_config = {"from_attributes": True}


class MerchantResponse(BaseModel):
    id: str
    legal_entity: Optional[str] = None
    industry: str
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    mid: Optional[str] = None
    bin: Optional[str] = None
    mcc: Optional[str] = None
    ein: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # nested
    profile: Optional[MerchantProfileDAO] = None
    latest_score: Optional[ScoreSummary] = None

    model_config = {"from_attributes": True}
