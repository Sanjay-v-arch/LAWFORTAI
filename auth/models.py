from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    contact: str  # email or phone
    password: str
    role: str  # Citizen | Police | Legal
    verified: bool = False

    policeId: Optional[str] = None
    lawyerId: Optional[str] = None

    created_at: datetime = datetime.utcnow()
