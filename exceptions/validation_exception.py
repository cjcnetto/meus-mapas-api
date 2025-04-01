from exceptions.base_my_map_exception import BaseMyMapException

class ValidationException(BaseMyMapException):
    """Exceção personalizada para erros de validação."""
    def __init__(self, message="Erro de validação"):
        super().__init__(message)