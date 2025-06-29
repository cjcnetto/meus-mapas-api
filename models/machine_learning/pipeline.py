import pickle


class Pipeline:
    """
    Classe para carregar o pipeline de machine learning
    """

    def __init__(self):
        """Inicializa o pipeline"""
        self.pipeline = None

    def load_pipeline(self, path):
        """Carregamos o pipeline construído durante a fase de treinamento
        """

        with open(path, 'rb') as file:
            self.pipeline = pickle.load(file)
        return self.pipeline
