import joblib
import numpy as np

def preprocess(prices : list[float]) -> list[float]:
    pct_changes = np.diff(prices) / prices[:-1]
    return pct_changes.tolist()

def predictSimpleTrend(
    assetType : str,
    price_list : list[float]
) -> int:
    X = preprocess(price_list)
    model = joblib.load(
        "ml_models/stock_simple_model.pkl" if assetType == "stock" else "ml_models/crypto_simple_model.pkl"
    )
    return int(model.predict([X])[0])