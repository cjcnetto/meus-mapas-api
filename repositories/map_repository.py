from typing import List
from exceptions.not_found_exception import NotFoundException
from exceptions.validation_exception import ValidationException
from models import Map
from sqlalchemy.orm import Session


class MapRepository:
    """Define o acesso a base de dados para a entidade de mapa"""

    def find_by_id(self, session: Session, id: int) -> Map:
        """
        Busca um mapa pelo seu ID
        Arguments:
            session: sessão de acesso ao banco de dados
            id: id do mapa a ser buscado
        Returns: Mapa encontrado ou None se não encontrado
        """
        map = session.query(Map).filter(Map.id == id).first()
        return map

    def find_by_name(self, session: Session, name: str) -> Map:
        """
        Busca um mapa pelo seu nome
        Arguments:
            session: sessão de acesso ao banco de dados
            name: nome do mapa a ser buscado
        Returns: Mapa encontrado ou None se não encontrado
        """
        map = session.query(Map).filter(Map.name == name).first()
        return map

    def list_all(self, session: Session) -> List[Map]:
        """
        Busca todos os mapas cadastrados na base
        Arguments:
            session: sessão de acesso ao banco de dados
        Returns: Lista de mapas encontrados
        """
        maps = session.query(Map).all()
        return maps

    def create(self, session: Session, name: str, description: str) -> Map:
        """
        Cria um mapa novo
        Arguments:
            session: sessão de acesso ao banco de dados
            name: nome do mapa a ser criado
            description: descrição do mapa a ser criado
        Returns: Mapa criado
        """
        self.__validate_name(name)
        self.__validate_description(description)
        new_map = Map(name=name, description=description)
        session.add(new_map)
        return new_map

    def update(self, session: Session, id: int,
               name: str, description: str) -> Map:
        """
        Atualiza um mapa existente
        Arguments:
            session: sessão de acesso ao banco de dados
            id: id do mapa a ser atualizado
            name: novo nome do mapa
            description: nova descrição do mapa
        Returns: Mapa atualizado
        """
        self.__validate_name(name)
        self.__validate_description(description)
        map_to_update = session.query(Map).filter(Map.id == id).first()
        if (map_to_update is None):
            raise NotFoundException("Mapa não encontrado")
        map_to_update.name = name
        map_to_update.description = description
        return map_to_update

    def delete(self, session: Session, id: int) -> str:
        """
        Remove um mapa existente e retorna o nome do mapa que foi removido
        Arguments:
            session: sessão de acesso ao banco de dados
            id: id do mapa a ser removido
        Returns: Nome do mapa removido
        """
        map_to_delete = session.query(Map).filter(Map.id == id).first()
        if (map_to_delete is None):
            raise NotFoundException("Mapa não encontrado")
        name = map_to_delete.name
        session.delete(map_to_delete)
        return name

    def __validate_name(self, name: str):
        """Valida as constraints do nome do mapa.
        Não deve ser maior que 256 e não ser vazio"""
        if (name is None or name == ""):
            raise ValidationException("O nome do mapa não pode ser vazio")
        if (len(name) > 256):
            raise ValidationException(
                "O nome do mapa não pode ter mais que 256 caracteres"
            )

    def __validate_description(self, description: str):
        """Validates the size of the description"""
        if (len(description) > 2000):
            raise ValidationException(
                "A descrição do mapa não pode ter mais que 2000 caracteres"
                )
