from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from middleware.ratelimiter import limiter
from schema.network import PredictRequest
from db.cache import price
from fastapi.responses import JSONResponse
from fastapi import Request, status
from auth.tokens import verify_token
from dotenv import load_dotenv
from os import getenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.tokens import verify_token
load_dotenv()

security = HTTPBearer()

async def auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to verify token credentials.
    Raises 401 if invalid.
    """
    token = credentials.credentials  # <-- this is the actual token string
    if not await verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


router = APIRouter(
    prefix="/ai",
    dependencies=[Depends(auth)]
)

@router.post("/predict", tags=["predict"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def predict_price(request: Request, req: PredictRequest):
    prediction, currency, currency_price = await price(req.name, req.softwarename, req.data, req.currency)
    if prediction is None or currency is None or currency_price is None:
        return JSONResponse(content={"message": "Something went wrong"}, status_code=500)
    return JSONResponse(content={
        "prediction": float(prediction), 
        "currency": currency, 
        "curency_price": currency_price
        })
