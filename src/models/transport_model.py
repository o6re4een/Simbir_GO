
from db.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional

from schemas.transport_schema import TransportSchema

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
    # colorId: Mapped[int] = mapped_column(ForeignKey("Color.id"))
    ownerId: Mapped[int | None]= mapped_column(ForeignKey("User.id"), nullable=True)
    # transportTypeId: Mapped[int]= mapped_column(ForeignKey("TransportType.id"))
    # transportModelId: Mapped[int] = mapped_column(ForeignKey("TransportModel.id"))

    # #Relation build
    owner: Mapped[Optional["UsersModel"]] = relationship(back_populates="transport")
    # transportType: Mapped["TransportTypeModel"] = relationship("TransportModel",back_populates="transport")
    # color: Mapped["ColorModel"] = relationship("TransportModel",back_populates="transport")
    # model: Mapped["TransportModelModel"] = relationship("TransportModel",back_populates="transport")


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

            # colorId=self.colorId,
            # modelId=self.transportModelId,
            # transportTypeId=self.transportTypeId,
            

            
        )
