from sklearn.metrics import accuracy_score


class Evaluator:

    """
    Classe para avaliar modelos de Machine Learning.
    """

    def evaluate(self, model, X_test, Y_test):
        """
        Faz uma predição e avalia o modelo. Poderia parametrizar o tipo de
        avaliação, entre outros.
        """
        predicoes = model.predict(X_test)
        # Caso o seu problema tenha mais do que duas classes,
        # altere o parâmetro average
        return accuracy_score(Y_test, predicoes)
