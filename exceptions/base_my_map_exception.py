class BaseMyMapException(Exception):
    """Exception criada para o controle de exceções da app"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message