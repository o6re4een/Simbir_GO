from models.transport_model import ColorModel

from utils.repository import SQLAlchemyRepository


class ColorRepository(SQLAlchemyRepository):
    model = ColorModel
