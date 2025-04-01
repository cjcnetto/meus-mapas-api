from schemas.base import BaseSchema

class ErrorSchema(BaseSchema):
    """
        Define o esquema de erro para a API
        message - Mensagem de erro
    """
    message: str = "Um erro não esperado"
