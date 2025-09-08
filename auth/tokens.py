import time
from bson import ObjectId
from db.collections import TokenDB
from dotenv import load_dotenv
from utils.encryption import generateToken
from os import getenv
load_dotenv()


async def create_token(name: str, email: str, is_premium: bool) -> dict:
    """
    Create a new token for a user.
    - Token = name + email + password
    - Always stores created_at
    - If not premium, adds expire_at (3 days from now)
    """
    token_str = generateToken(name, email)
    now = int(time.time())

    token_data = {
        "name": name,
        "email": email,
        "token": token_str,
        "is_premium": is_premium,
        "created_at": now,
    }

    if not is_premium:
        token_data["expire_at"] = now + int(getenv("TOKEN_EXPIRY")) * 24 * 60 * 60

    try:
        inserted = await TokenDB.insert_one(token_data)
        return {
            "status": "success",
            "message": "Token created successfully",
            "id": str(inserted.inserted_id),
            "token": token_str,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating token: {e}"
        }


async def get_token(token: str) -> dict:
    """
    Retrieve a token document by token string.
    """
    try:
        record = await TokenDB.find_one({"token": token})
        if not record:
            return {
                "status": "error",
                "message": "Token not found"
            }
        record["_id"] = str(record["_id"])
        return {
            "status": "success",
            "data": record
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching token: {e}"
        }


async def verify_token(token: str) -> bool:
    """
    Verify if token exists and is still valid.
    - Premium tokens never expire
    - Non-premium tokens expire after 3 days
    """
    record = await TokenDB.find_one({"token": token})
    if not record:
        return False

    if record.get("is_premium", False):
        return True

    expire_at = record.get("expire_at")
    if expire_at and expire_at > int(time.time()):
        return True

    # Token expired → delete it
    await TokenDB.delete_one({"token": token})
    return False


async def delete_token(token: str) -> dict:
    """
    Delete a token document by token string.
    """
    try:
        result = await TokenDB.delete_one({"token": token})
        if result.deleted_count == 0:
            return {
                "status": "error",
                "message": "Token not found"
            }
        return {
            "status": "success",
            "message": "Token deleted successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting token: {e}"
        }


