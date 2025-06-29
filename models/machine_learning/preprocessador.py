from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np

from MachineLearning.date_process_result import DateProcessResult


class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(
            dataset,
            percentual_teste,
            seed
        )
        # normalização/padronização
        return (X_train, X_test, Y_train, Y_test)

    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(
            X, Y, test_size=percentual_teste, random_state=seed)

    def preparar_form(self,
                      latitude: float,
                      longitude: float,
                      date: datetime):
        """
        Prepara os dados recebidos do front para serem usados no modelo.
        """
        weekday = date.weekday()
        month = date.month
        period = DateProcessResult.process_period_of_day(date.hour)

        X_input = np.array([weekday, month, period, latitude, longitude])
        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)
        return X_input
