import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

# 1000개의 샘플에 대해 29개의 변화율
X = np.random.randn(1000, 29)
y = (X.sum(axis = 1) > 0).astype(int)

model = LogisticRegression()
model.fit(X, y)
joblib.dump(model, "/Users/tori/dev/only_tori/tori_stock_predict/predictor/ml_models/crypto_simple_model.pkl")
