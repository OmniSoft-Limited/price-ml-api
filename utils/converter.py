import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

main_api_url = getenv("CURRENCY_API_URL")
api_key = getenv("CURRENCY_API_KEY")

URL = f"{main_api_url}/v6/{api_key}/latest/USD"

def convert(amount: float, currency: str) -> float:
    rate = float(requests.get(URL).json()["conversion_rates"][currency])
    return rate * amount