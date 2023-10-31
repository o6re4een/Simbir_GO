


from models.transport_model import TransportModel
from utils.repository import SQLAlchemyRepository


class TransportRepository(SQLAlchemyRepository):
    model = TransportModel
