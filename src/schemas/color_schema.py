from datetime import datetime
from pydantic import BaseModel




#default schema
class ColorSchemaBase(BaseModel):
    value: str

#schema to create transport type   
class ColorSchemaCreate(ColorSchemaBase):
    pass
    

#chema to read data from table
class ColorSchema(ColorSchemaBase):
    
    id: int
    value: str
    transport: list["TransportSchema"] = []

    class Config:
        from_attributes = True
