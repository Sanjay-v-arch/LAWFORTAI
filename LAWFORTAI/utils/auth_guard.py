from fastapi import Depends, HTTPException
from auth.jwt import decode_token

def lawyer_only(token=Depends(decode_token)):
    if token["role"] != "lawyer":
        raise HTTPException(status_code=403, detail="Lawyer access only")
    return token
