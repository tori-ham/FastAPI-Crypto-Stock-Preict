import os
from dotenv import load_dotenv
import requests
from typing import List

load_dotenv()

# API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
# API_URL = os.getenv("ALPHA_VANTAGE_API_URL", "")
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
API_URL = os.environ.get("ALPHA_VANTAGE_API_URL")

def getPricesForInterval(
    symbol : str,
    interval : str = "1min",
    outputSize = "compact"
) -> List[float] :
    params = {
        "function" : "TIME_SERIES_INTRADAY",
        "symbol" : symbol,
        "interval" : interval,
        "outputsize" : outputSize,
        "apikey" : API_KEY
    }
    
    resp = requests.get(
        API_URL,
        params = params
    )
    data = resp.json()
    
    time_series_key = f"Time Series ({interval})"
    if time_series_key not in data:
        raise Exception(f"API Response Error : {data}")
    
    sorted_items = sorted(data[time_series_key].items())
    prices = [ float(entry["4. close"]) for _, entry in sorted_items ]

    # 최근 30분
    return prices[ -30 : ]

