from dataclasses import field
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class APIResponse(BaseModel):
    message: str
    status: str 
    data: Optional[Any] = None

class ProfessionalDetailsResponse(BaseModel):
    company: Optional[str] = None
    department: Optional[str] = None
    join_date: Optional[datetime] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    phone: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None
    first_name: str
    last_name: str
    professional_details: Optional[ProfessionalDetailsResponse] = None
    class Config:
        from_attributes = True

# --- Signatory request & DAO ---
class SignatoryRequest(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: Optional[datetime] = None
    residential_address: Optional[str] = None
    phone_mobile: Optional[str] = None
    phone_business: Optional[str] = None
    email: Optional[str] = None
    ssn_or_national_id: Optional[str] = None
    gov_id_front: Optional[str] = None  # expect path/url for now
    gov_id_back: Optional[str] = None
    ownership_percent: Optional[float] = None
    digital_signature: Optional[str] = None

class SignatoryDAO(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: Optional[datetime] = None
    residential_address: Optional[str] = None
    phone_mobile: Optional[str] = None
    phone_business: Optional[str] = None
    email: Optional[str] = None
    ssn_or_national_id: Optional[str] = None
    gov_id_front: Optional[str] = None
    gov_id_back: Optional[str] = None
    ownership_percent: Optional[float] = None
    digital_signature: Optional[str] = None

    model_config = {"from_attributes": True}


# --- IBO / Entity request & DAO ---
class IboEntityRequest(BaseModel):
    legal_business_name: str
    dba: Optional[str] = None
    business_type: Optional[str] = None
    business_address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    ein: Optional[str] = None
    bank_name: Optional[str] = None
    routing_number: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    articles_of_incorporation: Optional[str] = None
    operating_agreement: Optional[str] = None
    business_license: Optional[str] = None
    proof_of_address: Optional[str] = None

class IboEntityDAO(BaseModel):
    legal_business_name: str
    dba: Optional[str] = None
    business_type: Optional[str] = None
    business_address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    ein: Optional[str] = None
    bank_name: Optional[str] = None
    routing_number: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    articles_of_incorporation: Optional[str] = None
    operating_agreement: Optional[str] = None
    business_license: Optional[str] = None
    proof_of_address: Optional[str] = None

    model_config = {"from_attributes": True}


# --- Merchant Account request & DAO (MID profile) ---
class MerchantAccountRequest(BaseModel):
    merchant_legal_name: Optional[str] = None
    dba: Optional[str] = None
    mcc: Optional[str] = None
    processing_type: Optional[str] = None
    average_ticket: Optional[float] = None
    highest_ticket: Optional[float] = None
    monthly_processing_volume: Optional[float] = None
    refund_policy_url: Optional[str] = None
    customer_support_phone: Optional[str] = None
    customer_support_email: Optional[str] = None
    checkout_url: Optional[str] = None
    settlement_bank_name: Optional[str] = None
    settlement_routing_number: Optional[str] = None
    settlement_account_number: Optional[str] = None
    settlement_account_type: Optional[str] = None

class MerchantAccountDAO(BaseModel):
    merchant_legal_name: Optional[str] = None
    dba: Optional[str] = None
    mcc: Optional[str] = None
    processing_type: Optional[str] = None
    average_ticket: Optional[float] = None
    highest_ticket: Optional[float] = None
    monthly_processing_volume: Optional[float] = None
    refund_policy_url: Optional[str] = None
    customer_support_phone: Optional[str] = None
    customer_support_email: Optional[str] = None
    checkout_url: Optional[str] = None
    settlement_bank_name: Optional[str] = None
    settlement_routing_number: Optional[str] = None
    settlement_account_number: Optional[str] = None
    settlement_account_type: Optional[str] = None

    model_config = {"from_attributes": True}


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


# --- MerchantOnboardRequest updated to include nested structures ---
class MerchantOnboardRequest(BaseModel):
    legal_entity: Optional[str] = None
    type_of_merchant: str
    industry: str
    fico_score: Optional[int] = Field(None, ge=300, le=850)
    self_employed: Optional[bool] = None
    annual_income: Optional[float] = None
    verified_income: Optional[float] = None
    mid: Optional[str] = None
    bin: Optional[str] = None
    mcc: Optional[str] = None
    ein: Optional[str] = None
    website: Optional[str] = None
    device_risk_score: Optional[float] = Field(0, ge=0, le=1)
    fraud_score: Optional[float] = Field(0, ge=0, le=1)
    keywords: List[str] = []
    business_profile: Optional[MerchantProfileRequest] = None

    # NEW fields
    signatories: Optional[List[SignatoryRequest]] = None
    ibo_entity: Optional[IboEntityRequest] = None
    merchant_accounts: Optional[List[MerchantAccountRequest]] = None
    documents: Optional[List[str]] = None  # list of doc URLs/paths


class MerchantResponse(BaseModel):
    message: str
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
    business_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None

    model_config = {"from_attributes": True}

class UserMerchantResponse(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class MerchantResponseDAO(BaseModel):
    id: str = None
    legal_entity: Optional[str] = None
    industry: str
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    type_of_merchent: str
    profile: Optional[MerchantProfileDAO] = None
    signatories: Optional[List[SignatoryDAO]] = None
    ibo_entity: Optional[IboEntityDAO] = None
    merchant_accounts: Optional[List[MerchantAccountDAO]] = None
    documents: Optional[List[str]] = None
    latest_score: Optional[ScoreSummary] = None
    user_details: Optional[UserMerchantResponse] = None

    model_config = {"from_attributes": True}


class MerchantListResponse(BaseModel):
    id: str
    name: str
    email: str
    status: str
    type_of_merchent: str
    riskScore: Optional[float] = 0.0
    revenue: Optional[str] = "0"
    transactions: Optional[int] = 0
    joinDate: str
    category: Optional[str] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True
