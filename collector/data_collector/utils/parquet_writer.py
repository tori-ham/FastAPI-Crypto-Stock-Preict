import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

parquetPath = os.environ.get("PARQUET_PATH")


def saveDataToParquet(
    symbol : str,
    df : pd.DataFrame,
    kind : str = "stock"
):
    folder = f"{parquetPath}/parquetData/{kind}"
    os.makedirs(folder, exist_ok=True)
    
    file_path = f"{folder}/{symbol}.parquet"
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns]
    
    rename_map = {}
    for col in df.columns:
        if "date" in col.lower() or "datetime" in col.lower():
            rename_map[col] = "datetime"
        elif "open" in col.lower():
            rename_map[col] = "open"
        elif "high" in col.lower():
            rename_map[col] = "high"
        elif "low" in col.lower():
            rename_map[col] = "low"
        elif "close" in col.lower():
            rename_map[col] = "close"
        elif "volume" in col.lower():
            rename_map[col] = "volume"
    df = df.rename(columns = rename_map)
    
    if os.path.exists(file_path):
        existing_df = pd.read_parquet(file_path)
        combined_df = pd.concat( [ existing_df, df ] ).drop_duplicates(subset = ["datetime"]).sort_values("datetime")
    else:
        combined_df = df
    # combined_df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    combined_df.to_parquet(file_path, index = False)
    print(f"{symbol} : {len(combined_df)} Rows 저장 완료")