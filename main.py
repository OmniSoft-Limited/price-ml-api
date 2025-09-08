from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 
from slowapi.errors import RateLimitExceeded
from middleware.ratelimiter import limiter, rate_limit_handler
import logging
from routers import predictor, admins, tokens
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(predictor.router)
app.include_router(admins.router)
app.include_router(tokens.router)

@app.get("/")
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def home(request: Request):
    return JSONResponse(content={"message": "Hello from Software Price Predictor API!"})

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = int(getenv("PORT", "8080"))
    host = getenv("HOST", "localhost")
    logging.info(f"Running on http://{host}:{port}")
    
    uvicorn.run(app, port=port, host=host)