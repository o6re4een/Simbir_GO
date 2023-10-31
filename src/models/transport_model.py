
from db.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional
# from models import *
from schemas.transport_schema import TransportSchema
from schemas.color_schema import ColorSchema
from schemas.transportType_schema import TransportTypeSchema
from schemas.transportModel_schema import TransportModelSchema
# from models.transportModel_model import TransportModelModel
# from models.users_model import UsersModel
# from models.color_model import ColorModel
# from models.transportType_model import TransportTypeModel



class TransportModel(Base):
    __tablename__ = "Transport"


    id: Mapped[int] = mapped_column(primary_key=True)
  

    #Basic Columns
    canBeRented: Mapped[bool] = mapped_column(default=True)
    identifier: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]


    #Allow nulles
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    minutePrice: Mapped[Optional[float]] = mapped_column(nullable=True)
    dayPrice: Mapped[Optional[float]] =  mapped_column(nullable=True)
    

    #ForeignKeys 
    colorId: Mapped[int] = mapped_column(ForeignKey("Color.id"))
    ownerId: Mapped[int]= mapped_column(ForeignKey("User.id"))
    transportTypeId: Mapped[int]= mapped_column(ForeignKey("TransportType.id"))
    transportModelId: Mapped[int] = mapped_column(ForeignKey("TransportModel.id"))

    # #Relation build
    owner: Mapped[Optional["UsersModel"]] = relationship("UsersModel", back_populates="transport")
    transportType:  Mapped["TransportTypeModel"] = relationship("TransportTypeModel", back_populates="transport")
    color: Mapped["ColorModel"] = relationship("ColorModel",back_populates="transport")
    model: Mapped["TransportModelModel"] = relationship("TransportModelModel", back_populates="transport")


    def to_read_model(self) -> TransportSchema:
        return TransportSchema(
            id=self.id,
            canBeRented=self.canBeRented,
            identifier=self.identifier,
            latitude=self.latitude,
            longitude=self.longitude,
            description=self.description,
            minutePrice=self.minutePrice,
            dayPrice=self.dayPrice,
            
            ownerId=self.ownerId,
            colorId=self.colorId,
            transportModelId=self.transportModelId,
            transportTypeId=self.transportTypeId,

            # owner= self.owner,
            # transportType=self.transportType,
            # color=self.color,
            # model=self.model
            

            
        )


class ColorModel(Base):
    __tablename__ = "Color"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("TransportModel",back_populates="color")

    def to_read_model(self) -> ColorSchema:
        return ColorSchema(
           id=self.id,
           value=self.value,
        #    transport=self.transport,
            
        )


class TransportTypeModel(Base):
    __tablename__ = "TransportType"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("TransportModel",back_populates="transportType")

    def to_read_model(self) -> TransportTypeSchema:
        return TransportTypeSchema(
            id=self.id,
            value=self.value,
            # transport=self.transport, 
        )


class TransportModelModel(Base):
    __tablename__ = "TransportModel"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("TransportModel",back_populates="model")

    def to_read_model(self) -> TransportModelSchema:
        return TransportModelSchema(
           id=self.id,
           value=self.value,
        #    transport=self.transport,
            
        )
