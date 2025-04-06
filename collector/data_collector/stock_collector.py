import yfinance as yf
from datetime import datetime 

import pandas as pd

from utils.sqlite_writer import createTableIfNotExists, insertPrice
from utils.parquet_writer import saveDataToParquet

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

def collectStockToParquet(symbol : str):
    symbol = symbol.upper()
    
    print(f"[{datetime.now()}] Collecting {symbol}...")
    df = yf.download(
        symbol, 
        period = "1d",
        interval = "1m",
        progress = False
    )
    
    if df.empty:
        print(f"No data for {symbol}")
        return 
    
    df = df.reset_index()
    df = df.rename(
        columns = {
            "Datetime" : "datetime",
            "Open" : "open",
            "High" : "high",
            "Low" : "low",
            "Close" : "close",
            "Volume" : "volume"
        }
    )
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    saveDataToParquet(symbol, df, kind = "stock")