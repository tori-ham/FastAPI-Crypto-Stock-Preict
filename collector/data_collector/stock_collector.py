import yfinance as yf
from datetime import datetime 
from utils.sqlite_writer import createTableIfNotExists, insertPrice

def collectStock( symbol : str ):
    symbol = symbol.upper()
    print(f"[{datetime.now()}] Collecting {symbol}...")
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")
    
    if df.empty:
        print("No Data Received")
        return 
    
    prices = []
    for idx, row in df.iterrows():
        prices.append(
            (
                idx.strftime("%Y-%m-%d %H:%M:%S"),
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"]
            )
        )
    
    createTableIfNotExists(symbol)
    insertPrice(symbol, prices)
    print(f"Successfully Collected {len(prices)} rows for {symbol}")