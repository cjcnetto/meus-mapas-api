from logging import Logger
from typing import List
from exceptions.not_found_exception import NotFoundException
from exceptions.validation_exception import ValidationException
from models.point_of_interest import PointOfInterest
from repositories import MapRepository, PointOfInterestRepository, BaseMyMapException
from schemas import *
from models import Map, Session

class MapService:
    """Serviço que trata as regras de negócio para o mapa, com seus pontos"""
    def __init__(self, map_repository: MapRepository, point_of_interest_repository: PointOfInterestRepository, logger: Logger):
        self.map_repository = map_repository
        self.point_of_interest_repository = point_of_interest_repository
        self.logger = logger

    def list_all_maps(self) -> ListMapResponse:
        """Retorna todos os mapas cadastrados na base"""
        self.logger.info(f"get maps called")
        session = Session()
        try:
            maps = self.map_repository.list_all(session)
            mapsSchema = []
            if not maps:
                self.logger.info(f"No maps found")
                message = "Nenhum mapa encontrado"
            else:            
                self.logger.info(f"%d Maps found" % len(maps))
                message = f"Total de mapas encontrados {len(maps)}"
                for map in maps:
                    mapsSchema.append(self.__convert_map_to_schema(map))
            return ListMapResponse(maps=mapsSchema, message=message)
        except Exception as e:
            self.logger.error(f"Cannot get maps", exc_info=True)
            raise Exception("Houve um erro inesperado ao buscar os mapas")
        finally:
            session.close()

    def upsert_map(self, request: UpsertMapRequest) -> UpsertMapResponse:
        """Atualiza ou cria um mapa """
        id = request.id
        self.logger.info(f"upsert map called {id}")
        action = ""
        session = Session()
        try:
            #Checa se o mapa já existe
            if(id != None and id >= 0):
                self.logger.info(f"Updating map '{id}'")
                action = "update"
                map = self.map_repository.update(session, request.id, request.name, request.description)
            else:
                map = self.map_repository.find_by_name(session, request.name)
                if(map != None):
                    self.logger.info(f"Map '{request.name}' already exists") 
                    raise ValidationException(message=f"Mapa com o nome {request.name} já existe")
                self.logger.info(f"Creating new map '{request.name}', '{request.description}'")
                action = "create"                
                map = self.map_repository.create(session, request.name, request.description)
            session.commit()
            mapSchema = self.__convert_map_to_schema(map)
            return UpsertMapResponse(message=f"Mapa criado com sucesso", map=mapSchema)
        except BaseMyMapException as e:
            self.logger.error(f"Cannot get maps", exc_info=True)
            session.rollback()
            raise e
        except Exception as e:
            self.logger.error(f"Cannot {action} map '{request.name}', '{request.description}'",exc_info=True)
            session.rollback()
            actionText = "criar" if(action == "create") else "atualizar"
            raise Exception(f"Não foi possível {actionText} o mapa")
        finally:
            session.close()
            
    def delete(self, id_schema: FindMapRequest) -> DelSchema:
        """Remove um mapa"""
        self.logger.info(f"delete map called with id {id_schema.id}")
        if(id_schema.id == None):
            self.logger.error("delete_map called without id")
            raise ValidationException("O id deve ser informado")
        session = Session()
        try:
            points = self.point_of_interest_repository.delete_by_map_id(session, id_schema.id)
            name = self.map_repository.delete(session, id_schema.id)
            session.commit()
            message = f"Mapa removido com sucesso. Com {points} pontos de interesse removidos."
            return DelSchema(message=message, name=name)
        except BaseMyMapException as e:
            self.logger.error(f"Cannot delete maps", exc_info=True)
            session.rollback()
            raise e        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Cannot delete map '{id_schema.id}'",exc_info=True)
            message = "Erro ao remover mapa"
            raise Exception(message)
        finally:
            session.close()

    def __convert_map_to_schema(self, map: Map):
        return MapSchema(
            id=map.id, 
            name=map.name, 
            description=map.description, 
            points= len(map.points),
            creation_date=map.creation_date.strftime("%Y-%m-%d %H:%M:%S"), 
            update_date=map.update_date.strftime("%Y-%m-%d %H:%M:%S"))
    
    def list_all_points(self, findMap: FindMapRequest) -> ListPointOfInterestResponse:
        """Retorna todos os pontos de interesse cadastrados para um mapa na base"""
        self.logger.info(f"list all points of interest called with map id {findMap.id}")
        try:
            session = Session()
            map = self.map_repository.find_by_id(session, findMap.id)
            if(map == None):   
                self.logger.error(f"Map '{findMap.id}' not found")
                raise NotFoundException("Map não encontrado para os pontos")
            points = self.point_of_interest_repository.list_all(session, findMap.id)
            if not points or len(points) == 0:
                self.logger.info(f"No points of interest found")
                return ListPointOfInterestResponse(map_name=map.name, map_description=map.description,message="Mapa sem pontos", points=[])
            else:
                self.logger.info(f"%d Map {map.name} desc: {map.description} Points found " % len(points))
                return self.__convert_points_to_schema(map.name, map.description, points, message=f"Pontos encontrados {len(points)}")
        except Exception as e:
            self.logger.error(f"Cannot list points of interest",exc_info=True)
            raise Exception("Houve um erro inesperado ao buscar os pontos de interesse")
        finally:
            session.close()

    def upsert_point(self, request: UpsertPointOfInterestRequest) -> UpsertPointOfInterestResponse:
        """Atualiza ou cria um ponto de interesse no mapa"""
        id = request.id
        self.logger.info(f"upsert point called {id}")
        session = Session()
        try:
            map = self.map_repository.find_by_id(session, request.map_id)
            if(map == None):   
                self.logger.error(f"Map '{request.map_id}' not found")
                raise ValueError("Map not found")
            action = ""
            point = None
            if(id != None and id >= 0):
                action = "update"
                self.logger.info(f"Updating point '{request.map_id}'-'{id}'")
                point = self.point_of_interest_repository.update(session, request.map_id, request.id, request.name, request.description, request.latitude, request.longitude)
            else:
                action = "create"
                self.logger.info(f"Creating new point MAP: '{request.map_id}' - '{request.name}', '{request.description}' lat: '{request.latitude}' long: '{request.longitude}'")
                point = self.point_of_interest_repository.create(session, request.map_id, request.name, request.description, request.latitude, request.longitude)
            session.commit()
            pointSchema = self.__convert_point_to_schema(point)            
            return UpsertPointOfInterestResponse(message=f"Ponto criado com sucesso", point_of_interest=pointSchema)
        except BaseMyMapException as e:
            self.logger.error(f"Cannot get maps", exc_info=True)
            session.rollback()
            raise e
        except Exception as e:
            self.logger.error(f"Cannot {action} point '{request.name}', '{request.description}'",exc_info=True)
            session.rollback()
            action = "criar" if(action == "create") else "atualizar"
            raise Exception(f"Não foi possível {action} o ponto de interesse")
        finally:
            session.close()
        
    def delete_point(self, id_schema: FindPointOfInterestRequest) -> DelSchema:
        """Remove um ponto de interesse pelo seu id de mapa e seu id"""
        map_id = getattr(id_schema, 'map_id', None)
        self.logger.info(f"delete point called with id {map_id} and point id {id_schema.id}")
        if(map_id == None):
            self.logger.error("delete_map called without id")
            raise ValueError("Map not found")
        session = Session()
        name = None
        message = None    
        try:    
            map = self.map_repository.find_by_id(session, map_id)
            if(map == None):
                self.logger.error(f"Map '{map_id}' not found")
                raise ValueError("Map not found")
            name = self.point_of_interest_repository.delete(session, map_id, id_schema.id)
            session.commit()
            name = f"{map.name} - {name}"
            message = "Ponto removido com sucesso."
            return DelSchema(message=message, name=name)
        except BaseMyMapException as e:
            self.logger.error(f"Cannot delete maps", exc_info=True)
            session.rollback()
            raise e        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Cannot delete map '{id_schema.id}'",exc_info=True)
            message = "Erro ao remover mapa"
            raise Exception(message)
        finally:
            session.close()

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
