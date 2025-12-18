import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_otp_email(to_email: str, otp: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = "LawFort AI - OTP Verification"

    body = f"""
    Your OTP for LawFort AI is: {otp}

    This OTP is valid for 5 minutes.
    Do not share it with anyone.
    """
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")))
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
