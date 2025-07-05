

class FogoCruzadoMetadata:

    name: str
    path: str
    allDataPath: str
    holdoutDataPath: str
    scalerPath: str

    COLUMN_VICTIMS = 'victims'
    COLUMN_DATE = 'date'
    COLUMN_LATITUDE = 'latitude'
    COLUMN_LONGITUDE = 'longitude'
    COLUMN_POLICE_ACTION = 'policeAction'

    COLUMN_WEEKDAY = 'weekday'
    COLUMN_MONTH = 'month'
    COLUMN_PERIOD = 'period'
    COLUMN_SHOOTING_SEVERITY = 'gravidade'

    COLUMNS = [
        COLUMN_POLICE_ACTION,
        COLUMN_VICTIMS,
        COLUMN_DATE,
        COLUMN_LATITUDE,
        COLUMN_LONGITUDE
    ]

    COLUMNS_WITH_PREDICTION = [
        COLUMN_WEEKDAY,
        COLUMN_MONTH,
        COLUMN_PERIOD,
        COLUMN_LATITUDE,
        COLUMN_LONGITUDE,
        COLUMN_SHOOTING_SEVERITY
    ]

    def __init__(
            self,
            name: str,
            path: str,
            allDataPath: str,
            holdoutDataPath: str,
            scalerPath: str = None):
        """
        Classe que representa um modelo de Machine Learning.
        :param name: Nome do modelo.
        :param path: Caminho para o arquivo do modelo.
        :param allDataPath: Caminho para o arquivo de dados completos.
        :param holdoutDataPath: Caminho para o arquivo de dados de holdout.
        :param scalerPath: Caminho para o arquivo do scaler (opcional).
        """
        self.name = name
        self.path = path
        self.allDataPath = allDataPath
        self.holdoutDataPath = holdoutDataPath
        self.scalerPath = scalerPath
