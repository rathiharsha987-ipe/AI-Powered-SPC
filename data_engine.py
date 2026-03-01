import numpy as np
import pandas as pd

def generate_factory_data():
    print("Simulating production line data...")
    np.random.seed(42)
    
    # 30 subgroups of 5 measurements each (Healthy process: Mean=50, Std=2)
    data = [np.random.normal(loc=50, scale=2, size=5) for _ in range(30)]
    df = pd.DataFrame(data, columns=['S1', 'S2', 'S3', 'S4', 'S5'])
    
    # --- THE SABOTAGE (Damage) ---
    # Injecting anomalies to test our Smart-SPC system
    df.iloc[12] = [65, 62, 68, 64, 66] # Sudden Mean Shift (Spike)
    df.iloc[20] = [40, 60, 35, 65, 50] # High Variance (Instability)
    
    df.to_csv("process_data.csv", index=False)
    print("✅ Created 'process_data.csv'. Ready for Phase 3!")

if __name__ == "__main__":
    generate_factory_data()