from pydantic import BaseModel, EmailStr
from typing import Optional

# -------------------- Signup --------------------
class SignupSchema(BaseModel):
    name: str
    contact: str
    role: str
    policeId: Optional[str] = None
    lawyerId: Optional[str] = None
    password: Optional[str] = None  # ✅ OPTIONAL

# -------------------- Login --------------------
class LoginSchema(BaseModel):
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

# -------------------- OTP --------------------
class OtpSchema(BaseModel):
    contact: str
    otp: str
