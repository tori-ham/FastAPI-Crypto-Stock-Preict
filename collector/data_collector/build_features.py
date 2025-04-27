import os 
import pandas as pd
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

DATA_DIRECTORY = os.environ.get("DATA_DIRECTORY")
PARQUET_PATH = os.environ.get("PARQUET_PATH")
STOCK_DB_PATH = os.environ.get("STOCK_DB_PATH")


def build_features(symbol = "TSLA", kind = "stock"):
    data_path = f"{PARQUET_PATH}/{kind}/{symbol}.parquet"
    df = pd.read_parquet(data_path)
    df["date"] = pd.to_datetime(df["datetime"]).dt.date
    
    economic_indicator_dir = Path("data/eco")
    for eco_ind_file in economic_indicator_dir.glob("*.parquet"):
        eco_ind_df = pd.read_parquet(eco_ind_file)
        eco_ind_df["date"] = pd.to_datetime(eco_ind_df["date"]).dt.date
        df = df.merge(
            eco_ind_df,
            on = "date",
            how = "left"
        )
    
    news_sentiment_dir = Path("data/news_sentiment")
    date_set = set(df["date"].unique())
    rows = []
    for path in news_sentiment_dir.glob("*.parquet"):
        news_sentiment_df = pd.read_parquet(path)
        news_sentiment_df = news_sentiment_df[news_sentiment_df["date"].isin(date_set)]
        grouped = news_sentiment_df.groupby("date")["sentiment_value"].mean().reset_index()
        grouped.columns = ["date", "news_sentiment"]
        rows.append(grouped)
    
    if rows:
        sentiment_df = pd.concat(rows).drop_duplicates("date")
        df = df.merge(
            sentiment_df,
            on = "date",
            how = "left"
        )
    else:
        df["news_sentiment"] = 0.0
    
    output_dir = f"data/features/{kind}"
    os.makedirs(output_dir, exist_ok = True)
    df.to_parquet(f"{output_dir}/{symbol}_feature.parquet", index = False)
    
    print(f"Complete to Build FeatureSet -> {output_dir}/{symbol}_features.parquet")
    