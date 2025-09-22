import csv
import os
import random
from datetime import datetime, timedelta
import sys

# Optional: Use pandas for balancing
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# Configuration
NORMAL_LOGS = 26000
ANOMALOUS_LOGS = 24000
LOG_FILE = "logs/full_dataset.csv"
os.makedirs("logs", exist_ok=True)

# Constants
USER_ROLES = ["user", "admin", "fleet"]
DEVICES = ["mobile", "tablet", "dashboard", "spoofed_device", "unknown_device"]
LOCATIONS = ["london", "manchester", "birmingham", "foreign"]
CHARGER_IDS = [f"CHG-{i:03d}" for i in range(100)]
HOURS = list(range(24))

# Simulate a MAC address
def generate_mac():
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

# Geo-coordinate generator (UK based)
def generate_geo(role):
    if role == "fleet":
        return f"{random.uniform(52.4, 53.5):.5f},{random.uniform(-1.9, -0.9):.5f}"
    return f"{random.uniform(51.3, 53.5):.5f},{random.uniform(-2.3, 0.2):.5f}"

# Risk scoring function
def compute_risk(context):
    score = 0.0
    if context["behavior_context"] == "anomalous":
        score += 0.4
    if context["device_id"] in ["spoofed_device", "unknown_device"]:
        score += 0.2
    if context["location"] == "foreign":
        score += 0.1
    if context["hour"] < 6 or context["hour"] > 22:
        score += 0.2
    return round(min(score, 1.0), 3)

# Simulate a single legitimate log
def simulate_legit_log(user_id):
    hour = random.choice(HOURS)
    role = random.choice(USER_ROLES)
    entry = {
        "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(0, 100000))).isoformat(),
        "ev_user_id": user_id,
        "device_id": generate_mac(),
        "role": role,
        "location": random.choice(["london", "manchester", "birmingham"]),
        "geo_coordinates": generate_geo(role),
        "charger_id": random.choice(CHARGER_IDS),
        "session_duration": round(random.uniform(5.0, 120.0), 2),
        "power_usage": round(random.uniform(1.0, 50.0), 2),
        "behavior_context": "normal",
        "hour": hour
    }
    entry["risk_score"] = compute_risk(entry)
    entry["access_granted"] = entry["risk_score"] < 0.5
    return entry

# Simulate a single attacker log
def simulate_attack_log(index):
    hour = random.choice([1, 2, 3, 23])
    role = random.choice(USER_ROLES)
    attack = {
        "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(0, 100000))).isoformat(),
        "ev_user_id": f"attacker_{index}",
        "device_id": random.choice(["spoofed_device", "unknown_device"]),
        "role": role,
        "location": "foreign",
        "geo_coordinates": generate_geo(role),
        "charger_id": random.choice(CHARGER_IDS),
        "session_duration": round(random.uniform(1.0, 20.0), 2),
        "power_usage": round(random.uniform(0.5, 10.0), 2),
        "behavior_context": "anomalous",
        "hour": hour
    }
    attack["risk_score"] = compute_risk(attack)
    attack["access_granted"] = attack["risk_score"] < 0.7  # Some attackers may bypass
    return attack

def generate_full_dataset():
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "ev_user_id", "device_id", "role", "location", "geo_coordinates",
            "charger_id", "session_duration", "power_usage", "behavior_context",
            "risk_score", "access_granted"
        ])

        for i in range(NORMAL_LOGS):
            row = simulate_legit_log(f"evuser_{i % 100:03d}")
            writer.writerow([row[k] for k in row if k != "hour"])

        for i in range(ANOMALOUS_LOGS):
            row = simulate_attack_log(i)
            writer.writerow([row[k] for k in row if k != "hour"])

    print(f"✅ Dataset generated at {LOG_FILE} with {NORMAL_LOGS + ANOMALOUS_LOGS} entries.")

def generate_balanced_dataset():
    if not HAS_PANDAS:
        print("❌ pandas is required for balancing. Please install pandas and try again.")
        sys.exit(1)
    df = pd.read_csv(LOG_FILE)
    label_col = 'behavior_context'
    min_count = df[label_col].value_counts().min()
    df_balanced = df.groupby(label_col, group_keys=False).apply(lambda x: x.sample(min_count, random_state=42)).reset_index(drop=True)
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    df_balanced.to_csv('logs/dataset.csv', index=False)
    print(f"✅ Balanced dataset saved to logs/dataset.csv with {len(df_balanced)} rows.")

if __name__ == "__main__":
    if '--balanced' in sys.argv:
        generate_balanced_dataset()
    else:
        generate_full_dataset()
