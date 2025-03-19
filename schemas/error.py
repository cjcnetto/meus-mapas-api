from schemas.base import BaseSchema

class ErrorSchema(BaseSchema):
    """Defines the schema for the error response"""
    message: str = "An error occurred"
