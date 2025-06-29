import ast
import pandas as pd
from MachineLearning.date_process_result import DateProcessResult
from models.machine_learning.loader import Loader


class FogoCruzadoDataProcessor:
    """
    Classe para processar dados do Fogo Cruzado.
    """

    def __init__(self, date_data_processor, loader: Loader):
        """Inicializa o processador com um carregador de dados."""
        self.date_data_processor = date_data_processor
        self.loader = loader

    def load_data(self, url: str) -> pd.DataFrame:
        """
        Processa o dataset, transformando as colunas de vítimas e data.
        """
        df = self.loader.load_raw_data(url)
        dfFiltered = df[df[Loader.COLUMN_POLICE_ACTION]].copy()
        dfFiltered[Loader.COLUMN_VICTIMS] = (
            dfFiltered[Loader.COLUMN_VICTIMS]
            .apply(self._parse_victims)
        )

        dfFiltered['total_victims'] = dfFiltered[Loader.COLUMN_VICTIMS].apply(
            lambda v: len(v) if isinstance(v, list) else 0)
        dfFiltered['deaths'] = dfFiltered[Loader.COLUMN_VICTIMS].apply(
            self._count_deaths)

        dfFiltered[Loader.COLUMN_SHOOTING_SEVERITY] = dfFiltered.apply(
            lambda row: self._classify(row['total_victims'], row['deaths']
                                       ), axis=1)

        dfFiltered[Loader.COLUMN_DATE] = pd.to_datetime(
            dfFiltered[Loader.COLUMN_DATE])
        dfFiltered[Loader.COLUMN_WEEKDAY] = dfFiltered[
            Loader.COLUMN_DATE
        ].apply(lambda date: date.weekday())
        dfFiltered[Loader.COLUMN_MONTH] = dfFiltered[
            Loader.COLUMN_DATE].dt.month
        dfFiltered[Loader.COLUMN_PERIOD] = (
            dfFiltered[Loader.COLUMN_DATE]
            .dt.hour
            .apply(DateProcessResult.process_period_of_day)
        )
        dfFiltered.drop(
             [Loader.COLUMN_POLICE_ACTION, Loader.COLUMN_DATE,
              Loader.COLUMN_VICTIMS, 'total_victims',
              'deaths'], axis=1, inplace=True)
        new_order = [
            Loader.COLUMN_WEEKDAY, Loader.COLUMN_MONTH, Loader.COLUMN_PERIOD,
            Loader.COLUMN_LATITUDE, Loader.COLUMN_LONGITUDE,
            Loader.COLUMN_SHOOTING_SEVERITY]
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
