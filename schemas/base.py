from pydantic import BaseModel


class BaseSchema(BaseModel):
    def to_json(self):
        """Converte o objeto para JSON"""
        return self.dict()
