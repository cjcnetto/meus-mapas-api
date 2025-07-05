from test.evaluator import Evaluator
from models.shooting_severity.shooting_severity_machine_learning_model import (
    ShootingSeverityMachineLearnModel,
)
from models.shooting_severity.available_models import AvailableModels


modelCartNorm = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_CART_NORM)
modelCartOrig = ShootingSeverityMachineLearnModel(
    AvailableModels.METADATA_MODEL_CART_ORIG)

evaluator = Evaluator()

# Carga dos dados
X, y = modelCartOrig.get_X_y()
accuracyToTest = 0.3


def run(model, accuracyToTestInTheRun=accuracyToTest):
    modelo_lr = model.load_model()

    # Obtendo as métricas da Regressão Logística
    accuracy = evaluator.evaluate(modelo_lr, X, y)
    print(f"Acurácia do modelo {model.metadata.name}: {accuracy}")
    assert accuracy >= accuracyToTestInTheRun, (
        f"Esperava valor >= {accuracyToTestInTheRun}, mas recebi {accuracy}"
    )


def predict(X_entrada, shootingModel):
    model = model = shootingModel.load_model()
    scaler = shootingModel.load_scaler()
    rescaledEntradaX = scaler.transform(X_entrada)
    return model.predict(rescaledEntradaX)[0]


def test_model_prediction_mortos_cart_norm():
    X_entrada = [[
                2,
                3,
                1,
                -22.960106,
                -43.169318
            ]]
    prediction = predict(X_entrada, modelCartNorm)
    assert prediction == 'mortos', (
        f"Esperava 'mortos', mas recebi {prediction}"
    )


def test_model_prediction_sem_vitima_cart_norm():
    X_entrada = [[
                1,
                7,
                2,
                -22.964289,
                -43.183631
            ]]
    prediction = predict(X_entrada, modelCartNorm)
    assert prediction == 'sem_vitima', (
        f"Esperava 'sem_vitima', mas recebi {prediction}"
    )


def test_model_prediction_ferido_cart_norm():
    X_entrada = [[
                2,
                8,
                1,
                -22.9642353058,
                -43.1898117065
            ]]
    prediction = predict(X_entrada, modelCartNorm)
    assert prediction == 'ferido', (
        f"Esperava 'ferido', mas recebi {prediction}"
    )


def test_model_cart_norm():
    run(modelCartNorm)


def test_model_cart_orig():
    run(modelCartOrig)
