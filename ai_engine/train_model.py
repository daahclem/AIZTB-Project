# AI model training using simulation logs
import torch
import torch.optim as optim
import pandas as pd
from risk_model import Autoencoder

LOG_PATH = '../Logs/full_dataset.csv'
MODEL_PATH = 'model.pth'

# Use the correct CSV columns
def label_encode(df, columns):
    encoders = {}
    for col in columns:
        unique = sorted(df[col].unique())
        mapping = {v: i for i, v in enumerate(unique)}
        df[col] = df[col].map(mapping)
        encoders[col] = mapping
    return df, encoders

def load_data():
    print(f"Loading data from {LOG_PATH} ...")
    try:
        df = pd.read_csv(LOG_PATH)
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        raise
    print(f"Loaded dataframe with shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    cat_cols = ['ev_user_id', 'device_id', 'role', 'location', 'charger_id']
    df, encoders = label_encode(df, cat_cols)
    drop_cols = ['timestamp', 'geo_coordinates', 'behavior_context']
    if 'access_granted' in df.columns:
        drop_cols.append('access_granted')
    print(f"Dropping columns: {drop_cols}")
    X = df.drop(drop_cols, axis=1).values
    print(f"Feature matrix shape: {X.shape}")
    # Save encoders for inference
    with open('encoders.json', 'w') as f:
        import json
        json.dump(encoders, f)
    return torch.tensor(X, dtype=torch.float32), X.shape[1]

def train():
    data, input_dim = load_data()
    model = Autoencoder(input_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.MSELoss()
    for epoch in range(20):
        optimizer.zero_grad()
        recon = model(data)
        loss = loss_fn(recon, data)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
    torch.save(model.state_dict(), MODEL_PATH)
    print("Model trained and saved.")

if __name__ == '__main__':
    train()
