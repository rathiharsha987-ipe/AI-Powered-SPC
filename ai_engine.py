# To look for hidden problems.
from sklearn.ensemble import IsolationForest

def get_ai_predictions(df, sensitivity=0.1):
    # The 'sensitivity' from the slider becomes the 'contamination' here
    model = IsolationForest(contamination=sensitivity, random_state=42)
    
    # We only train on the numeric samples S1-S5
    numeric_df = df.select_dtypes(include=['number'])
    preds = model.fit_predict(numeric_df)
    
    return preds  # 1 = Normal, -1 = Anomaly