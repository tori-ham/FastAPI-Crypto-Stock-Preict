import os
from typing import List, Tuple
from datetime import datetime

import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ.get("STOCK_DB_PATH", "stock_data.db")

def getDB():
    conn = sqlite3.connect(DB_PATH)
    return (conn, conn.cursor())
    

def createTableIfNotExists(symbol : str):
    (conn, cur) = getDB()
    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS stock_{symbol} (
                datetime TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """
    )
    conn.commit()
    conn.close()

def insertPrice(
    symbol : str,
    prices : List[Tuple[str, float, float, float, float, float]]
):
    (conn, cur) = getDB()
    for row in prices:
        cur.execute(
            f"""
                INSERT OR IGNORE INTO stock_{symbol} ( datetime, open, high, low, close, volume ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            row
        )
    conn.commit()
    conn.close()