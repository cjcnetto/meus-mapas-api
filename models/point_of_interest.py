from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, PrimaryKeyConstraint
from datetime import datetime
from models import Base

class PointOfInterest(Base):
    __tablename__ = 'point_of_interest'

    id = Column(Integer, nullable=False)
    map_id = Column(Integer, ForeignKey('map.pk_map'), nullable=False)
    name = Column(String(256), nullable=False)
    description = Column(String(2000))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now())
    update_date = Column(DateTime, default=lambda: datetime.now())

    __table_args__ = (
        PrimaryKeyConstraint('id', 'map_id'),  # Chave composta
    )

    def __init__(self, id: int, map_id: int, name: str, description: str, latitude: float, longitude: float):
        """
        Tabela que controla os pontos de interesse criados dentro de um mapa

        Arguments:
            id: Id do ponto de interesse a ser criado dentro do mapa
            map_id: id do mapa dono do ponto de interesse
            name: Nome do ponto de interesse 
            description: Descrição do ponto de interesse
            latitude: Coordenada de latitude em WGS64 do ponto de interesse.
            longitude: Coordenada de longitude em WGS64 do ponto de interesse.
        """
        self.id = id
        self.map_id = map_id
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude