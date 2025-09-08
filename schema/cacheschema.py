from pydantic import BaseModel

class CacheSchema(BaseModel):
    id: str
    title: str
    params: str
    price: float
    timestamp: int
    expirytime: int