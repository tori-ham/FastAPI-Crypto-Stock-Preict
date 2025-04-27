import os
import pandas as pd
from datetime import datetime, UTC
from pathlib import Path
from fredapi import Fred
import requests

from dotenv import load_dotenv
load_dotenv()

DATA_DIRECTORY = os.environ.get("DATA_DIRECTORY")
ECOS_API_KEY = os.environ.get("ECOS_API_KEY")
FRED_API_KEY = os.environ.get("FRED_API_KEY")
fred = Fred(api_key = FRED_API_KEY)

save_path = f"{DATA_DIRECTORY}/eco"
os.makedirs(save_path, exist_ok = True)

from config import FRED_SERIES, ECOS_SERVICE_NAME, ECOS_REQUEST_TYPE, ECOS_LANGUAGE, ECOS_COUNT_START, ECOS_COUNT_END, ECOS_CODE, ECOS_INTERVAL, ECOS_START_DATE, ECOS_END_DATE, ECOS_STATIC_CODE_1, ECOS_STATOC_CODE_2

def saveDataToParquet(newDf, pPath):
    if Path(pPath).exists():
        old_data = pd.read_parquet(pPath)
        combined = pd.concat([old_data, newDf])
        combined = combined.drop_duplicates(
            subset = ["date"]
        ).sort_values("date")
    else:
        combined = newDf
    combined.to_parquet(pPath, index = False)
    print(f"Complete to Save Data to parquet : {pPath}")

def getFredData():
    for name, sid in FRED_SERIES.items():
        print(f"Collect FRED Data ... {name}")
        series = fred.get_series(sid)
        df = series.reset_index()
        df.columns = ["date", name]
        saveDataToParquet(df, f"{save_path}/{name}.parquet")

def getEcosData():
    print("Collect ECOS Data ...")
    # url = f"https://ecos.bok.or.kr/api/{ECOS_SERVICE_NAME}/{ECOS_API_KEY}/{ECOS_REQUEST_TYPE}/{ECOS_LANGUAGE}/kr_rate/1/1000/722Y001/M/2000/2025/0101000"
    url = f"https://ecos.bok.or.kr/api/{ECOS_SERVICE_NAME}/{ECOS_API_KEY}/{ECOS_REQUEST_TYPE}/{ECOS_LANGUAGE}/{ECOS_COUNT_START}/{ECOS_COUNT_END}/{ECOS_CODE}/{ECOS_INTERVAL}/{ECOS_START_DATE}/{ECOS_END_DATE}/"
    res = requests.get(url)
    data = res.json()
    rows = []
    print(data)
    for item in data['kr_rate']['row']:
        date = item['TIME']
        value = float(item['DATA_VALUE'])
        rows.append( (date, value) )
    df = pd.DataFrame(
        rows,
        cols = [ "date", "kr_base_rate" ]
    )
    df["date"] = pd.to_datetime(df["date"], format="%Y%m")
    saveDataToParquet(df, f"{save_path}/kr_base_rate.parquet")

def getEconomicIndicatorData():
    # getFredData()
    getEcosData()