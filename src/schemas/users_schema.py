from datetime import datetime
from pydantic import BaseModel

# from schemas.transport_schema import TransportSchema


#default schema
class UserSchemaBase(BaseModel):
    username: str

#schema to create user   
class UserSchemaCreate(UserSchemaBase):
    password: str
    
class UserSchemaResponse(UserSchemaBase):
    
    balance: float
    isAdmin: bool

    class Config:
        from_attributes = True


class userSchemaEdit(UserSchemaResponse, UserSchemaCreate):
    pass

class UserSchema(UserSchemaCreate, UserSchemaResponse):
    id: int
  

