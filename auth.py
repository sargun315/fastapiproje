from jose import jwt,JWTError
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY="mysecret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth_schema= OAuth2PasswordBearer(tokenUrl="login")

#token create
def create_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY)

def verify_token(token:str = Depends(oauth_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=404, detail="not found token")