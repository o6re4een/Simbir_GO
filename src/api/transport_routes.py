from datetime import datetime, timedelta
from typing import Annotated, Callable
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import sqlalchemy
from api.auth_handler import create_acess_token
from api.auth_logic import JWTBearer, admin_access, bcrypt_context, authenticate_user,user_deps

from api.deps import UOWDep
from schemas.token_schema import Token
from schemas.transport_schema import TransportSchemaBase, TransportSchemaCreate, TransportSchemaUpdate

from schemas.users_schema import UserSchema, UserSchemaCreate, UserSchemaResponse
from services.transport_service import TransportService
from services.users_service import UsersService
from setting import JWT_SECRET as jwt_secret



router = APIRouter(
    prefix="/Transport",
    tags=["TransportController"],
)


@router.post("", )
async def add_transport(
    uow: UOWDep,
    user: user_deps,
    transport_data: TransportSchemaCreate
    ):
    transport = await TransportService().create_transport(uow, transport_data, user.id)
    return transport 

@router.get("/{id}", )
async def get_transport_by_id(
    uow: UOWDep,
   
    id: int,
    ):
    try:
        transport = await TransportService().get_transport_by_id(uow, id)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No that id")

    return transport 

@router.put("/{id}", )
async def update_transport(
    uow: UOWDep,
    user: user_deps,
    transport_data: TransportSchemaUpdate,
    id: int
    ):

    curr_transport = await TransportService().get_transport_by_id(uow, id)
    if not curr_transport.ownerId == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not owner")
    
    transport = await TransportService().update_transport(uow, id, transport_data)
    return transport 

@router.delete("/{id}", )
async def delete_transport(
    uow: UOWDep,
    user: user_deps,
    id: int
    ):

    curr_transport = await TransportService().get_transport_by_id(uow, id)
    if not curr_transport.ownerId == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not owner")
    
    transport = await TransportService().delete_transport_by_id(uow, id)
    return transport 

