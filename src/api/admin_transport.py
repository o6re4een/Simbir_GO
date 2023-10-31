from typing import Annotated, Callable
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy
from api.auth_logic import admin_access, bcrypt_context
from api.deps import UOWDep
from schemas.transport_schema import TransportSchema, TransportSchemaUpdate, TransportSchemaUpdateAdmin
from services.transport_service import TransportService
# from schemas.users_schema import UserSchema, UserSchemaResponse, userSchemaEdit
# from services.users_service import UsersService


#admin jwt
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlkIjoxMiwiYWRtaW4iOnRydWUsImV4cCI6MTY5ODc1NjIyMH0.MDQA0xYjVOGXbaW5kJ-N0e6elToODbbjadRFbeI-vKI

# user jwt = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiaWQiOjE0LCJhZG1pbiI6ZmFsc2UsImV4cCI6MTY5ODc1NzY4Nn0.Yzn5nW6I8aCQxiKH88akisw-N06sNxOrhTeU4jhq-V8

router = APIRouter(
    prefix="/Admin/Transport",
    tags=["AdminTransportController"],
)



@router.get("", response_model=list[TransportSchema])
async def find_transport_by_id_range(
    # user: user_deps,
    uow: UOWDep,
    start: int,
    count: int,
    type: str,
    admin: bool = Depends(admin_access),
):
    stop: int = start+count
    try:
        transport = await TransportService().find_transport_by_id_range(uow, start, stop, type)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No that type")
    return transport

@router.get("/{id}", )
async def get_transport_by_id(
    # user: user_deps,
    uow: UOWDep,
    id:int,
    admin: bool = Depends(admin_access),
):
    
    transport = await TransportService().get_transport_by_id(uow, id)
    return transport



@router.put("/{id}", )
async def update_transport(
    uow: UOWDep,
    transport_data: TransportSchemaUpdateAdmin,
    id: int,
    admin: bool = Depends(admin_access),
    ):
    
    transport = await TransportService().update_transport(uow, id, transport_data)
    return transport 



@router.delete("/{id}", )
async def delete_transport(
    uow: UOWDep,
    id: int,
    admin: bool = Depends(admin_access),
    ):

       
    transport = await TransportService().delete_transport_by_id(uow, id)
    return transport 
