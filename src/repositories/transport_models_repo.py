from models.transport_model import TransportModelModel

from utils.repository import SQLAlchemyRepository


class TransportModelRepository(SQLAlchemyRepository):
    model = TransportModelModel
