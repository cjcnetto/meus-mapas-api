from typing import Optional
import pandas as pd
import pickle

from sklearn.base import BaseEstimator
from models.shooting_severity.fogo_cruzado_metadata import FogoCruzadoMetadata


class ShootingSeverityMachineLearnModel:
    def __init__(self, metadata: FogoCruzadoMetadata):
        self.metadata: FogoCruzadoMetadata = metadata
        self.allData: Optional[pd.DataFrame] = None
        self.holdoutData: Optional[pd.DataFrame] = None
        self.model: Optional[BaseEstimator] = None

    def load_model(self) -> BaseEstimator:
        """
        Carrega um modelo de previsão a partir de um arquivo.
        """
        if self.model is None:
            if self.metadata.path.endswith('.pkl'):
                with open(self.metadata.path, 'rb') as file:
                    self.model = pickle.load(file)
            else:
                raise ValueError(
                    'Formato de arquivo não suportado: apenas .pkl é aceito.')
        return self.model

    def load_all_data(self) -> pd.DataFrame:
        """
        Carrega e retorna um DataFrame. Há diversos parâmetros
        """
        if self.allData is None:
            self.allData = pd.read_csv(
                self.metadata.allDataPath,
                usecols=FogoCruzadoMetadata.COLUMNS,
                skiprows=0,
                delimiter=',',
                encoding='utf-8-sig')
        return self.allData

    def load_holdout_data(self) -> pd.DataFrame:
        """
        Carrega um dataframe com os dados de teste
        para a previsão.
        """
        if self.holdoutData is None:
            self.holdoutData = pd.read_csv(
                self.metadata.holdoutDataPath,
                usecols=FogoCruzadoMetadata.COLUMNS_WITH_PREDICTION,
                skiprows=0,
                delimiter=',',
                encoding='utf-8-sig')
        return self.holdoutData

    def get_X_y(self) -> tuple:
        """
        Retorna as variáveis independentes (X) e dependentes (y)
        do conjunto de dados de holdout.
        """
        dataset = self.load_holdout_data()
        array = dataset.values
        X = array[:, 0:5]
        y = array[:, 5]
        return X, y

    def hasScaler(self) -> bool:
        """
        Verifica se o modelo possui um scaler associado.
        """
        return self.metadata.scalerPath is not None

    def load_scaler(self):
        """
        Carrega o scaler associado ao modelo, se existir.
        """
        if self.hasScaler():
            with open(self.metadata.scalerPath, 'rb') as file:
                return pickle.load(file)
        else:
            raise ValueError("Scaler não está disponível para este modelo.")
