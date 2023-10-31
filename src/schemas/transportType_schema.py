from datetime import datetime
from pydantic import BaseModel

#default schema
class TransportTypeSchemaBase(BaseModel):
    value: str

#schema to create transport type   
class TransportTypeSchemaCreate(TransportTypeSchemaBase):
    pass
    

#chema to read data from table
class TransportTypeSchema(TransportTypeSchemaBase):
    
    id: int
    value: str
    # transport: list["TransportSchema"] = []
    class Config:
        from_attributes = True
