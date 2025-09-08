from pydantic import BaseModel

class TokenSchema(BaseModel):
    name: str
    email: str
    is_premium: bool