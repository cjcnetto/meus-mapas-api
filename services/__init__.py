from repositories import MapRepository, PointOfInterestRepository
from services.map_service import MapService
from services.prediction_service import ShootingSeverityPredictionService
from models.shooting_severity.shooting_severity_machine_learning_model import (
    ShootingSeverityMachineLearnModel,
)
from models.shooting_severity.available_models import AvailableModels
from logger import logger

# Inicializa o serviço de previsão e o serviço de mapa
# define aqui o modelo
model = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_CART_ORIG)
prediction = ShootingSeverityPredictionService(model)

map_service = MapService(
    prediction, MapRepository(), PointOfInterestRepository(), logger)
