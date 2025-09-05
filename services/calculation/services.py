from dataclasses import dataclass
from typing import List, Dict, Tuple

HIGH_RISK = {"peptides", "cannabis", "psilocybin", "subscription_ecommerce"}


@dataclass
class BankBehavior:
    overdrafts_6mo: int = 0
    avg_balance: float = 0.0
    nsf_fees: int = 0


@dataclass
class GateOutput:
    points: int
    tags: List[str]
    details: Dict


class Calculation:

    @staticmethod
    def gate_age_income(self_employed: bool, annual_income: float, verified_income: float | None) -> GateOutput:
        # Gate 1: Age & Income (brief: model income suitability)
        # Simplified: use income sufficiency + delta to verified
        points = 0
        tags: List[str] = []
        details = {}
        base = verified_income if verified_income is not None else annual_income
        if base >= 90000:
            points += 20
        elif base >= 60000:
            points += 12
        elif base >= 30000:
            points += 5
        else:
            points -= 10
            tags.append("low_income")
        if verified_income is not None and verified_income < 0.8 * annual_income:
            points -= 5
            tags.append("income_mismatch")
        details.update({"income_used": base})
        return GateOutput(points, tags, details)

    @staticmethod
    def gate_identity_fraud(device_risk_score: float, fraud_score: float) -> GateOutput:
        # Gate 2: Identity & Fraud (simulate Socure + SentiLink style scores)
        points = 0
        tags: List[str] = []
        details = {"device_risk_score": device_risk_score, "fraud_score": fraud_score}
        # Lower is better; clamp 0..1
        dr = max(0.0, min(1.0, device_risk_score))
        fr = max(0.0, min(1.0, fraud_score))
        points += int((1 - dr) * 10)  # good device hygiene adds points
        points += int((1 - fr) * 15)  # lower fraud_score adds points
        if fr > 0.6:
            points -= 25;
            tags.append("high_fraud_signal")
        elif fr > 0.3:
            tags.append("moderate_device_risk")
        return GateOutput(points, tags, details)

    @staticmethod
    def gate_creditworthiness(fico_score: int | None, tradelines: int | None = None,
                              utilization: float | None = None, chargeoffs: int | None = None,
                              dti: float | None = None) -> GateOutput:
        # Gate 3: Creditworthiness (simulate Experian logic per brief)
        points = 0
        tags: List[str] = []
        details = {"fico": fico_score, "tradelines": tradelines, "utilization": utilization, "chargeoffs": chargeoffs,
                   "dti": dti}
        if fico_score is None:
            points -= 10
            tags.append("thin_file")
        else:
            if fico_score < 580:
                return GateOutput(points - 999, tags + ["fico_below_min"], details)  # knockout
            elif fico_score < 620:
                points -= 15
            elif fico_score < 680:
                points += 5
            else:
                points += 18
        if utilization is not None and utilization > 0.75: points -= 10; tags.append("high_utilization")
        if chargeoffs and chargeoffs > 0: points -= 20; tags.append("chargeoffs_present")
        if dti is not None and dti > 0.45: points -= 8; tags.append("high_dti")
        return GateOutput(points, tags, details)

    @staticmethod
    def gate_bank_behaviour(bb: BankBehavior) -> GateOutput:
        # Gate 4: Bank Behavior (simulate Plaid/Open Banking)
        points = 0
        tags: List[str] = []
        details = {"overdrafts_6mo": bb.overdrafts_6mo, "avg_balance": bb.avg_balance, "nsf_fees": bb.nsf_fees}
        if bb.avg_balance >= 5000:
            points += 20
        elif bb.avg_balance >= 2000:
            points += 12
        elif bb.avg_balance >= 500:
            points += 5
        else:
            points -= 10;
            tags.append("low_avg_balance")

        if bb.overdrafts_6mo >= 3:
            points -= 15;
            tags.append("frequent_overdrafts")
        elif bb.overdrafts_6mo == 2:
            points -= 8
        elif bb.overdrafts_6mo == 1:
            points -= 4

        if bb.nsf_fees >= 2: points -= 10; tags.append("nsf_events")
        return GateOutput(points, tags, details)

    def industry_rules(industry: str, keywords: list[str]) -> Tuple[int, list[str], int]:
        # Returns (industry_points, tags, heat_penalty)
        tags: List[str] = []
        base_score = 10   # start with high score = safe
        ind = (industry or "").lower().strip().replace(" ", "_")
        kw = {k.lower() for k in (keywords or [])}

        if ind in HIGH_RISK or len(HIGH_RISK & kw) > 0:
            tags.append(ind if ind in HIGH_RISK else "high_risk_keyword")
            base_score = 1   # lower score = more risk

        # heat_penalty now directly proportional to risk
        return (base_score, tags, (10 - base_score) * 10)

    @staticmethod
    def combine_gates(g1: GateOutput, g2: GateOutput, g3: GateOutput, g4: GateOutput,
                      industry_pts: int, industry_tags: List[str]) -> dict:
        credit_weight = g3.points
        fraud_penalty = g2.points - 10 if "high_fraud_signal" in g2.tags else g2.points
        bank_score = g4.points
        industry_penalty = industry_pts

        raw = credit_weight + fraud_penalty + bank_score + industry_penalty + g1.points
        # Normalize 0..100
        final_score = max(0, min(100, raw))
        if final_score >= 71:
            tier, decision = "Hot", "Approve"
        elif final_score >= 51:
            tier, decision = "Warm", "Manual Review"
        else:
            tier, decision = "Cold", "Reject"

        risk_tags = list({*g1.tags, *g2.tags, *g3.tags, *g4.tags, *industry_tags})
        explanation = {
            "credit_weight": credit_weight,
            "fraud_penalty": fraud_penalty,
            "bank_score": bank_score,
            "industry_risk_penalty": industry_penalty
        }
        return {"score": final_score, "tier": tier, "decision": decision,
                "risk_tags": risk_tags, "explanation": explanation}
