from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def lawyer_only(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("role") != "lawyer":
        raise HTTPException(status_code=403, detail="Lawyer access only")

    return payload
