from pydantic import BaseModel
from typing import Optional, List

from schemas.base import BaseSchema

class MapSchema(BaseSchema):
    """Represents a map"""
    id: int = 1
    name: str = "Mapa"
    description: str = "Map description here"
    creation_date: str = "2021-01-01T00:00:00"
    update_date: str = "2021-01-01T00:00:00"

class FindMapRequest(BaseModel):
    """Represents the request to find a map"""
    id: int = 1

class UpsertRequest(BaseModel):
    """Representes the request to create or update a map"""
    id: Optional[int]
    name: str = "Mapa"
    description: str = "Map description here"

class UpsertResponse(BaseSchema):
    """Represents the response to create or update a map"""
    message: str = "Map created"
    map: MapSchema

class ListMapResponse(BaseSchema):
    """List of maps"""
    maps: List[MapSchema]
    message: str = "Error in the list of maps"