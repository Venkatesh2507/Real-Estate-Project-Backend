from fastapi import Depends,HTTPException,status
from fastapi.security  import HTTPBearer,HTTPAuthorizationCredentials
from firebase_admin import auth
security = HTTPBearer()

def verify_firebase_token(
        credentials:HTTPAuthorizationCredentials = Depends(security)
):
    # token = credentials.credentials
    # try:
    #     decoded_token = auth.verify_id_token(token)
    #     return decoded_token
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #          detail="Invalid or expired Firebase token"
    #     )

    if credentials is None or credentials.scheme.lower()!="bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    id_token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"}
        )
        

