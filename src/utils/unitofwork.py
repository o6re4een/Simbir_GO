from abc import ABC, abstractmethod
from typing import Type

from db.db import async_session_maker
from repositories.color_repo import ColorRepository
from repositories.transport_models_repo import TransportModelRepository
from repositories.transport_repo import TransportRepository
from repositories.transport_types_repo import TransportTypeRepository
from repositories.users_repo import UsersRepository



# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    transport: Type[TransportRepository]
    transport_types: Type[TransportTypeRepository]
    transport_models: Type[TransportModelRepository]
    colors: Type[ColorRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.transport = TransportRepository(self.session)
        self.users = UsersRepository(self.session)
        self.transport_types = TransportTypeRepository(self.session)
        self.transport_models = TransportModelRepository(self.session)
        self.colors = ColorRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()