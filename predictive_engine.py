import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def run_prediction():
    # 1. Load data and calculate means
    df = pd.read_csv("process_data.csv")
    x_bar = df.mean(axis=1, numeric_only=True).values
    
    # 2. Setup Linear Regression
    # We use the last 10 subgroups to predict the 31st point
    lookback = 10
    X = np.arange(len(x_bar[-lookback:])).reshape(-1, 1)
    y = x_bar[-lookback:]
    
    model = LinearRegression().fit(X, y)
    
    # Predict the next subgroup mean (index 10 in our window)
    next_idx = np.array([[lookback]])
    prediction = model.predict(next_idx)[0]
    
    print(f" Predictive Analysis Complete.")
    print(f"Current Mean: {x_bar[-1]:.2f} | Predicted Next Mean: {prediction:.2f}")

    # 3. Visualization of the Trend
    plt.figure(figsize=(10, 4))
    plt.plot(range(len(x_bar)), x_bar, marker='o', label='Actual Data')
    
    # Add the prediction point in purple
    plt.scatter(len(x_bar), prediction, color='purple', marker='X', s=200, label='AI Forecast')
    
    # Draw a trend line for the last 10 points
    trend_line = model.predict(np.arange(lookback + 1).reshape(-1, 1))
    plt.plot(range(len(x_bar)-lookback, len(x_bar)+1), trend_line, 'p--', alpha=0.5)

    plt.axhline(53.65, color='r', linestyle='--', label='UCL (Warning Level)')
    plt.title("Predictive Process Forecasting")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_prediction()