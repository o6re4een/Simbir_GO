from datetime import datetime
from pydantic import BaseModel


#default schema
class TransportModelSchemaBase(BaseModel):
    value: str

#schema to create transport type   
class TransportModelCreate(TransportModelSchemaBase):
    pass
    

#chema to read data from table
class TransportModelSchema(TransportModelSchemaBase):
    
    id: int
    value: str
    
    # transport: list["TransportSchema"] = []

    class Config:
        from_attributes = True
