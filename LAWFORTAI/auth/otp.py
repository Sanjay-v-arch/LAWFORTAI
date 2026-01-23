import random
import time
import logging
from typing import Dict

# OTP store structure
# {
#   contact: {
#       "otp": "123456",
#       "expires": 1234567890,
#       "attempts": 0
#   }
# }
logger = logging.getLogger("uvicorn")

OTP_STORE: Dict[str, dict] = {}

OTP_EXPIRY_SECONDS = 300        # 5 minutes
MAX_OTP_ATTEMPTS = 5            # brute-force protection


def generate_otp(contact: str) -> str:
    """
    Generate a 6-digit OTP and store it with expiry + attempts.
    """
    otp = str(random.randint(100000, 999999))

    OTP_STORE[contact] = {
        "otp": otp,
        "expires": time.time() + OTP_EXPIRY_SECONDS,
        "attempts": 0
    }

    # ⚠️ DEBUG ONLY (remove in production)
    logger.info("OTP generated successfully")


    return otp


def verify_otp(contact: str, otp: str) -> bool:
    """
    Verify OTP with expiry & attempt limit.
    """
    record = OTP_STORE.get(contact)

    if not record:
        return False

    # ⏰ OTP expired
    if time.time() > record["expires"]:
        OTP_STORE.pop(contact, None)
        return False

    # 🚫 Too many attempts
    if record["attempts"] >= MAX_OTP_ATTEMPTS:
        OTP_STORE.pop(contact, None)
        return False

    # ❌ Wrong OTP
    if record["otp"] != otp:
        record["attempts"] += 1
        return False

    # ✅ Correct OTP → cleanup
    OTP_STORE.pop(contact, None)
    return True
