
from typing import Annotated, Callable
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy
from api.auth_logic import admin_access, bcrypt_context, user_deps, get_current_user
from api.deps import UOWDep
from schemas.users_schema import UserSchema, UserSchemaResponse, userSchemaEdit
from services.users_service import UsersService


router = APIRouter(
    prefix="/Payment",
    tags=["PaymentController"],
)

@router.post("/Hesoyam/{accountId}")
async def pay_user(
    uow:UOWDep,
    accountId: int,
    user: user_deps,
):
    try:
        if not user.id == accountId:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin")
        user = await UsersService().add_balance(uow, accountId)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    return user

@router.post("/Admin/Hesoyam/{accountId}")
async def pay_admin(
    uow:UOWDep,
    accountId: int,
    isAdmin: bool = Depends(admin_access),
):
    try:
        user = await UsersService().add_balance(uow, accountId)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user