from datetime import datetime
import enum
from pydantic import BaseModel
# from models.transport_model import *

#base schema

class TransportType(enum.Enum):

    car = "Car"
    bike = "Bike"
    scooter = "Scooter"
    

class TransportSchemaBase(BaseModel):
    
   
    #Basic Columns
    canBeRented: bool
    identifier: str
    latitude: float
    longitude: float

    #Allow nulles
    description: str | None = None
    minutePrice: float | None = None
    dayPrice: float | None = None

    #ForeignKeys 
   


    #Relation build
    # transportType: str
    # model: str

class TransportSchemaCreate(TransportSchemaBase):
    # Values for create 
    model: str
    transportType: str
    color: str
    
class TransportSchemaUpdate(TransportSchemaBase):
    model: str
   
    color: str

class TransportSchemaUpdateAdmin(TransportSchemaUpdate):
    ownerId: int



class TransportSchema(TransportSchemaBase):
   
    id: int
   
    transportTypeId: int
    ownerId: int
    colorId: int
    transportModelId: int
   
    
    class Config:
        from_attributes = True

       

class TrasnportSchemaResponse(TransportSchema):
    
    model: str | None = None
    transportType: str | None = None
    color: str | None = None
    owner: str | None = None
