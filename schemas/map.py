from pydantic import BaseModel
from typing import List

from schemas.base import BaseSchema


class MapSchema(BaseSchema):
    """
        Representa um mapa
        id - Identificador do mapa
        name - Nome do mapa
        points - Quantidade de pontos de interesse do mapa
        description - Descrição do mapa
        creation_date - Data de criação do mapa
        update_date - Data de atualização do mapa
    """
    id: int = 1
    name: str = "Mapa"
    points: int = 10
    description: str = "Descrição do mapa aqui"
    creation_date: str = "2021-01-01T00:00:00"
    update_date: str = "2021-01-01T00:00:00"


class FindMapRequest(BaseModel):
    """Representa a requisição para buscar um mapa"""
    id: int = 1


class UpsertMapRequest(BaseModel):
    """
        Representa a requisição para criar ou atualizar um mapa
        id - Identificador do mapa, se for -1 um novo mapa é criado
        name - Nome do mapa
        description - Descrição do mapa
    """
    id: int = -1
    name: str = "Mapa"
    description: str = "Descrição do mapa aqui"


class UpsertMapResponse(BaseSchema):
    """
        Representa a resposta para criar ou atualizar um mapa
        map - Mapa criado ou atualizado
        message - Mensagem de sucesso ou erro
    """
    message: str = "Mapa criado com sucesso"
    map: MapSchema


class ListMapResponse(BaseSchema):
    """
        Representa a resposta para listar todos os mapas
        maps - Lista de mapas
        message - Mensagem de sucesso ou erro
    """
    maps: List[MapSchema]
    message: str = "Lista de mapas obtida com sucesso"
