from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, PrimaryKeyConstraint, Sequence
from datetime import datetime
from models import Base

class PointOfInterest(Base):
    __tablename__ = 'point_of_interest'

    id = Column(Integer, nullable=False)  # Chave primária
    map_id = Column(Integer, ForeignKey('map.pk_map'), nullable=False) # Chave estrangeira e segunda chave primaria
    name = Column(String(256), nullable=False)
    description = Column(String(2000))
    creation_date = Column(DateTime, default=lambda: datetime.now())
    update_date = Column(DateTime, default=lambda: datetime.now())
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'map_id'),  # Chave composta
    )

    def __init__(self, id: int, map_id: int, name: str, description: str, latitude: float, longitude: float):
        self.id = id
        self.map_id = map_id
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
