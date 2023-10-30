
from schemas.users_schema import UserSchema
from db.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional



class UsersModel(Base):
    __tablename__ = "User"


    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Optional[float]] = mapped_column(default=0)
    isAdmin: Mapped[Optional[bool]] = mapped_column(default=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    
   



    # transports: Mapped[List["Transport"]] = relationship()

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            balance=self.balance,
            isAdmin=self.isAdmin,
            username=self.username,
            password=self.password,
           
            
        )
