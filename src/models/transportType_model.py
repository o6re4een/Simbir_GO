
    
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional


from schemas.transportType_schema import TransportTypeSchema


class TransportTypeModel(Base):
    __tablename__ = "TransportType"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("TransportTypeModel",back_populates="transportType")

    def to_read_model(self) -> TransportTypeSchema:
        return TransportTypeSchema(
            id=self.id,
            value=self.value,
            transport=self.transport, 
        )
