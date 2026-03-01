#Calculates the Control Limits for the X-bar Chart based on the subgroup data.
import pandas as pd

def get_spc_limits(df):
    x_bar = df.mean(axis=1, numeric_only=True)
    r_range = df.max(axis=1, numeric_only=True) - df.min(axis=1, numeric_only=True)
    
    A2 = 0.577  # Statistical constant for subgroup size n=5
    grand_mean = x_bar.mean()
    mean_r = r_range.mean()
    
    ucl = grand_mean + (A2 * mean_r)
    lcl = grand_mean - (A2 * mean_r)
    
    return ucl, lcl, grand_mean