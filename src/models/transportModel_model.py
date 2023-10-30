from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional

from schemas.transportModel_schema import TransportModelSchema






class TransportModelModel(Base):
    __tablename__ = "TransportModel"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("TransportModelModel",back_populates="model")

    def to_read_model(self) -> TransportModelSchema:
        return TransportModelSchema(
           id=self.id,
           value=self.value,
           transport=self.transport,
            
        )
