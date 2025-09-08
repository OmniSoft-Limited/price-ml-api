from schema.adminschema import AdminSchema
from db.collections import AdminDB
import time
from bson import ObjectId
from pymongo.errors import PyMongoError

from utils.encryption import hash_password, verify_password


async def create_user(name: str, email: str, password: str) -> dict:
    """Create a new admin user."""
    user = {
        "name": name,
        "email": email,
        "password": password,
        "created_at": int(time.time())
    }
    try:
        inserted_user = await AdminDB.insert_one(user)
        return {
            "status": "success",
            "message": "User created successfully",
            "id": str(inserted_user.inserted_id),  # ObjectId -> str
        }
    except PyMongoError as e:
        return {"status": "error", "message": f"Database Error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected Error: {e}"}


async def get_user_by_id(id: str) -> dict:
    """Get a user by MongoDB ObjectId."""
    try:
        user = await AdminDB.find_one({"_id": ObjectId(id)})
        if not user:
            return {"status": "error", "message": "User not found"}

        return {
            "status": "success",
            "message": "User found successfully",
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}


async def get_user_by_email(email: str) -> dict:
    """Get a user by email."""
    try:
        user = await AdminDB.find_one({"email": email})
        if not user:
            return {"status": "error", "message": "User not found"}

        return {
            "status": "success",
            "message": "User found successfully",
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}


async def get_user_by_name(name: str) -> dict:
    """Get a user by name."""
    try:
        user = await AdminDB.find_one({"name": name})
        if not user:
            return {"status": "error", "message": "User not found"}

        return {
            "status": "success",
            "message": "User found successfully",
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}


async def update_user(id: str, name: str = None, email: str = None, password: str = None) -> dict:
    """Update user details by ID."""
    try:
        updates = {}
        if name:
            updates["name"] = name
        if email:
            updates["email"] = email
        if password:
            updates["password"] = hash_password(password)

        if not updates:
            return {"status": "error", "message": "No fields to update"}

        result = await AdminDB.update_one(
            {"_id": ObjectId(id)},
            {"$set": updates}
        )

        if result.matched_count == 0:
            return {"status": "error", "message": "User not found"}

        return {"status": "success", "message": "User updated successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}


async def delete_user(id: str) -> dict:
    """Delete a user by ID."""
    try:
        result = await AdminDB.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return {"status": "error", "message": "User not found"}

        return {"status": "success", "message": "User deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}

async def authenticate(username: str, password: str) -> bool:
    """
    Authenticate a user.
    """
    try:
        user = await AdminDB.find_one({"name": username})
        if not user:
            return False
        if not verify_password(password, user["password"]):
            return False
        return True
    except Exception:
        return False