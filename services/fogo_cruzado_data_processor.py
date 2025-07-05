import ast
import pandas as pd
from models.machine_learning.machine_learning_util import MachineLearningUtil
from models.machine_learning.model_metadata import ModelMetadata


class FogoCruzadoDataProcessor:
    """
    Classe para processar dados do Fogo Cruzado.
    O objetivo dessa classe é regatar os dados de tiroteios do Rio de janeiro
    a partir da api do fogo cruzado e processar esses dados para serem
    utilizados em modelos de machine learning.
    """

    def __init__(self, date_data_processor, loader: ModelMetadata):
        """Inicializa o processador com um carregador de dados."""
        self.date_data_processor = date_data_processor
        self.loader = loader

    def load_data(self, url: str) -> pd.DataFrame:
        """
        Processa o dataset, transformando as colunas de vítimas e data.
        """
        df = self.loader.load_raw_data(url)
        dfFiltered = df[df[ModelMetadata.COLUMN_POLICE_ACTION]].copy()
        dfFiltered[ModelMetadata.COLUMN_VICTIMS] = (
            dfFiltered[ModelMetadata.COLUMN_VICTIMS]
            .apply(self._parse_victims)
        )

        dfFiltered['total_victims'] = dfFiltered[
            ModelMetadata.COLUMN_VICTIMS].apply(
            lambda v: len(v) if isinstance(v, list) else 0)
        dfFiltered['deaths'] = dfFiltered[ModelMetadata.COLUMN_VICTIMS].apply(
            self._count_deaths)

        dfFiltered[ModelMetadata.COLUMN_SHOOTING_SEVERITY] = dfFiltered.apply(
            lambda row: self._classify(row['total_victims'], row['deaths']
                                       ), axis=1)

        dfFiltered[ModelMetadata.COLUMN_DATE] = pd.to_datetime(
            dfFiltered[ModelMetadata.COLUMN_DATE])
        dfFiltered[ModelMetadata.COLUMN_WEEKDAY] = dfFiltered[
            ModelMetadata.COLUMN_DATE
        ].apply(lambda date: date.weekday())
        dfFiltered[ModelMetadata.COLUMN_MONTH] = dfFiltered[
            ModelMetadata.COLUMN_DATE].dt.month
        dfFiltered[ModelMetadata.COLUMN_PERIOD] = (
            dfFiltered[ModelMetadata.COLUMN_DATE]
            .dt.hour
            .apply(MachineLearningUtil.process_period_of_day)
        )
        dfFiltered.drop(
             [ModelMetadata.COLUMN_POLICE_ACTION, ModelMetadata.COLUMN_DATE,
              ModelMetadata.COLUMN_VICTIMS, 'total_victims',
              'deaths'], axis=1, inplace=True)
        new_order = [
            ModelMetadata.COLUMN_WEEKDAY,
            ModelMetadata.COLUMN_MONTH,
            ModelMetadata.COLUMN_PERIOD,
            ModelMetadata.COLUMN_LATITUDE,
            ModelMetadata.COLUMN_LONGITUDE,
            ModelMetadata.COLUMN_SHOOTING_SEVERITY]
        dfFiltered = dfFiltered[new_order]
        return dfFiltered

    def _parse_victims(self, v) -> list:
        """
        Converte uma string ou dicionário de vítimas em uma lista de vítimas.
        """
        if isinstance(v, str) and v.strip().startswith('['):
            try:
                return ast.literal_eval(v)
            except (ValueError, SyntaxError):
                return []
        return v if isinstance(v, list) else []

    def _count_deaths(self, vitimas) -> int:
        """ Conta o número de vítimas mortas em uma lista de vítimas."""
        return self._count_by_status(vitimas, 'Dead')

    def _count_by_status(self, vitimas, status: str) -> int:
        """
        Conta o número de vítimas com um determinado
        status em uma lista de vítimas.
        """
        if not isinstance(vitimas, list):
            return 0
        return sum(1 for vit in vitimas if vit.get('situation') == status)

    def _classify(self, victims: int, deaths: int) -> str:
        """
        Classifica a gravidade de um evento com base no
        número de vítimas e mortos.
        """
        if victims == 0:
            return 'Sem vítimas'
        elif deaths == 0:
            return 'Sem mortos'
        else:
            return 'Com mortos'
