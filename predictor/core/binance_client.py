import os
from functools import lru_cache

import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.environ.get("BINANCE_SECRET_KEY")
BINANCE_API_URL = os.environ.get("BINANCE_API_URL")

def getBinancePrices(
    symbol : str,
    interval = "1m",
    limit = 30
) -> List[float] : 
    params = {
        "symbol" : symbol,
        "interval" : interval,
        "limit" : limit
    }
    resp = requests.get(
        BINANCE_API_URL,
        params = params
    )
    data = resp.json()
    
    if not isinstance(data, list):
        raise Exception(f"Invalid response from Binance: {data}")
    return [ float(candle[4]) for candle in data ]

@lru_cache(maxsize = 1)
def getBinanceSymbolPairs(asset) -> list[str] :
    url = os.environ.get("BINANCE_SYMBOL_API_URL")
    resp = requests.get(url)
    data = resp.json()
    
    symbols = [
        s["symbol"] for s in data["symbols"] if s["status"] == "TRADING" and s["quoteAsset"] == asset
    ]
    return symbols