import pandas as pd
import random

def evaluate_access(risk_score):
    if risk_score > 0.7:
        return False
    elif risk_score < 0.4:
        return True
    else:
        return random.choice([True, False])

def evaluate_metrics(log_file_path):
    df = pd.read_csv(log_file_path)
    print("\n📊 Evaluation Metrics:")
    print(f"Total Records: {len(df)}")
    print(f"Total Access Granted: {df['access_granted'].sum()}")
    print(f"Total Access Denied: {(~df['access_granted']).sum()}")
    print(f"Access Accuracy: {df['access_granted'].mean():.2f}")
    print(f"Average Risk Score: {df['risk_score'].mean():.2f}")
    print(df['policy_type'].value_counts())