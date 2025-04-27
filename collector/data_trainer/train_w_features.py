import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

def train_with_feature(
    symbol : str,
    kind : str = "stock",
    model_type = "rf"
):
    feature_path = f"data/features/{kind}/{symbol}_features.parquet"
    model_dir = "models"
    os.makedirs(model_dir, exist_ok = True)
    
    df = pd.read_parquet(feature_path)
    
    df = df.sort_values("datetime")
    df["future_close"] = df["close"].shift(-1)
    df["target"] = (df["future_close"] > df["close"]).astype(int)
    df = df.dropna()
    
    X = df.drop(columns = [
        "datetime",
        "future_close",
        "targe"
    ])
    y = df["target"]
    
    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.2, random_state = 42 )
    if model_type == "rf":
        model = RandomForestClassifier(
            n_estimators = 100,
            max_depth = 8,
            random_state = 42
        )
    else:
        raise ValueError("Not Supported Model : {model_type}")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"[{kind.upper()}] Complete to Train Model {symbol}")
    print(f" Accuracy : {acc : .4f}")
    print("Classification Report")
    print(classification_report(y_test, y_pred))
    
    model_path = f"{model_dir}/model_from_features_{kind}_{symbol}.pkl"
    joblib.dump(model, model_path)
    print(f"Complete to Save Model - {model_path}")