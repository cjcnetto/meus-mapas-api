from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from  models import Base

class Map(Base):
    __tablename__ = 'map'

    id = Column("pk_map", Integer, primary_key=True)
    name = Column(String(256), unique=True)
    description = Column(String(2000), unique=False)
    creation_date = Column(DateTime, default=lambda: datetime.now())
    update_date = Column(DateTime, default=lambda: datetime.now())

    points = relationship("PointOfInterest")
    
    def __init__(self, name:str, description:str):
        """
        Tabela que controla os mapas 

        Arguments:
            name: Name of the map it must be unique
            description: description opf the map
        """
        self.name = name
        self.description = description