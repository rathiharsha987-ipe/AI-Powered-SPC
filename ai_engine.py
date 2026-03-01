import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def run_ai_anomaly_detection():
    # Load data
    df = pd.read_csv("process_data.csv")
    
    # Initialize and Isolation Forest
    model = IsolationForest(contamination=0.1, random_state=42)
    
    # We only train on the numeric samples (S1-S5), not the whole 
    preds = model.fit_predict(df)
    
    # Tag the results
    df['AI_Status'] = ["Anomaly" if p == -1 else "Normal" for p in preds]
    
    # Calculate X-bar for plotting 
    x_bar = df.mean(axis=1, numeric_only=True)
    
    # Identify anomalies for the scatter plot
    anomalies = df[df['AI_Status'] == "Anomaly"]
    
    print(f"AI identified {len(anomalies)} anomalies.")
    print(anomalies[['AI_Status']]) 

    # Visualization
    plt.figure(figsize=(12, 5))
    plt.plot(x_bar, marker='o', color='lightgrey', label='Process Flow', alpha=0.6)
    
    # Highlight AI-detected points in orange
    plt.scatter(anomalies.index, x_bar[anomalies.index], 
                color='orange', s=100, label='AI Flagged Anomaly', zorder=5)
    
    plt.title("AI-Powered Anomaly Detection")
    plt.xlabel("Subgroup Index")
    plt.ylabel("Mean Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_ai_anomaly_detection()