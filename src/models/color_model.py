from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional

from schemas.color_schema import ColorSchema




class ColorModel(Base):
    __tablename__ = "Color"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] 

    #Relation Many-to-one
    transport: Mapped[List["TransportModel"]] = relationship("ColorModel",back_populates="color")

    def to_read_model(self) -> ColorSchema:
        return ColorSchema(
           id=self.id,
           value=self.value,
           transport=self.transport,
            
        )
