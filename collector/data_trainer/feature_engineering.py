import pandas as pd
import numpy as np

def createFeaturesNLabels(
    df : pd.DataFrame,
    window : int = 30
) : 
    prices = df["close"].values
    X = []
    y = []
    
    for i in range(len(prices) - window - 1):
        window_data = prices[ i : i + window ]
        label = int( prices[ i + window ] > prices[ i + window - 1 ] ) # up = 1, down = 0
        X.append(np.diff(window_data) / window_data[ : -1 ])
        y.append(label)
    
    return np.array(X), np.array(y)
        