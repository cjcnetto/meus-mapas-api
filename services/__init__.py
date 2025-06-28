from repositories import MapRepository, PointOfInterestRepository
from services.map_service import MapService
from services.prediction_service import ShootingSeverityPredictionService
from logger import logger

model_path = "./MachineLearning/model.pkl"

prediction = ShootingSeverityPredictionService()
prediction.load_model(model_path)
map_service = MapService(
    prediction, MapRepository(), PointOfInterestRepository(), logger)
