from exceptions.base_my_map_exception import BaseMyMapException


class NotFoundException(BaseMyMapException):
    """Exceção personalizada para recursos não encontrados."""
    def __init__(self, message="Recurso não encontrado"):
        super().__init__(message)