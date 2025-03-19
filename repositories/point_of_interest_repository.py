from datetime import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from models import Session, PointOfInterest

class PointOfInterestRepository:
    """Defines the repository that handles the point of interest data it is responsable to handles with the database"""
    
    def find_by_id(self, map_id: int, pointId: int) -> PointOfInterest:
        """Finds a map by its id"""
        session = Session()
        point = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id, PointOfInterest.id == pointId).first()
        session.close()
        return point
    
    def list_all(self, map_id: int) -> List[PointOfInterest]:
        """Finds all points of interest in a map"""
        session = Session()
        points = session.query(PointOfInterest).filter(PointOfInterest.map_id == map_id).all()
        session.close()
        return points
    
    def create(self, mapId: int, name: str, description: str, latitude: float, longitude: float) -> PointOfInterest:
        """Creates a map"""
        session = Session()
        max_id = session.query(func.max(PointOfInterest.id)).filter(PointOfInterest.map_id == mapId).scalar()
        max_id = (max_id or 0) + 1
        new_point = PointOfInterest(max_id, mapId, name, description, latitude, longitude)
        session.add(new_point)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(f"Error to create a new point with mapId ({mapId}).", e)
        session.refresh(new_point)
        session.close()
        return new_point
    
    def update(self, mapId: int, id: int, name: str, description: str, latitude: int, longitude: int) -> PointOfInterest:
        """Updates a map"""
        if(name == None or name == ""):
            raise ValueError("Name is required.")
        if(latitude == None or latitude == ""):
            raise ValueError("Latitude is required.")
        if(longitude == None or longitude == ""):
            raise ValueError("Longitude is required.")
        
        session = Session()
        point_of_interest_to_update = session.query(PointOfInterest).filter(PointOfInterest.map_id == mapId, PointOfInterest.id == id).first()
        if(point_of_interest_to_update == None):
            raise ValueError(f"Map with id '{mapId}' and point of interest with id '{id}' not found.")
        point_of_interest_to_update.name = name
        point_of_interest_to_update.description = description
        point_of_interest_to_update.latitude = latitude
        point_of_interest_to_update.longitude = longitude
        point_of_interest_to_update.updated_at = datetime.now()
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(f"Error to create a new map with name ({name}).", e)
        session.refresh(point_of_interest_to_update)
        session.close()
        return point_of_interest_to_update
    
    def delete(self, mapId: int, id: int) -> str:
        """Deletes a map and returns the name of the maps deleted"""
        session = Session()
        point_of_interest_to_delete = session.query(PointOfInterest).filter(PointOfInterest.map_id == mapId, PointOfInterest.id == id).first()
        if(point_of_interest_to_delete == None):
            raise ValueError(f"Map with id '{mapId}' and point of interest with id '{id}' not found.")
        name = point_of_interest_to_delete.name
        session.delete(point_of_interest_to_delete)
        session.commit()
        session.close()
        return name