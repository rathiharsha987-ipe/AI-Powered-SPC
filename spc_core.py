import pandas as pd
import matplotlib.pyplot as plt

def run_statistical_control():
    df = pd.read_csv("process_data.csv")
    
    # 1. Calculate subgroup Mean (X-bar) and Range (R)
    x_bar = df.mean(axis=1)
    r_range = df.max(axis=1) - df.min(axis=1)
    
    # 2. Calculate Control Limits (Constants for n=5)
    A2 = 0.577
    grand_mean = x_bar.mean()
    mean_r = r_range.mean()
    
    ucl = grand_mean + (A2 * mean_r)
    lcl = grand_mean - (A2 * mean_r)
    
    # 3. Visualization
    plt.figure(figsize=(10, 4))
    plt.plot(x_bar, marker='o', color='b', label='X-bar (Subgroup Mean)')
    plt.axhline(ucl, color='r', linestyle='--', label=f'UCL ({ucl:.2f})')
    plt.axhline(lcl, color='r', linestyle='--', label=f'LCL ({lcl:.2f})')
    plt.axhline(grand_mean, color='g', label='Grand Mean')
    
    plt.title("Traditional X-bar Control Chart")
    plt.legend()
    plt.savefig("spc_chart.png")
    print(f"📊 Chart generated. UCL: {ucl:.2f}, LCL: {lcl:.2f}")
    plt.show()

if __name__ == "__main__":
    run_statistical_control()