from datetime import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
from models import Session, Map

class MapRepository:
    """Defines the repository that handles the map data it is responsable to handles with the database"""
    
    def find_by_id(self, id: int) -> Map:
        """Finds a map by its id"""
        session = Session()
        map = session.query(Map).filter(Map.id == id).first()
        session.close()
        return map
    
    def find_by_name(self, name: str) -> Map:
        """Finds a map by its name"""
        session = Session()
        map = session.query(Map).filter(Map.name == name).first()
        session.close()
        return map

    def list_all(self) -> List[Map]:
        """Finds all maps"""
        session = Session()
        maps = session.query(Map).all()
        session.close()
        return maps
    
    def create(self, name: str, description: str) -> Map:
        """Creates a map"""
        self.__validate_name(name)
        session = Session()
        new_map = Map(name=name, description=description)
        session.add(new_map)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(f"Error to create a new map with name ({map.name}).", e)
        session.refresh(new_map)
        session.close()
        return new_map
    
    def update(self, id: str, name: str, description: str) -> Map:
        """Updates a map"""
        self.__validate_name(name)

        session = Session()
        map_to_update = session.query(Map).filter(Map.id == id).first()
        if(map_to_update == None):
            raise ValueError(f"Map with id '{map.id}' not found.")
        map_to_update.name = name
        map_to_update.description = description
        map_to_update.updated_at = datetime.now()
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(f"Error to create a new map with name ({map.name}).", e)
        session.refresh(map_to_update)
        session.close()
        return map_to_update
    
    def delete(self, id: int) -> str:
        """Deletes a map and returns the name of the maps deleted"""
        session = Session()
        map_to_delete = session.query(Map).filter(Map.id == id).first()
        if(map_to_delete == None):
            raise ValueError(f"Map with id '{id}' not found.")
        name = map_to_delete.name
        session.delete(map_to_delete)
        session.commit()
        session.close()
        return name
    
    def __validate_name(self, name:str):
        """Validates the not null constraint of the map name"""
        if(name == None or name == ""):
            raise ValueError(f"The map name must not be empty to create a new map, receveied name '{name}'")