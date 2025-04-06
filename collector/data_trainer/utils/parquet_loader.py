import os
import pandas as pd
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

PARQUET_PATH = os.environ.get("PARQUET_PATH")

def loadParquet(
    symbol : str,
    kind : str = "stock"
) -> pd.DataFrame :
    path = Path(f"{PARQUET_PATH}/parquetData/{kind}/{symbol}.parquet")
    if not path.exists():
        raise FileNotFoundError(f"{path} doew not exists")
    
    df = pd.read_parquet(path)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns]
    
    for col in df.columns : 
        if "datetime" in col:
            df = df.rename(columns = {col : "datetime"})
        elif "open" in col:
            df = df.rename(columns = {col : "open"})
        elif "high" in col:
            df = df.rename(columns = {col : "high"})
        elif "low" in col:
            df = df.rename(columns = {col : "low"})
        elif "close" in col:
            df = df.rename(columns = {col : "close"})
        elif "volume" in col:
            df = df.rename(columns = {col : "volume"})
    if "datetime" not in df.columns:
        raise ValueError("datetime column missing even after fix")
    return df.sort_values("datetime")