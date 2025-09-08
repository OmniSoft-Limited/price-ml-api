from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi.util import get_remote_address
from middleware.ratelimiter import limiter
from os import getenv
from utils.encryption import hash_password, verify_password
from auth.users import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_user_by_name,
    update_user,
    delete_user,
)
from schema.adminschema import AdminSchema
from utils.validation import validate_email

username_env = getenv("ID")
password_env = getenv("PASSWORD")  # <-- should already be hashed & stored in .env
security = HTTPBasic()

def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Dependency to verify admin credentials.
    Raises 401 if invalid.
    """
    if credentials.username.strip() != username_env.strip() or verify_password(credentials.password.strip(), password_env):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

router = APIRouter(
    prefix="/admins",
    dependencies=[Depends(admin_auth)]
)

@router.post("/create", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def create_admin(
    req: AdminSchema = Body(...),
    request: Request = None
):
    """
    Create a new admin user.
    """

    if not validate_email(req.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")

    # If valid, create the admin user
    return await create_user(
        name=req.name,
        email=req.email,
        password=hash_password(req.password),
    )


@router.get("/get/{id}", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def get_admin_by_id_route(id: str, req: AdminSchema, request: Request):
    """
    Get an admin user by ID.
    """
    if not validate_email(req.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")

    return await get_user_by_id(id)


@router.get("/email/{email}", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def get_admin_by_email_route(email: str, request: Request):
    """
    Get an admin user by email.
    """
    return await get_user_by_email(email)


@router.get("/name/{name}", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def get_admin_by_name_route(name: str, request: Request):
    """
    Get an admin user by name.
    """
    return await get_user_by_name(name)


@router.put("/update/{id}", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def update_admin(id: str, req: AdminSchema, request: Request):
    """
    Update an admin user by ID.
    """

    if not validate_email(req.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
    
    return await update_user(
        id=id,
        name=req.name,
        email=req.email,
        password=req.password,
    )


@router.delete("/delete/{id}", tags=["admins"])
@limiter.limit(getenv("RATE_LIMIT", "10/minute"))
async def delete_admin(id: str, request: Request):
    """
    Delete an admin user by ID.
    """
    return await delete_user(id)
