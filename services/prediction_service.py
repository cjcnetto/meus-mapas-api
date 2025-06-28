from datetime import datetime
import pickle


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
        period = self.__period(date.hour)

        return self.model.predict(
            [[weekday, month, period, latitude, longitude]])[0]

    def __period(
            self,
            h: int) -> int:
        """
        Recebe um horário em formato de 24 horas (0-23)
        e retorna o período do dia:
        Arguments:
        h -- Hora no formato 0-23
        Returns:
        1 - madrugada (00:00-05:59)
        2 - manhã (06:00-11:59)
        3- tarde (12:00-17:59)
        4 - noite (18:00-23:59)
        """
        if h < 6:
            return 1
        elif h < 12:
            return 2
        elif h < 18:
            return 3
        else:
            return 4
