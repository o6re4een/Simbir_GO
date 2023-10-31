from __future__ import annotations
import datetime
from schemas.users_schema import UserSchema
from db.db import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional

# association_table = Table(
#     "User_Rent",
#     Base.metadata,
#     Column("UserId", ForeignKey("Users.id"), primary_key=True),
#     Column("RentId", ForeignKey("Rent.id"), primary_key=True),
# )


class UsersModel(Base):
    __tablename__ = "User"


    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Optional[float]] = mapped_column(default=0)
    isAdmin: Mapped[Optional[bool]] = mapped_column(default=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    transport: Mapped[List["TransportModel"] | None] = relationship("TransportModel",back_populates="owner")
   
    # rents: Mapped[List["RentModel"]] =  relationship(secondary=association_table, back_populates="users")


    # transports: Mapped[List["Transport"]] = relationship()

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            balance=self.balance,
            isAdmin=self.isAdmin,
            username=self.username,
            password=self.password,
           
            
        )



# class RentModel(Base):
#     __tablename__ = "Rent"


#     id: Mapped[int] = mapped_column(primary_key=True)
#     transportId: Mapped[int]

#     timeStart: Mapped[datetime.date]
#     timeEnd: Mapped[datetime.date | None]

#     users: Mapped[List["UsersModel"]] = relationship(secondary=association_table, back_populates="rents")

#     rentType: Mapped[str]
#     finalPrice: Mapped[str | None]