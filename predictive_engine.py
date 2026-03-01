import numpy as np
from sklearn.linear_model import LinearRegression

def get_next_prediction(df):
    x_bar = df.mean(axis=1, numeric_only=True).values
    lookback = 10
    
    # Prepare the last 10 points for the "future" guess
    X = np.arange(lookback).reshape(-1, 1)
    y = x_bar[-lookback:]
    
    model = LinearRegression().fit(X, y)
    prediction = model.predict(np.array([[lookback]]))[0]
    
    return prediction