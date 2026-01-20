from fastapi import APIRouter, HTTPException, Request
import logging
from auth.schemas import SignupSchema, LoginSchema, OtpSchema
from auth.otp import generate_otp, verify_otp
from auth.jwt import hash_password, verify_password, create_token
from auth.email import send_otp_email

router = APIRouter()
logger = logging.getLogger("uvicorn")
# -------------------- APPROVED POLICE IDS --------------------
VALID_POLICE_IDS = {
    "POL12345",
    "POL67890",
    "POL98765",
    "98757496857"  # add your real IDs here
}
# -------------------- APPROVED LAWYER IDS --------------------
VALID_LAWYER_IDS = {
    "LAW12345",
    "LAW67890",
    "LAW99999",
    "ADV2024001"  # add your real IDs here
}


# -------------------- In-memory DB (Replace with MongoDB later) --------------------
FAKE_DB = {}

# -------------------- SIGNUP --------------------
@router.post("/signup")
async def signup(data: SignupSchema, request: Request):
    logger.info(f"Signup attempt from {request.client.host} | Contact: {data.contact}")

    # ---- HARD VALIDATION ----
    if not data.name or not data.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if not data.contact or not data.contact.strip():
        raise HTTPException(status_code=400, detail="Contact is required")

    if not data.password or not data.password.strip():
        raise HTTPException(status_code=400, detail="Password is required")

    if data.role not in ["citizen", "police", "lawyer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if data.role == "police":
        if not data.policeId:
            raise HTTPException(status_code=400, detail="Police ID is required")

        if data.policeId not in VALID_POLICE_IDS:
            raise HTTPException(status_code=403, detail="Invalid Police ID")

    if data.role == "lawyer":
        if not data.lawyerId:
            raise HTTPException(status_code=400, detail="Lawyer ID is required")

        if data.lawyerId not in VALID_LAWYER_IDS:
            raise HTTPException(status_code=403, detail="Invalid Lawyer ID")

    # ---- USER EXISTENCE LOGIC ----
    existing_user = FAKE_DB.get(data.contact)

    if existing_user:
        if existing_user["verified"]:
            raise HTTPException(
                status_code=400,
                detail="User already exists. Please login."
            )
        else:
            logger.info(f"User {data.contact} exists but not verified. Resending OTP.")

    # ---- SAVE / UPDATE USER ----
    FAKE_DB[data.contact] = {
        "name": data.name.strip(),
        "contact": data.contact.strip(),
        "password": hash_password(data.password),
        "role": data.role,
        "verified": False,
        "policeId": data.policeId if data.role == "police" else None,
        "lawyerId": data.lawyerId if data.role == "lawyer" else None,
    }

    # ---- OTP ----
    otp = generate_otp(data.contact)
    send_otp_email(data.contact, otp)


    return {
        "message": "OTP sent for verification",
        "role": data.role
    }


# -------------------- VERIFY OTP --------------------
@router.post("/verify-otp")
async def verify(data: OtpSchema, request: Request):
    logger.info(f"OTP verification from {request.client.host} | Contact: {data.contact}")

    if data.contact not in FAKE_DB:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_otp(data.contact, data.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    FAKE_DB[data.contact]["verified"] = True
    logger.info(f"User {data.contact} verified successfully")

    return {"message": "Account verified"}


# -------------------- LOGIN --------------------
@router.post("/login")
async def login(data: LoginSchema, request: Request):
    user = None
    identifier = None

    if data.contact:
        user = FAKE_DB.get(data.contact)
        identifier = data.contact

    logger.info(f"Login attempt from {request.client.host} | Identifier: {identifier}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["verified"]:
        raise HTTPException(status_code=403, detail="Verify account first")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_token({
        "sub": identifier,
        "role": user["role"]
    })

    return {
        "token": token,
        "user": {
            "name": user["name"],
            "role": user["role"],
            "contact": user["contact"],
            "policeId": user["policeId"],
            "lawyerId": user["lawyerId"],
        },
    }
