import hmac, hashlib, json
import httpx
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from config import QUILTT_API_KEY, QUILTT_BASE_URL, QUILTT_WEBHOOK_SECRET
from models.models_openbanking import BankConnection, BankAccount, BankTransaction

HEADERS = {"Authorization": f"Bearer {QUILTT_API_KEY}", "Content-Type": "application/json"}

class QuilttService:
    @staticmethod
    async def create_connect_session(merchant_id: str, redirect_url: Optional[str] = None) -> dict:
        """
        Requests a new Quiltt Connect session URL the frontend can open in a webview
        to start Finicity linking. Endpoint name may vary; adjust path to your Quiltt account.
        """
        payload = {
            "provider": "finicity",
            "metadata": {"merchant_id": merchant_id},
            "redirect_url": redirect_url,   # optional, can be None
        }
        async with httpx.AsyncClient(timeout=30) as client:
            # Replace path with your Quiltt Connect Session endpoint
            resp = await client.post(f"{QUILTT_BASE_URL}/connect/sessions", headers=HEADERS, json=payload)
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    async def exchange_public_token(session_token: str) -> dict:
        """
        Exchange a short-lived session/public token for a stable Quilt connection_id
        """
        async with httpx.AsyncClient(timeout=30) as client:
            # Replace path with Quiltt's token exchange endpoint
            resp = await client.post(f"{QUILTT_BASE_URL}/connect/exchange", headers=HEADERS, json={"session_token": session_token})
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    def upsert_connection(db: Session, merchant_id: str, connection_id: str, raw: dict, status: str = "connected") -> BankConnection:
        conn = db.query(BankConnection).filter(BankConnection.connection_id == connection_id).one_or_none()
        if not conn:
            conn = BankConnection(merchant_id=merchant_id, connection_id=connection_id, status=status, raw=json.dumps(raw))
            db.add(conn)
        else:
            conn.status = status
            conn.raw = json.dumps(raw)
            conn.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conn)
        return conn

    @staticmethod
    async def fetch_accounts(connection_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            # Replace with Quiltt account listing endpoint
            resp = await client.get(f"{QUILTT_BASE_URL}/connections/{connection_id}/accounts", headers=HEADERS)
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    async def fetch_transactions(connection_id: str, account_id: str, start_date: str, end_date: str) -> dict:
        async with httpx.AsyncClient(timeout=60) as client:
            # Replace with Quiltt transactions endpoint
            params = {"start_date": start_date, "end_date": end_date}
            resp = await client.get(f"{QUILTT_BASE_URL}/connections/{connection_id}/accounts/{account_id}/transactions", headers=HEADERS, params=params)
            resp.raise_for_status()
            return resp.json()

    @staticmethod
    def persist_accounts(db: Session, connection: BankConnection, accounts_payload: dict):
        items = accounts_payload.get("accounts") or accounts_payload.get("data") or []
        for a in items:
            acct = BankAccount(
                connection_id=connection.id,
                provider_account_id=str(a.get("id") or a.get("accountId")),
                name=a.get("name"),
                mask=(a.get("mask") or a.get("accountNumberMasked")),
                type=a.get("type"),
                subtype=a.get("subtype"),
                currency=a.get("currency") or "USD",
                current_balance=a.get("balances", {}).get("current") if isinstance(a.get("balances"), dict) else a.get("currentBalance"),
                available_balance=a.get("balances", {}).get("available") if isinstance(a.get("balances"), dict) else a.get("availableBalance"),
                institution_name=(a.get("institution", {}) or {}).get("name") if isinstance(a.get("institution"), dict) else a.get("institutionName"),
            )
            db.add(acct)
        db.commit()

    @staticmethod
    def persist_transactions(db: Session, account_id: str, tx_payload: dict):
        rows = tx_payload.get("transactions") or tx_payload.get("data") or []
        for t in rows:
            db.add(BankTransaction(
                account_id=account_id,
                provider_txn_id=str(t.get("id") or t.get("transactionId")),
                amount=float(t.get("amount")),
                currency=t.get("currency") or "USD",
                posted_at=datetime.fromisoformat(t.get("postedAt") or t.get("postDate") or t.get("date")),
                description=t.get("description") or t.get("memo"),
                category=(t.get("category") or t.get("categoryName") or ""),
            ))
        db.commit()

    @staticmethod
    def verify_webhook(signature_header: str, body_bytes: bytes) -> bool:
        """
        Verify X-Quiltt-Signature using your webhook secret (HMAC-SHA256)
        """
        if not signature_header or not QUILTT_WEBHOOK_SECRET:
            return False
        mac = hmac.new(QUILTT_WEBHOOK_SECRET.encode(), body_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(mac, signature_header)
