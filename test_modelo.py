from models.machine_learning.loader import Loader
from models.machine_learning.evaluator import Evaluator
from models.machine_learning.pipeline import Pipeline
from MachineLearning.fogo_cruzado_data_processor import (
    FogoCruzadoDataProcessor,
)
from MachineLearning.date_process_result import DateProcessResult
# To run: pytest -v test_modelos.py

# Instanciação das Classes

date_data_processor = DateProcessResult()
loader = Loader()
processor = FogoCruzadoDataProcessor(
    date_data_processor,
    loader)

evaluator = Evaluator()
pipeline = Pipeline()

# Parâmetros
url_dados = "./MachineLearning/data/tiroteios_RJ.csv"

# Carga dos dados
dataset = processor.load_data(url_dados)
array = dataset.values
X = array[:, 0:5]
y = array[:, 5]


def test_model():
    lr_path = './MachineLearning/model/model.pkl'
    modelo_lr = pipeline.load_pipeline(lr_path)

    # Obtendo as métricas da Regressão Logística
    accuracy = evaluator.evaluate(modelo_lr, X, y)
    assert accuracy >= 0.45, f"Esperava valor >= 40%, mas recebi {accuracy}"
