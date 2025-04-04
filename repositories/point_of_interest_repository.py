from datetime import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from exceptions.not_found_exception import NotFoundException
from exceptions.validation_exception import ValidationException
from models import PointOfInterest
from sqlalchemy.orm import Session

class PointOfInterestRepository:
    """Define o acesso a base de dados para entidade de ponto de interesse de um mapa"""
    
    def list_all(self, session: Session, map_id: int) -> List[PointOfInterest]:
        """
        Busca todos os pontos de interesse de um mapa
        Arguments:
            session: sessão de acesso ao banco de dados
            map_id: id do mapa a ser buscado
        Returns: Lista de pontos de interesse encontrados
        """
        points = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id).all()
        return points
    
    def create(self, session: Session, map_id: int, name: str, description: str, latitude: float, longitude: float) -> PointOfInterest:
        """
        Cria um novo ponto de interesse em um mapa
        Arguments:
            session: sessão de acesso ao banco de dados
            map_id: id do mapa dono do ponto de interesse
            name: nome do ponto de interesse a ser criado
            description: descrição do ponto de interesse a ser criado
            latitude: coordenada de latitude em WGS64 do ponto de interesse
            longitude: coordenada de longitude em WGS64 do ponto de interesse
        Returns: Ponto de interesse criado
        """
        self.__validate(map_id, name, description, latitude, longitude)
        max_id = session.query(func.max(PointOfInterest.id)).filter(PointOfInterest.map_id == map_id).scalar()
        max_id = (max_id or 0) + 1
        new_point = PointOfInterest(max_id, map_id, name, description, latitude, longitude)
        session.add(new_point)
        return new_point
    
    def update(self, session: Session, map_id: int, id: int, name: str, description: str, latitude: int, longitude: int) -> PointOfInterest:
        """
        Atualiza um ponto de interesse no mapa
        Arguments:
            session: sessão de acesso ao banco de dados
            map_id: id do mapa dono do ponto de interesse
            id: id do ponto de interesse a ser atualizado
            name: nome do ponto de interesse a ser atualizado
            description: descrição do ponto de interesse a ser atualizado
            latitude: coordenada de latitude em WGS64 do ponto de interesse
            longitude: coordenada de longitude em WGS64 do ponto de interesse
        Returns: Ponto de interesse atualizado
        """
        self.__validate(map_id, name, description, latitude, longitude)
    
        point_of_interest_to_update = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id, PointOfInterest.id == id).first()
        if(point_of_interest_to_update == None):
            raise NotFoundException(f"Ponto de interesse não encontrado")
        point_of_interest_to_update.name = name
        point_of_interest_to_update.description = description
        point_of_interest_to_update.latitude = latitude
        point_of_interest_to_update.longitude = longitude
        return point_of_interest_to_update

    def delete_by_map_id(self, session: Session, map_id: int) -> int:
        """
        Remove todos os pontos de interesse de um mapa e retorna o nome do mapa que foi removido
        Arguments:
            session: sessão de acesso ao banco de dados
            map_id: id do mapa dono do ponto de interesse
        Returns: Nome do mapa removido
        """
        points_of_interest_to_delete = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id).all()
        for point in points_of_interest_to_delete:
            session.delete(point)
        return len(points_of_interest_to_delete)

    def delete(self, session: Session, map_id: int, id: int) -> str:
        """Remove um ponto de interesse do mapa"""
        point_of_interest_to_delete = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id, PointOfInterest.id == id).first()
        if(point_of_interest_to_delete == None):
            raise NotFoundException(f"Ponto de interesse não encontrado")
        name = point_of_interest_to_delete.name
        session.delete(point_of_interest_to_delete)
        return name
    
    def __validate(self, map_id: int, name: str, description: str, latitude: float, longitude: float):
        """Faz as validações do ponto de interesse"""
        if(map_id == None or map_id < 0):
            raise ValidationException(f"O mapa dono do ponto de interesse não foi informado")
        if(name == None or name == ""):
            raise ValidationException(f"O nome do ponto não pode ser vazio")
        if(len(name) > 256):
            raise ValidationException(f"O nome do ponto não pode ter mais que 256 caracteres")
        if(len(description)>2000):
            raise ValidationException(f"A descrição do ponto não pode ter mais que 2000 caracteres")
        if(latitude == None):
            raise ValidationException(f"Latitude do ponto não pode ser vazia")
        if(longitude == None):
            raise ValidationException(f"Longitude do ponto não pode ser vazia")