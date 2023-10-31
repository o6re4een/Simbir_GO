from abc import ABC, abstractmethod
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import between, delete, insert, select, update
from sqlalchemy.orm import lazyload


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplemented

    @abstractmethod
    async def find_all(self):
        raise NotImplemented


class SQLAlchemyRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def add_one(self, data: dict) :
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one().to_read_model()

    async def edit_one(self, id: int, data: dict) :
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one().to_read_model()
    
    async def find_all(self):
        stmt = select(self.model)
        print(self.session)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    
    async def find_one_relation(self, **filter_by):
        
        stmt = select(self.model).filter_by(**filter_by).options(lazyload("*"))
        try:
            res = await self.session.execute(stmt)
            print(res)
            return res.scalar_one().to_read_model()
        except sqlalchemy.exc.NoResultFound:
            return None
    async def find_one(self, **filter_by):
        
        stmt = select(self.model).filter_by(**filter_by)
        try:
            res = await self.session.execute(stmt)
            return res.scalar_one().to_read_model()
        except sqlalchemy.exc.NoResultFound:
            return None
        # res = res.scalar_one().to_read_model()
        return res
    
    async def find_by_id_range(self, start_id: int, end_id: int, **filter_by):
        stmt = select(self.model).where(between(self.model.id, start_id, end_id)).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        users = [row[0].to_read_model() for row in res.all()]
        return users
    
    async def delete_by_id(self, id:int):
        stmt = delete(self.model).where(self.model.id== id)
        res = await self.session.execute(stmt)
        print(res)
        return True
    

    