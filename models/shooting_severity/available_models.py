from models.shooting_severity.fogo_cruzado_metadata import FogoCruzadoMetadata


class AvailableModels:
    METADATA_MODEL_CART = FogoCruzadoMetadata(
        name='DecisionTreeWithUnderSampling',
        path='./MachineLearning/model/model_cart.pkl',
        allDataPath='./MachineLearning/data/tiroteios_RJ.csv',
        holdoutDataPath='./MachineLearning/data/test_completo_cart.csv')

    METADATA_MODEL_CART_ORIG = FogoCruzadoMetadata(
        name='DecisionTreeWithUnderOriginalData',
        path='./MachineLearning/model/model_cart_orig.pkl',
        allDataPath='./MachineLearning/data/tiroteios_RJ.csv',
        holdoutDataPath='./MachineLearning/data/test_completo_cart_orig.csv')

    METADATA_MODEL_CART_NORM = FogoCruzadoMetadata(
        name='DecisionTreeWithUnderNormData',
        path='./MachineLearning/model/victims_pred_model_cart.pkl',
        allDataPath='./MachineLearning/data/tiroteios_RJ.csv',
        holdoutDataPath='./MachineLearning/data/test_victims_cart.csv',
        scalerPath='./MachineLearning/scaler/minmax_scaler_victims.pkl')

    METADATA_MODEL_RF = FogoCruzadoMetadata(
        name='RandomForestWithUnderSamplingToSameSize',
        path='./MachineLearning/model/model_RF.pkl',
        allDataPath='./MachineLearning/data/tiroteios_RJ.csv',
        holdoutDataPath='./MachineLearning/data/test_completo_cart.csv')
