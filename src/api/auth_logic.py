
from typing import Annotated, Callable
from fastapi import Depends,  HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from api.auth_handler import decodeJWT
from api.deps import UOWDep


from schemas.users_schema import UserSchema
from services.users_service import UsersService



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

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
            # print(payload)
            
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


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

#Create a jwt

#Validate jwt
async def get_current_user(
        token: Annotated[str, Depends(JWTBearer())],
        uow: UOWDep,
        
) -> UserSchema:
    try:
        payload = decodeJWT(token)

        user_id: str = payload.get("id")
        
        user: UserSchema = await UsersService().get_by_id( uow, user_id)
       

        if not user: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not validated")


async def admin_access(
        token: Annotated[str, Depends(JWTBearer())],
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