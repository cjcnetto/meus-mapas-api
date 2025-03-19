from pydantic import BaseModel

class BaseSchema(BaseModel):
    def to_json(self):
        return self.dict()