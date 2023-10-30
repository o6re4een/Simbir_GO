# app/auth/auth_handler.py
# This file is responsible for signing , encoding , decoding and returning JWTS
from datetime import datetime, timedelta
import statistics
import time
from typing import Dict
from fastapi import HTTPException, status

from jose import JWTError, jwt
ALGORITHM = "HS256"
from setting import JWT_SECRET as jwt_secret

def create_acess_token(username:str, user_id:str, expires_delta: timedelta, is_admin: bool) ->str:
    encode = {"sub": username, "id": user_id, "admin": is_admin}
    expires = datetime.utcnow()+expires_delta
    encode.update({"exp": expires})
    token = jwt.encode(encode, jwt_secret, algorithm=ALGORITHM)
    
    return token 



def decodeJWT(token: str) -> dict:
   
    try:
        
        payload = jwt.decode(token, jwt_secret, algorithms=[ALGORITHM])
        expiration_time = payload.get('exp', None)
        
        
        if expiration_time is not None:
            current_time = datetime.utcnow()
            expiration_datetime = datetime.fromtimestamp(expiration_time)

            if current_time >= expiration_datetime:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token Expired")
        return payload
    except Exception as e:
        print(e)
        return None