from pydantic import BaseModel

class Record(BaseModel):
    id: str
    name: str
    softwarename: str
    params: str
    price: float
    currency: str
    curency_price: float
    timestamp: int