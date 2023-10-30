

from models.users_model import UsersModel
from utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UsersModel
