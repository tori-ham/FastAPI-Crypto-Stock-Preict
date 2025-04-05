import os
import requests
from datetime import datetime
from utils.sqlite_writer import createTableIfNotExists, insertPrice

from dotenv import load_dotenv

load_dotenv()

BINANCE_API_URL = os.environ.get("BINANCE_API_URL")

def collectCrypto(
    symbol : str = "BTCUSDT",
    interval = "1m",
    limit = 30
) : 
    symbol = symbol.upper()
    print(f"[{datetime.now()}] Collecting {symbol}...")
    params = {
        "symbol" : symbol,
        "interval" : interval,
        "limit" : limit
    }
    
    try:
        resp = requests.get(
            BINANCE_API_URL,
            params = params
        )
        data = resp.json()
        if not isinstance(data, list):
            print("Invalid Response", data)
            return 

        prices = []
        for row in data:
            timestamp = int(row[0]) // 1000
            dt = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            prices.append(
                (
                    dt,
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5])
                )
            )
        createTableIfNotExists(f"crypto_{symbol}")
        insertPrice(f"crypto_{symbol}", prices)
        print(f"Successfully Collected {len(prices)} rows for {symbol}")
    except Exception as e:
        print("Error Collecting Crypto Data : ", e)