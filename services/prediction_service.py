from datetime import datetime
import pickle

from MachineLearning.date_process_result import DateProcessResult


class ShootingSeverityPredictionService:

    def __init__(self):
        """Inicializa o modelo"""
        self.model = None

    def load_model(self, path):
        """
        Carrega um modelo de previsão a partir de um arquivo.
        """
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            raise Exception('Formato de arquivo não suportado')
        return self.model

    def predict(self,
                latitude: float,
                longitude: float,
                date: datetime) -> str:
        """
        Faz uma previsão da severidade de tiroteio com base nos dados
        fornecidos.
        """
        if self.model is None:
            raise Exception(
                'Modelo não foi carregado. Use carrega_modelo() primeiro.')
        weekday = date.weekday()
        month = date.month
        period = DateProcessResult.process_period_of_day(date.hour)

        return self.model.predict(
            [[weekday, month, period, latitude, longitude]])[0]
