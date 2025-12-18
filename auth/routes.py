from fastapi import APIRouter, HTTPException, Request
import logging
from auth.schemas import SignupSchema, LoginSchema, OtpSchema
from auth.otp import generate_otp, verify_otp
from auth.jwt import hash_password, verify_password, create_token

router = APIRouter()
logger = logging.getLogger("uvicorn")

# -------------------- In-memory DB (Replace with MongoDB later) --------------------
FAKE_DB = {}

# -------------------- SIGNUP --------------------
@router.post("/signup")
async def signup(data: SignupSchema, request: Request):
    logger.info(
        f"Signup attempt from {request.client.host} | Contact: {data.contact}"
    )

    # ---- HARD VALIDATION ----
    if not data.name or not data.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if not data.contact or not data.contact.strip():
        raise HTTPException(status_code=400, detail="Contact is required")

    if not data.password or not data.password.strip():
        raise HTTPException(status_code=400, detail="Password is required")

    # ---- USER EXISTENCE LOGIC (FIXED) ----
    existing_user = FAKE_DB.get(data.contact)

    if existing_user:
        if existing_user["verified"]:
            raise HTTPException(
                status_code=400,
                detail="User already exists. Please login."
            )
        else:
            logger.info(
                f"User {data.contact} exists but not verified. Resending OTP."
            )

    # ---- SAVE / UPDATE USER ----
    FAKE_DB[data.contact] = {
        "name": data.name.strip(),
        "contact": data.contact.strip(),
        "password": hash_password(data.password),
        "role": data.role,
        "verified": False,
        "policeId": data.policeId,
        "lawyerId": data.lawyerId,
    }

    # ---- OTP ----
    otp = generate_otp(data.contact)
    logger.info(f"OTP sent to {data.contact}: {otp}")

    return {"message": "OTP sent for verification"}


# -------------------- VERIFY OTP --------------------
@router.post("/verify-otp")
async def verify(data: OtpSchema, request: Request):
    logger.info(
        f"OTP verification attempt from {request.client.host} | Contact: {data.contact}"
    )

    if data.contact not in FAKE_DB:
        logger.warning(f"OTP verify failed: User {data.contact} not found")
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_otp(data.contact, data.otp):
        logger.warning(f"Invalid OTP for {data.contact}")
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
    elif data.email:
        user = next(
            (u for u in FAKE_DB.values() if u.get("email") == data.email), None
        )
        identifier = data.email

    logger.info(f"Login attempt from {request.client.host} | Identifier: {identifier}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["verified"]:
        raise HTTPException(status_code=403, detail="Verify account first")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_token({"sub": identifier, "role": user["role"]})

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
