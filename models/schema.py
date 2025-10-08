from dataclasses import field
from pydantic import BaseModel, Field, validator
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


class UserMerchantResponse(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


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
    type_of_merchant: str
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


class MerchantResponseDAO(BaseModel):
    id: str = None
    legal_entity: Optional[str] = None
    industry: str
    business_name: Optional[str] = None
    owner_name: Optional[str] = None
    type_of_merchent: str
    # nested
    profile: Optional[MerchantProfileDAO] = None
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


###########################################
# Product
###########################################

class ProductRequestDAO(BaseModel):
    name: str
    description: str


class ProductResponseDAO(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        from_attributes = True


###########################################
# Plans
###########################################

class PlanRequestDAO(BaseModel):
    name: str
    description: str
    minimum_selected: str
    no_of_items: str
    is_free: bool = False
    product_ids: List[str]
    price_m: Optional[str] = None
    price_y: Optional[str] = None
    duration: Optional[Any] = None
    recommended: bool = False

    @validator("product_ids", pre=True, always=True)
    def validate_products(cls, product_ids, values):
        no_of_items = values.get("no_of_items")
        if no_of_items is not None:
            try:
                no_of_items_int = int(no_of_items)
            except ValueError:
                raise ValueError("no_of_items must be integer")

            if no_of_items_int != len(product_ids):
                raise ValueError(
                    f"the number of items ({no_of_items_int}) must match the length of products selected length {len(product_ids)}")
        return product_ids


###########################################
# Gateways
###########################################

class GatewayRequestDAO(BaseModel):
    name: str
    api_key: str
    publishable_key: str
    webhook: str


class GatewayResponseDAO(BaseModel):
    id: str
    name: str
    api_key: str
    publishable_key: str
    webhook: str
    status: bool

    class Config:
        from_attributes = True


###########################################
# Offers
###########################################

class OfferRequestDAO(BaseModel):
    offer_name: str
    offer_starts: datetime
    offer_ends: datetime
    discount_percent: str
    plan_id: str


class OfferRequestModelDAO(BaseModel):
    coupon_id: str
    offer_name: str
    offer_starts: datetime
    offer_ends: datetime
    discount_percent: str
    plan_id: str
