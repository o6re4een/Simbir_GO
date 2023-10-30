from datetime import datetime, timedelta
from typing import Annotated, Callable
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import sqlalchemy
from api.auth_logic import admin_access, create_acess_token, bcrypt_context, authenticate_user,user_deps
from api.deps import UOWDep
from schemas.token_schema import Token

from schemas.users_schema import UserSchema, UserSchemaCreate, UserSchemaResponse
from services.users_service import UsersService
from setting import JWT_SECRET as jwt_secret



router = APIRouter(
    prefix="/Account",
    tags=["Users"],
)
# to get a string like this run:
# openssl rand -hex 32



@router.post("/SignUp", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserSchemaCreate,
    uow: UOWDep,
):
    #Change pass to hashed with secret
    user.password = bcrypt_context.hash(user.password)
    user = await UsersService().add_user(uow,user)
    token = create_acess_token(user.username, user.id, timedelta(hours=24), is_admin=user.isAdmin)
    return {"acess_token": token, "token_type": "bearer"}



@router.post("/SignIn", response_model=Token)
async def login(
    user:  Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep,
):
   
    user_auth: UserSchema = await authenticate_user(user.username, user.password, uow)
    
    if not user_auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    token = create_acess_token(user_auth.username, user_auth.id, timedelta(hours=24), is_admin=user_auth.isAdmin)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/Me", response_model=UserSchemaResponse)
async def get_me(
    user: user_deps,
    # admin: bool = Depends(admin_access),
   
):
    
    # print(user.isAdmin) 
    return user



@router.put("/Update", response_model=Token)
async def update_user(
    user: user_deps,
    uow: UOWDep,
    update_data: UserSchemaCreate,
):
   
    if user.password:
        update_data.password = bcrypt_context.hash(user.password)
    updated_user = await UsersService().update_user(uow, user.id, update_data)
    token = create_acess_token(updated_user.username, updated_user.id, timedelta(hours=24), is_admin=updated_user.isAdmin)
    return {"access_token": token, "token_type": "bearer"}
    

#ADMIN ROUTE
 

    