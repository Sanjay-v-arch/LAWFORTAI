import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

# JWT config
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

# Password hashing config (bcrypt-safe)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ------------------------
# PASSWORD UTILS
# ------------------------

def hash_password(password: str) -> str:
    """
    Hash password safely for bcrypt (max 72 bytes)
    """
    if not password:
        raise ValueError("Password cannot be empty")

    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify password against stored hash
    """
    if not password or not hashed_password:
        return False

    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(password, hashed_password)

# ------------------------
# JWT UTILS
# ------------------------

def create_token(data: dict) -> str:
    """
    Create JWT access token with expiry
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
