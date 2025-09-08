import logging
import time
from db.collections import RecordDB
from schema.network import PredictResponse
from schema.currency import CURRENCIES
from schema.record import Record
from utils.converter import convert
from utils.model import load_model, run
from dotenv import load_dotenv
load_dotenv()
from os import getenv


model = load_model("./model/model.onnx")

async def price(name: str, soft: str, data: list[float], currency: str) -> tuple[float, str, float]: 
    """
    Returns:
        prediction (float), currency (str), currency_price (float)
    """
    currency = currency.upper()
    params = str(data)

    if currency not in CURRENCIES:
        raise ValueError("Invalid currency")
    
    try:
        record = await RecordDB.find_one({"params": params})
        if record:
            expirytime = record["expirytime"]
            prediction = record["price"]
            record_currency = record.get("currency", currency)

            if expirytime > time.time():
                logging.info("Cache hit")
                # If cached currency differs, convert
                if record_currency != currency:
                    currency_price = convert(prediction, currency)
                else:
                    currency_price = record["curency_price"]
                return prediction, currency, currency_price
            else:
                try:
                    await RecordDB.delete_one({"params": params})
                    logging.info("Cache expired -> Cache miss")
                except Exception as e:
                    logging.error(f"Error: {e}")
                    return None, None, None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None, None, None

    # Cache miss, run prediction
    logging.info("Cache miss")
    prediction = run(model, data)  # blocking; consider async wrapper if needed
    try:
        currency_price = convert(float(prediction), currency)
        new_record: Record = {
            "name": name,
            "softwarename": soft,
            "params": str(data),
            "price": float(prediction),
            "timestamp": int(time.time()),
            "currency": currency,
            "curency_price": currency_price,
            "expirytime": int(time.time()) + int(getenv("CACHE_EXPIRY_TIME", "3600")) * 60 * 3 # 3 Hours, Has to be in changed later
        }
        await RecordDB.insert_one(new_record)
        logging.info("Cache miss")
    except Exception as e:
        logging.error(f"Error: {e}")
        return None, None, None

    return float(prediction), currency, float(currency_price)


