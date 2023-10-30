
from typing import Annotated, Callable
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy
from api.auth_logic import admin_access, bcrypt_context
from api.deps import UOWDep
from schemas.users_schema import UserSchema, UserSchemaResponse, userSchemaEdit
from services.users_service import UsersService


#admin jwt
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlkIjoxMiwiYWRtaW4iOnRydWUsImV4cCI6MTY5ODc1NjIyMH0.MDQA0xYjVOGXbaW5kJ-N0e6elToODbbjadRFbeI-vKI

# user jwt = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiaWQiOjE0LCJhZG1pbiI6ZmFsc2UsImV4cCI6MTY5ODc1NzY4Nn0.Yzn5nW6I8aCQxiKH88akisw-N06sNxOrhTeU4jhq-V8
router = APIRouter(
    prefix="/Admin",
    tags=["AdminAccountController"],
)

@router.get("/Account", response_model=list[UserSchemaResponse])
async def get_users_by_id(
    # user: user_deps,
    uow: UOWDep,
    start: int,
    count: int,
    admin: bool = Depends(admin_access),
):
    stop: int = start+count
    users = await UsersService().find_users_by_id_range(uow, start, stop)
    return users

@router.get("/Account/{id}", response_model=UserSchemaResponse)
async def get_by_id(
    # user: user_deps,
    uow: UOWDep,
    id: int,
    admin: bool = Depends(admin_access),
):
    try:

        user = await UsersService().get_by_id(uow, id)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/Account/{id}", response_model=UserSchema)
async def update_by_id(
    # user: user_deps,
    uow: UOWDep,
    user_update_data: userSchemaEdit,
    id: int,
    admin: bool = Depends(admin_access),
):
    try:
        if(user_update_data.password):
            user_update_data.password = bcrypt_context.hash(user_update_data.password)

        user = await UsersService().update_user(uow, id, user_update_data)

    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

@router.delete("/Account/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_by_id(
    # user: user_deps,
    uow: UOWDep,
    id: int,
    admin: bool = Depends(admin_access),
):
    try:
        
       isDeleted = await UsersService().delete_user_by_id(uow, id) 

    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return isDeleted
