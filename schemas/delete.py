from schemas.base import BaseSchema

class DelSchema(BaseSchema):
    """ 
        Define o esquema de resposta para a deleção de um objeto
        message - Mensagem de sucesso ou erro
        name - Nome do objeto removido
    """
    message: str = "Removido com sucesso"
    name: str =  "Nome do objeto removido"