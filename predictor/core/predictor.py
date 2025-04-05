import joblib
import numpy as np

def preprocess(prices : list[float]) -> list[float]:
    pct_changes = np.diff(prices) / prices[:-1]
    return pct_changes.tolist()

def predictTrend(
    price_list : list[float]
) -> int:
    X = preprocess(price_list)
    model = joblib.load("ml_models/simple_model.pkl")
    return int(model.predict([X])[0])