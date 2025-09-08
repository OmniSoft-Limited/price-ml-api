from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

client = AsyncIOMotorClient(getenv("MONGODB_URI"))
db = client.get_database(getenv("DB_NAME"))

