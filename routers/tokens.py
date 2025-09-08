from fastapi import APIRouter, Depends, Request, HTTPException, security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth.users import authenticate
from middleware.ratelimiter import limiter
from os import getenv

from schema.tokenschema import TokenSchema
from auth.tokens import create_token, get_token, verify_token, delete_token

security = HTTPBasic()

async def token_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Dependency to verify token credentials.
    Raises 401 if invalid.
    """
    if not await authenticate(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


router = APIRouter(
    prefix="/tokens",
    dependencies=[Depends(token_auth)]
)

@router.post("/create", tags=["tokens"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def create_token_route(req: TokenSchema, request: Request):
    """
    Create a new token for a user.
    """
    token = await create_token(
        name=req.name,
        email=req.email,
        is_premium=req.is_premium,
    )
    return {"token": token}


@router.get("/get/{token}", tags=["tokens"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def get_token_route(token: str, request: Request):
    """
    Retrieve token details.
    """
    data = get_token(token)
    if not data:
        raise HTTPException(status_code=404, detail="Token not found")
    return data


@router.get("/verify/{token}", tags=["tokens"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def verify_token_route(token: str, request: Request):
    """
    Verify if a token is valid.
    """
    is_valid = await verify_token(token)
    return {"token": token, "valid": is_valid}


@router.delete("/delete/{token}", tags=["tokens"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def delete_token_route(token: str, request: Request):
    """
    Delete a token.
    """
    deleted = await delete_token(token)
    if not deleted:
        raise HTTPException(status_code=404, detail="Token not found or already deleted")
    return deleted
