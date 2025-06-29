import pandas as pd


class Loader:

    COLUMN_VICTIMS = 'victims'
    COLUMN_DATE = 'date'
    COLUMN_LATITUDE = 'latitude'
    COLUMN_LONGITUDE = 'longitude'
    COLUMN_POLICE_ACTION = 'policeAction'

    COLUMN_WEEKDAY = 'weekday'
    COLUMN_MONTH = 'month'
    COLUMN_PERIOD = 'period'
    COLUMN_SHOOTING_SEVERITY = 'shooting_severity'

    COLUMNS = [
        COLUMN_POLICE_ACTION,
        COLUMN_VICTIMS,
        COLUMN_DATE,
        COLUMN_LATITUDE,
        COLUMN_LONGITUDE
    ]

    COLUMNS_WITH_PREDICTION = [
        COLUMN_LATITUDE,
        COLUMN_LONGITUDE,
        COLUMN_WEEKDAY,
        COLUMN_MONTH,
        COLUMN_PERIOD,
        COLUMN_SHOOTING_SEVERITY
    ]

    def load_raw_data(self, url: str) -> pd.DataFrame:
        """
        Carrega e retorna um DataFrame. Há diversos parâmetros
        """
        return pd.read_csv(
            url,
            usecols=Loader.COLUMNS,
            skiprows=0,
            delimiter=',',
            encoding='utf-8-sig')
