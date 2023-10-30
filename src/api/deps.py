# from repositories.users_repo import UsersRepository
# from services.users_service import UsersService



# def users_service():
#     return UsersService(UsersRepository)

from typing import Annotated

from fastapi import Depends


from utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
