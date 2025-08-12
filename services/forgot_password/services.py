from sqlalchemy.orm import Session
from models.models import User
from models.schema import ForgotPasswordRequest, ForgotPasswordResponse, VerifyOTPRequest, VerifyOTPResponse, \
    VerifyOTPResponseDAO
from fastapi import HTTPException, status
import secrets
import datetime

from jinja2 import Template

from utils.send_message import EmailClient


class ForgotPasswordService:
    @staticmethod
    def generate_reset_token(payload: ForgotPasswordRequest, db: Session) -> ForgotPasswordResponse:
        user = db.query(User).filter(User.email == payload.email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

        reset_token = ''.join(str(secrets.randbelow(10)) for _ in range(6))
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        user.reset_token = reset_token
        user.reset_token_expiry = expiry_time
        db.commit()

        msg_data = {"otp": reset_token}
        message_template = Template("""<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <title>OTP</title>
                            <meta name="viewport" content="width=device-width, initial-scale=1">
                            <style>
                              body { margin:0; padding:0; background:#ffffff; font-family:Arial, Helvetica, sans-serif; }
                              .wrap { width:100%; padding:24px 0; text-align:center; }
                              .otp { font-size:32px; font-weight:700; letter-spacing:6px; color:#111827; }
                            </style>
                          </head>
                          <body>
                            <div class="wrap">
                              <div class="otp">{{otp}}</div>
                            </div>
                          </body>
                        </html>""")

        msg = message_template.render(msg_data).strip()
        ses = EmailClient()
        ses.send_email(payload.email, "Reset Your Login Credentials", msg)
        # In real apps: Send this via email/SMS instead
        return ForgotPasswordResponse(
            message="Reset token generated. Please check your email.")

    @staticmethod
    def verify_otp(payload: VerifyOTPRequest, db_session: Session):
        try:
            user = db_session.query(User).filter(User.email == payload.email).first()
            if not user:
                raise HTTPException(status_code=404, detail="Invalid reset token")

            if not user.reset_token_expiry or user.reset_token_expiry < datetime.datetime.utcnow():
                raise HTTPException(status_code=400, detail="Reset token expired")

            if not payload.otp_code == user.reset_token:
                raise HTTPException(status_code=400, detail="Invalid Otp provided")

            reset_token = secrets.token_urlsafe(32)
            expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

            user.reset_token = reset_token
            user.reset_token_expiry = expiry_time

            db_session.commit()
            return VerifyOTPResponseDAO(message="Password has been Verified successfully",
                                        expire_token=reset_token)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong.")
