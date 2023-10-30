from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import UOWDep
from schemas.users_schema import UserSchemaCreate
from services.users_service import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def add_user(
    user: UserSchemaCreate,
    uow: UOWDep,
):
    user_id = await UsersService().add_user(uow,user)
    return {"user_id": user_id}


@router.get("")
async def get_users(
    uow: UOWDep,
):
    users = await UsersService().get_users(uow)
    return users

@router.get("/")
async def get_users(
    uow: UOWDep,
    username: str,
):
    users = await UsersService().get_by_username(uow, username)
    return users