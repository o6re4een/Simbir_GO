from datetime import datetime, timedelta
from typing import Annotated, Callable
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from api.deps import UOWDep


from schemas.users_schema import UserSchema
from services.users_service import UsersService
from setting import JWT_SECRET as jwt_secret
ALGORITHM = "HS256"


#decorator to chek if token is blacklisted
# def token_not_blacklisted():
#     def decorator(func: Callable):
#         async def wrapper(*args, **kwargs):
#             user = await get_current_user()
#             if user.access_token in blacklisted_tokens:
#                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is blacklisted")
#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/Account/SignIn", scheme_name="JWT")


async def authenticate_user(username: str, password: str, uow: UOWDep):
    user = await UsersService().get_by_username(uow, username)
    
    #Check if user exist
    if not user:
        return False

    #Verify password
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User password not match")

        return False

    return user

def create_acess_token(username:str, user_id:str, expires_delta: timedelta, is_admin: bool):
    encode = {"sub": username, "id": user_id, "admin": is_admin}
    expires = datetime.utcnow()+expires_delta
    encode.update({"exp": expires})
    
    return jwt.encode(encode, jwt_secret, algorithm=ALGORITHM)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_bearer)],
        uow: UOWDep,
) -> UserSchema:
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        
        user: UserSchema = await UsersService().get_by_id( uow, user_id)
       

        if not user: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not validated")


async def admin_access(
        token: Annotated[str, Depends(oauth2_bearer)],
        uow: UOWDep,
        
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not autorized")
    
    user: UserSchema = await get_current_user(token, uow)
    if not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin")
    return True

user_deps = Annotated[UserSchema, Depends(get_current_user)]

admin_deps = Annotated[bool, Depends(admin_access)]