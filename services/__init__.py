from repositories import *
from services.map_service import MapService
from services.point_of_interest_service import PointOfInterestService
from logger import logger

mapService = MapService(MapRepository(), logger)
pointOfInterestService = PointOfInterestService(MapRepository(), PointOfInterestRepository(), logger)