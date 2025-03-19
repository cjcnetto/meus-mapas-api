from logging import Logger
from typing import List
from models.point_of_interest import PointOfInterest
from repositories.map_repository import MapRepository
from repositories.point_of_interest_repository import PointOfInterestRepository
from schemas import *

class PointOfInterestService:
    """Serviço que trata as regras de negócio para o ponto de interesse, faz o meio de campo para entrega de dados entre o repositório e a API"""
    def __init__(self, map_repository: MapRepository, point_of_interest_repository: PointOfInterestRepository, logger: Logger):
        self.map_repository = map_repository
        self.point_of_interest_repository = point_of_interest_repository
        self.logger = logger

    def list_all(self, findMap: FindMapRequest) -> ListPointOfInterestResponse:
        """Get all points of interest in a map"""
        try:
            self.logger.info(f"list all points of interest called with map id {findMap.id}")
            map = self.map_repository.find_by_id(findMap.id)
            if(map == None):   
                self.logger.error(f"Map '{findMap.id}' not found")
                raise ValueError("Map not found")
            points = self.point_of_interest_repository.list_all(findMap.id)
            if not points or len(points) == 0:
                self.logger.info(f"No points of interest found")
                return ListPointOfInterestResponse(map_name=map.name, map_description=map.description,message="No points found", points=[])
            else:
                self.logger.info(f"%d Map {map.name} desc: {map.description} Points found " % len(points))
                return self.__convert_points_to_schema(map.name, map.description, points, message="Points of interest found")
        except Exception as e:
            self.logger.error(f"Cannot list points of interest",exc_info=True)
            return ListPointOfInterestResponse(map_name="", map_description="",message="Error in the list of points of interest", points=[])
    
    def upsert(self, request: UpsertPointOfInterestRequest) -> UpsertPointOfInterestResponse:
        """Add or update a point of interest to the database by its id, if the id is not present a new point of interest is created"""
        id = request.id
        self.logger.info(f"upsert point called {id}")

        #check if a map with the same name exists
        map = self.map_repository.find_by_id(request.map_id)
        if(map == None):   
            self.logger.error(f"Map '{request.map_id}' not found")
            raise ValueError("Map not found")
        action = ""
        point = None
        try:
            if(id != None and id >= 0):
                action = "update"
                self.logger.info(f"Updating point '{id}'")
                point = self.point_of_interest_repository.update(request.map_id, request.id, request.name, request.description, request.latitude, request.longitude)
            else:
                action = "create"
                self.logger.info(f"Creating new point '{request.name}', '{request.description}'")
                point = self.point_of_interest_repository.create(request.map_id, request.name, request.description, request.latitude, request.longitude)
            pointSchema = self.__convert_point_to_schema(point)
            return UpsertPointOfInterestResponse(message=f"Ponto criado com sucesso", point_of_interest=pointSchema)
        except Exception as e:
            self.logger.error(f"Cannot {action} point MAP: '{map.name}' - '{request.name}', '{request.description}'",exc_info=True)

            raise ValueError("Cannot create point of interest")
            
    def delete(self, id_schema: FindPointOfInterestRequest) -> DelSchema:
        """Delete a point by its id"""
        map_id = getattr(id_schema, 'map_id', None)
        self.logger.info(f"delete point called with id {map_id} and point id {id_schema.id}")
        if(map_id == None):
            self.logger.error("delete_map called without id")
            raise ValueError("Map not found")
        
        map = self.map_repository.find_by_id(map_id)
        if(map == None):
            self.logger.error(f"Map '{map_id}' not found")
            raise ValueError("Map not found")
        name = None
        message = None
        try:    
            name = self.point_of_interest_repository.delete(map_id, id_schema.id)
            name = f"{map.name} - {name}"
            message = "Ponto removido com sucesso."
        except Exception as e:
            self.logger.error(f"Cannot delete point '{map_id}' '{id_schema.id}'",exc_info=True)
            message = "Erro ao remover mapa"
        return DelSchema(mesage=message, name=name)

    def __convert_point_to_schema(self, point: PointOfInterest):
        return PointOfInterestSchema(
            map_id=point.map_id,
            id=point.id,
            name=point.name,
            description=point.description,
            latitude=point.latitude,
            longitude=point.longitude,
            creation_date=point.creation_date.strftime("%Y-%m-%d %H:%M:%S"), 
            update_date=point.update_date.strftime("%Y-%m-%d %H:%M:%S")
        )

    def __convert_points_to_schema(self, map_name: str, map_description: str, points: List[PointOfInterest], message: str):
        return ListPointOfInterestResponse(
            message=message,
            map_name=map_name,
            map_description=map_description,
            points=[self.__convert_point_to_schema(point) for point in points])