import os
import joblib

from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from utils.parquet_loader import loadParquet
from feature_engineering import createFeaturesNLabels
from .config import STOCK_SYMBOLS, CRYPTO_SYMBOLS

load_dotenv()

MODEL_DIRECTORY = os.environ.get("MODEL_DIRECTORY")

def trainModel(symbol : str, kind = "stock", model="logistic"):
    print(f"모델 처리 시작 {kind} - {symbol}")
    df = loadParquet(symbol, kind)
    X, y = createFeaturesNLabels(df, window = 30)
    
    if len(X) < 10:
        print(f"Too small data. {len(X)} Rows")
        return 
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    
    if model == "logistic" : 
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
    elif model == "xgboost" : 
        from xgboost import XGBClassifier
        model = XGBClassifier(
            n_estimators = 100,
            max_depth = 6,
            learning_rate = 0.1,
            use_label_encoder = False,
            eval_metric = "logloss"
        )
    elif model == "randomforest":
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(
            n_estimators = 100,
            max_depth = 10,
            random_state = 42
        )
    
    # Model training
    model.fit(X_train, y_train)
    
    # predict & estimate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"정확도 : {acc : 4f}")
    print("Classification Report")
    print(classification_report(y_test, y_pred))
    
    output_path = f"{MODEL_DIRECTORY}/simple_{kind}_{symbol}.pkl"
    joblib.dump(model, output_path)
    print(f"모델 저장 완료 : {output_path}")
    
if __name__ == "__main__":
    for symbol in STOCK_SYMBOLS:
        trainModel(symbol, "stock")
    for symbol in CRYPTO_SYMBOLS:
        trainModel(symbol, "crypto")