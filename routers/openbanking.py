from fastapi import APIRouter, Depends, HTTPException, Header, Query, status, Request
from sqlalchemy.orm import Session
from connections.db_connection import get_db
from services.quiltt_service import QuilttService
from models.models_openbanking import BankConnection, BankAccount
from api_response import ok, err

router = APIRouter(prefix="/openbanking", tags=["OpenBanking - Quiltt/Finicity"])

# 1) Start Connect session (frontend opens returned URL)
@router.post("/connect/start")
async def start_connect(merchant_id: str = Query(...), redirect_url: str | None = Query(None), db: Session = Depends(get_db)):
    try:
        sess = await QuilttService.create_connect_session(merchant_id, redirect_url)
        return ok("Connect session created", {"connect_session": sess})
    except Exception as e:
        return err(f"Failed to start connect: {e}")

# 2) Exchange token → create/attach connection to merchant
@router.post("/connect/exchange")
async def exchange_token(merchant_id: str = Query(...), session_token: str = Query(...), db: Session = Depends(get_db)):
    try:
        data = await QuilttService.exchange_public_token(session_token)
        connection_id = data.get("connection_id") or data.get("connectionId")
        if not connection_id:
            raise ValueError("Missing connection_id in Quiltt response")
        conn = QuilttService.upsert_connection(db, merchant_id=merchant_id, connection_id=connection_id, raw=data, status="connected")
        return ok("Connection established", {"connection_id": connection_id, "local_connection_id": conn.id})
    except Exception as e:
        return err(f"Token exchange failed: {e}")

# 3) Pull accounts from Quiltt and persist
@router.post("/connections/{connection_id}/sync-accounts")
async def sync_accounts(connection_id: str, db: Session = Depends(get_db)):
    try:
        payload = await QuilttService.fetch_accounts(connection_id)
        conn = db.query(BankConnection).filter(BankConnection.connection_id == connection_id).one_or_none()
        if not conn:
            raise HTTPException(status_code=404, detail="Local connection not found")
        QuilttService.persist_accounts(db, conn, payload)
        return ok("Accounts synced", {"count": len(payload.get("accounts") or payload.get("data") or [])})
    except Exception as e:
        return err(f"Failed to sync accounts: {e}")

# 4) Pull transactions for an account and persist
@router.post("/connections/{connection_id}/accounts/{provider_account_id}/sync-transactions")
async def sync_transactions(connection_id: str, provider_account_id: str, start_date: str = Query(...), end_date: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Find local account row by provider_account_id
        acct = db.query(BankAccount).filter(BankAccount.provider_account_id == provider_account_id).one_or_none()
        if not acct:
            raise HTTPException(status_code=404, detail="Account not found. Sync accounts first.")
        payload = await QuilttService.fetch_transactions(connection_id, provider_account_id, start_date, end_date)
        QuilttService.persist_transactions(db, acct.id, payload)
        return ok("Transactions synced", {"account_id": acct.id})
    except Exception as e:
        return err(f"Failed to sync transactions: {e}")

# 5) Webhook for Quiltt (Finicity events flow into here)
@router.post("/webhook")
async def quiltt_webhook(request: Request, x_quiltt_signature: str = Header(None), db: Session = Depends(get_db)):
    raw = await request.body()
    if not QuilttService.verify_webhook(x_quiltt_signature, raw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook signature")

    event = await request.json()
    # Examples: connection.updated, accounts.updated, transactions.synced, error
    etype = event.get("type")
    data = event.get("data", {})

    if etype == "connection.updated":
        conn_id = data.get("connection_id") or data.get("connectionId")
        status_val = data.get("status", "updated")
        # upsert connection if we know merchant; if not, just log
        # (you can extend to store event logs)
        return ok("Webhook processed", {"type": etype, "connection_id": conn_id, "status": status_val})

    # Add more handlers as needed...
    return ok("Webhook received", {"type": etype})
