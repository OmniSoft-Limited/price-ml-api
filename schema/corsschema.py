from pydantic import BaseModel

class CORSSchema(BaseModel):
    id: str
    name: str
    email: str
    token: str
    origin: list[str]
    created_at: int