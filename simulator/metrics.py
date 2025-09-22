def evaluate_metrics(log_file_path):
    import pandas as pd

    df = pd.read_csv(log_file_path)

    print("\n📊 Evaluation Metrics:")
    print(f"Total Records: {len(df)}")
    print(f"Total Access Granted: {df['access_granted'].sum()}")
    print(f"Total Access Denied: {(~df['access_granted']).sum()}")

    accuracy = df['access_granted'].mean()
    print(f"✅ Access Accuracy: {accuracy:.2f}")

    far = df[(df['risk_score'] > 0.6) & (df['access_granted'] == True)]
    print(f"🚨 False Acceptance Rate: {len(far) / len(df):.2f}")

    frr = df[(df['risk_score'] < 0.4) & (df['access_granted'] == False)]
    print(f"⛔ False Rejection Rate: {len(frr) / len(df):.2f}")

    print(f"📉 Average Risk Score: {df['risk_score'].mean():.2f}")

    adr = (~df['access_granted']).sum() / len(df)
    print(f"🔒 Access Denial Rate: {adr:.2f}")

    print("\n📚 Policy Match Breakdown:")
    print(df.groupby('policy_type')['access_granted'].value_counts(normalize=True).unstack().fillna(0).round(2))
