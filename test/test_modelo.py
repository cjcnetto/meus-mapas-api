from test.evaluator import Evaluator
from models.shooting_severity.shooting_severity_machine_learning_model import (
    ShootingSeverityMachineLearnModel,
)
from models.shooting_severity.available_models import AvailableModels


# Instanciação das Classes
modelCart = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_CART)
modelCartOrig = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_CART_ORIG)
modelRF = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_RF)
evaluator = Evaluator()

# Carga dos dados
X, y = modelCart.get_X_y()
accuracyToTest = 0.28


def run(model):
    modelo_lr = model.load_model()

    # Obtendo as métricas da Regressão Logística
    accuracy = evaluator.evaluate(modelo_lr, X, y)
    print(f"Acurácia do modelo {model.metadata.name}: {accuracy}")
    assert accuracy >= accuracyToTest, (
        f"Esperava valor >= {accuracyToTest}, mas recebi {accuracy}"
    )


def test_model_cart():
    run(modelCart)


def test_model_cart_orig():
    run(modelCartOrig)


def test_model_rf():
    run(modelRF)
