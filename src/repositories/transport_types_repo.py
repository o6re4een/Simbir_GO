from models.transport_model import  TransportTypeModel
from utils.repository import SQLAlchemyRepository


class TransportTypeRepository(SQLAlchemyRepository):
    model = TransportTypeModel
