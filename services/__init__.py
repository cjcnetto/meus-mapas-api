from repositories import *
from services.map_service import MapService
from logger import logger

map_service = MapService(MapRepository(), PointOfInterestRepository(), logger)