import os
import joblib

from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression

from utils.parquet_loader import loadParquet
from feature_engineering import createFeaturesNLabels

load_dotenv()

MODEL_DIRECTORY = os.environ.get("MODEL_DIRECTORY")

def trainkModel(symbol : str, kind = "stock"):
    print(f"모델 처리 시작 {kind} - {symbol}")
    df = loadParquet(symbol, kind)
    X, y = createFeaturesNLabels(df, window = 30)
    
    if len(X) < 10:
        print(f"Too small data. {len(X)} Rows")
        return 
    
    model = LogisticRegression()
    model.fit(X, y)
    
    output_path = f"{MODEL_DIRECTORY}/{kind}_{symbol}.pkl"
    joblib.dump(model, output_path)
    print(f"모델 저장 완료 : {output_path}")
    
if __name__ == "__main__":
    trainkModel("TSLA", "stock")
    trainkModel("BTCUSDT", "crypto")