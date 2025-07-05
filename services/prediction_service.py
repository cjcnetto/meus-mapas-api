from datetime import datetime
from models.date.date_cycle import DateCycle
from models.shooting_severity.shooting_severity_machine_learning_model import (
    ShootingSeverityMachineLearnModel
)


class ShootingSeverityPredictionService:

    def __init__(self, machineLearningModel: ShootingSeverityMachineLearnModel):
        """Inicializa o modelo"""
        self.machineLearningModel = machineLearningModel

    def predict(self,
                latitude: float,
                longitude: float,
                date: datetime) -> str:
        """
        Faz uma previsão da severidade de tiroteio com base nos dados
        fornecidos.
        """
        model = self.machineLearningModel.load_model()
        dateCycle = DateCycle(date)

        return model.predict(
            [[
                dateCycle.dayofWeek,
                dateCycle.month,
                dateCycle.periodOfTheDay,
                latitude,
                longitude
            ]])[0]
