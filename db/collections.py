from .conn import db
from dotenv import load_dotenv
from os import getenv
load_dotenv()

RecordDB = db.get_collection(getenv("RECORD_COLNAME"))

AdminDB = db.get_collection(getenv("ADMIN_COLNAME"))

TokenDB = db.get_collection(getenv("TOKEN_COLNAME"))