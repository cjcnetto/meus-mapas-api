from pydantic import BaseModel
from typing import List

from schemas.base import BaseSchema

class PointOfInterestSchema(BaseSchema):
    """
        Representa um ponto de interesse dentro de um mapa
        map_id - Identificador do mapa ao qual o ponto de interesse pertence
        id - Identificador do ponto de interesse
        name - Nome do ponto de interesse
        description - Descrição do ponto de interesse
        latitude - Latitude em WGS64 do ponto de interesse
        longitude - Longitude em WGS64 do ponto de interesse
        creation_date - Data de criação do ponto de interesse
        update_date - Data de atualização do ponto de interesse
    """
    map_id: int = 1
    id: int = 1
    name: str = "Nome do Ponto de Interesse de um mapa"
    description: str = "Descrição do ponto de interesse aqui"
    latitude: float = 0.0
    longitude: float = 0.0
    creation_date: str = "2021-01-01T00:00:00"
    update_date: str = "2021-01-01T00:00:00"

class FindPointOfInterestRequest(BaseSchema):
    """
        Representa a requisição para buscar um ponto de interesse
        map_id - Identificador do mapa ao qual o ponto de interesse pertence
        id - Identificador do ponto de interesse
    """
    map_id: int = 1
    id: int = 1

class UpsertPointOfInterestRequest(BaseModel):
    """
        Representa a requisição para criar ou atualizar um ponto de interesse
        map_id - Identificador do mapa ao qual o ponto de interesse pertence
        id - Identificador do ponto de interesse, se for -1 um novo ponto de interesse é criado
        name - Nome do ponto de interesse
        description - Descrição do ponto de interesse
        latitude - Latitude em WGS64 do ponto de interesse
        longitude - Longitude em WGS64 do ponto de interesse
    """
    map_id: int = 1
    id: int = -1
    name: str = "Nome do Ponto de Interesse de um mapa"
    description: str = "Descrição do ponto de interesse aqui"
    latitude: float = 0.0
    longitude: float = 0.0

class UpsertPointOfInterestResponse(BaseSchema):
    """
        Representa a resposta para criar ou atualizar um ponto de interesse
        point_of_interest - Ponto de interesse criado ou atualizado
        message - Mensagem de sucesso ou erro
    """
    message: str = "Ponto de Interesse criado com sucesso"
    point_of_interest: PointOfInterestSchema

class ListPointOfInterestResponse(BaseSchema):
    """
        Representa a resposta para listar todos os pontos de interesse de um mapa
        points - Lista de pontos de interesse
        map_name - Nome do mapa ao qual os pontos de interesse pertencem
        map_description - Descrição do mapa ao qual os pontos de interesse pertencem
        message - Mensagem de sucesso ou erro
    """
    points: List[PointOfInterestSchema]
    map_name: str = "Meu Mapa"
    map_description: str = "Descrição do mapa"
    message: str = "Pontos carregados com sucesso"