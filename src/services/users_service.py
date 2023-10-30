
    
from schemas.users_schema import UserSchema, UserSchemaCreate, UserSchemaResponse
from utils.unitofwork import IUnitOfWork


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UserSchemaCreate):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def get_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users
        
    async def get_by_username(self, uow: IUnitOfWork, username):
        async with uow:
            user = await uow.users.find_one(username=username)
            return user
        
    async def get_by_id(self, uow: IUnitOfWork, id) :
        async with uow:
            user = await uow.users.find_one(id=id)
            return user
        
    async def update_user(self, uow: IUnitOfWork, user_id:int,  user_data):
        async with uow:
            update_data_dict = user_data.model_dump(exclude_unset=True)
            updated_user = await uow.users.edit_one(user_id, update_data_dict)

            await uow.commit()
            return updated_user
           
    async def find_users_by_id_range(self, uow: IUnitOfWork, start_id: int, end_id: int):
        async with uow:
            users = await uow.users.find_by_id_range(start_id, end_id)
            return users
    
           
    async def delete_user_by_id(self, uow: IUnitOfWork, id:int):
        async with uow:
            res= await uow.users.delete_by_id(id)
            await uow.commit()
            return res
    