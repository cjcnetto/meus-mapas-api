from schemas.base import BaseSchema

class DelSchema(BaseSchema):
    """ Defines the schema for the delete endpoint"""
    mesage: str = "Deleted successuful"
    name: str =  "The name of the entity that was deleted"