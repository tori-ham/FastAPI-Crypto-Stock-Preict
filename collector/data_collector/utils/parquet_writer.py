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
    
    if os.path.exists(file_path):
        existing_df = pd.read_parquet(file_path)
        combined_df = pd.concat( [ existing_df, df ] ).drop_duplicates(subset = ["datetime"]).sort_values("datetime")
    else:
        combined_df = df
    combined_df.to_parquet(file_path, index = False)
    print(f"{symbol} : {len(combined_df)} Rows 저장 완료")