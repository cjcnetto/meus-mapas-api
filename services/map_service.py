from logging import Logger
from typing import List
from repositories.map_repository import MapRepository
from schemas import *
from models import Map

class MapService:
    """Serviço que trata as regras de negócio para o mapa, faz o meio de campo para entrega de dados entre o repositório e a API"""
    def __init__(self, map_repository: MapRepository, logger: Logger):
        self.map_repository = map_repository
        self.logger = logger
    def get(self, idSchema: FindMapRequest) -> MapSchema:
        """Get a map by its id"""
        id = idSchema.id
        self.logger.info(f"get map called with id {id}")
        if(id == None):
            self.logger.error("get_map called without id")
            raise ValueError("Map not found")
        
        map = self.map_repository.find_by_id(id)
        if(map == None):
            self.logger.error(f"Cannot find map '{id}'")
            raise ValueError(f"Map not found: {id}")
        return self.__convert_map_to_schema(map)

    def list_all(self) -> ListMapResponse:
        """Get all maps"""
        self.logger.info(f"get maps called")
        maps = self.map_repository.list_all()
        if not maps:
            self.logger.info(f"No maps found")
            return ListMapResponse(maps=[], message="Nenhum mapa encontrado")
        else:
            self.logger.info(f"%d Maps found" % len(maps))
            return self.__convert_maps_to_schema(maps)
    
    def upsert(self, request: UpsertRequest) -> UpsertResponse:
        ### Adds or update a map to the database by its id, if the id is not present a new map is created"""
        id = request.id
        self.logger.info(f"upsert map called {id}")

        action = ""
        try:
            if(id != None and id >= 0):
                action = "update"
                self.logger.info(f"Updating map '{id}'")
                map = self.map_repository.update(request.id, request.name, request.description)
            else:
                #check if a map with the same name exists
                map = self.map_repository.find_by_name(request.name)
                if(map != None):
                    self.logger.info(f"Map '{request.name}' already exists") 
                    return UpsertResponse(message="Mapa já existe", map=None)
                action = "create"
                self.logger.info(f"Creating new map '{request.name}', '{request.description}'")
                map = self.map_repository.create(request.name, request.description)
            mapSchema = self.__convert_map_to_schema(map)
            return UpsertResponse(message=f"Mapa aa com sucesso", map=mapSchema)
        except Exception as e:
            self.logger.error(f"Cannot {action} map '{request.name}', '{request.description}'",exc_info=True)
            raise ValueError("Cannot create map")
            
    def delete(self, idSchema: FindMapRequest) -> DelSchema:
        """Delete a map by its id"""
        id = getattr(idSchema, 'id', None)
        self.logger.info(f"delete map called with id {id}")
        if(id == None):
            self.logger.error("delete_map called without id")
            raise ValueError("Map not found")
        name = None
        message = None
        try:
            name = self.map_repository.delete(id)
            message = "Mapa removido com sucesso."
        except Exception as e:
            self.logger.error(f"Cannot delete map '{id}'",exc_info=True)
            message = "Erro ao remover mapa"
        return DelSchema(message, name=name)

    def __convert_map_to_schema(self, map: Map):
        return MapSchema(
            id=map.id, 
            name=map.name, 
            description=map.description, 
            creation_date=map.creation_date.strftime("%Y-%m-%d %H:%M:%S"), 
            update_date=map.update_date.strftime("%Y-%m-%d %H:%M:%S"))

    def __convert_maps_to_schema(self, maps: List[Map]):
        return ListMapResponse(
            maps=[self.__convert_map_to_schema(map) for map in maps])