from datetime import datetime
from pydantic import BaseModel

#base schema
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
    transportTypeId: int
    ownerId: int
    colorId: int
    modelId: int

    #Relation build
    # transportType: TransportTypeSchema

class TransportSchemaCreate(BaseModel):
    pass

class TransportSchema(TransportSchemaBase):
   
    id: int
  

    #Allow nulles
    

    #ForeignKeys 
    # owner: int
    # transportTypeId: int
   
    
    class Config:
        from_attributes = True



       

