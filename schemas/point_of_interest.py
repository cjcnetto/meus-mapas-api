from pydantic import BaseModel
from typing import Optional, List

from schemas.base import BaseSchema

class PointOfInterestSchema(BaseSchema):
    map_id: int = 1
    id: int = 1
    name: str = "Point of interest"
    description: str = "Point of interest description here"
    latitude: int = 0
    longitude: int = 0
    creation_date: str = "2021-01-01T00:00:00"
    update_date: str = "2021-01-01T00:00:00"

class FindPointOfInterestRequest(BaseSchema):
    map_id: int = 1
    id: int = 1

class UpsertPointOfInterestRequest(BaseModel):
    """Representes the request to create or update a point of interest"""
    map_id: int = 1
    id: Optional[int]
    name: str = "Point of interest"
    description: str = "Point of interest description here"
    latitude: float = 0.0
    longitude: float = 0.0

class UpsertPointOfInterestResponse(BaseSchema):
    """Represents the response to create or update a point of interest"""
    message: str = "Map created"
    point_of_interest: PointOfInterestSchema

class ListPointOfInterestResponse(BaseSchema):
    """List of maps"""
    points: List[PointOfInterestSchema]
    map_name: str = "Meu Mapa"
    map_description: str = "Descrição do mapa"
    message: str = "Error in the list of maps"
