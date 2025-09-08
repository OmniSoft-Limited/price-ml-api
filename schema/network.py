from pydantic import BaseModel

class PredictRequest(BaseModel):
    name: str
    softwarename: str
    data: list[float]
    currency: str

class PredictResponse(BaseModel):
    prediction: float
    currency: str
    curency_price: float