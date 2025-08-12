import smtplib
import uuid
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

CHARSET = "UTF-8"
smtp_server = "smtp.gmail.com"
smtp_port = 587


def generate_custom_string():
    first_part = f"{random.getrandbits(64):016x}"
    second_part = str(uuid.uuid4())
    third_part = f"{random.randint(0, 999999):06d}"
    result = f"{first_part}-{second_part}-{third_part}"
    return result


class EmailClient:

    @staticmethod
    def send_email_via_SMTP(recipient, subject, body_html, cc):
        message = MIMEMultipart("alternative")
        smtp_email = os.getenv("SMTP_EMAIL")
        message["Subject"] = subject
        message["From"] = smtp_email
        message["To"] = recipient
        if cc:
            message["Cc"] = cc

        part_ = MIMEText(body_html, "html")
        message.attach(part_)
        server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_password = os.getenv("SMTP_PASSWORD")
        try:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, recipient, message.as_string())
            print("Email sent! Message ID: ", generate_custom_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

    @staticmethod
    def send_email(recipient, subject, body_html, cc: str = None):
        EmailClient.send_email_via_SMTP(recipient, subject, body_html, cc)
