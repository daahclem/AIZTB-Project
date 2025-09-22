import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import json

LOG_PATH = '../Logs/full_dataset.csv'
MODEL_PATH = 'rf_model.pkl'
ENCODERS_PATH = 'encoders.json'

# Load and preprocess data
def load_data():
    df = pd.read_csv(LOG_PATH)
    cat_cols = ['ev_user_id', 'device_id', 'role', 'location', 'charger_id']
    encoders = {}
    for col in cat_cols:
        unique = sorted(df[col].unique())
        mapping = {v: i for i, v in enumerate(unique)}
        df[col] = df[col].map(mapping)
        encoders[col] = mapping
    # Save encoders for inference
    with open(ENCODERS_PATH, 'w') as f:
        json.dump(encoders, f)
    X = df.drop(['timestamp', 'geo_coordinates', 'access_granted', 'behavior_context'], axis=1)
    y = (df['behavior_context'] == 'anomalous').astype(int)  # 1 = anomalous, 0 = normal
    return X, y

def train_supervised():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print('Supervised Model Performance:')
    print(classification_report(y_test, y_pred))
    print('Accuracy:', accuracy_score(y_test, y_pred))
    joblib.dump(clf, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')

if __name__ == '__main__':
    train_supervised()
