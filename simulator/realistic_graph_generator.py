import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")
np.random.seed(42)

# Constants
NUM_SESSIONS = 10000
NUM_USERS = 20
NUM_CHARGERS = 10
SESSION_DURATION = np.random.randint(5, 121, NUM_SESSIONS)
POWER_USAGE = np.round(np.random.uniform(1.2, 22, NUM_SESSIONS), 2)
TIME_OF_DAY = np.random.choice(["morning", "afternoon", "evening", "off_hours"], NUM_SESSIONS, p=[0.25, 0.35, 0.25, 0.15])
LOCATIONS = np.random.choice(["London", "Manchester", "Birmingham", "anomaly"], NUM_SESSIONS, p=[0.4, 0.3, 0.25, 0.05])
POLICIES = np.random.choice(["RBAC", "ABAC", "MAC", "DAC"], NUM_SESSIONS, p=[0.5, 0.2, 0.2, 0.1])
ROLES = np.random.choice(["User", "Admin", "Fleet"], NUM_SESSIONS, p=[0.7, 0.2, 0.1])

# Simulate session context
sessions = pd.DataFrame({
    "session_id": np.arange(NUM_SESSIONS),
    "user_id": np.random.randint(1, NUM_USERS+1, NUM_SESSIONS),
    "charger_id": np.random.randint(1, NUM_CHARGERS+1, NUM_SESSIONS),
    "session_duration": SESSION_DURATION,
    "power_usage": POWER_USAGE,
    "time_of_day": TIME_OF_DAY,
    "location": LOCATIONS,
    "policy_type": POLICIES,
    "role": ROLES
})

# Assign legitimate vs attack BASED ON ROLE AND TIME OF DAY
role_attack_base = {"User": 0.08, "Admin": 0.14, "Fleet": 0.18}
time_attack_mod = {"morning": 0.8, "afternoon": 0.6, "evening": 1.1, "off_hours": 1.6}
role_risk_means = {"User": 0.26, "Admin": 0.33, "Fleet": 0.36}
role_risk_attack = {"User": 0.75, "Admin": 0.81, "Fleet": 0.86}
time_risk_mod = {"morning": -0.04, "afternoon": -0.07, "evening": 0.03, "off_hours": 0.09}

behavior_context = []
risk_score = []
for idx, row in sessions.iterrows():
    role = row["role"]
    tod = row["time_of_day"]
    # Attack probability increases at night/off_hours, especially for privileged roles
    attack_prob = role_attack_base[role] * time_attack_mod[tod]
    is_attack = np.random.rand() < attack_prob
    behavior_context.append("anomalous" if is_attack else "normal")
    # Risk means are higher at risky times
    if is_attack:
        risk = np.clip(np.random.normal(role_risk_attack[role] + time_risk_mod[tod], 0.08), 0, 1)
    else:
        risk = np.clip(np.random.normal(role_risk_means[role] + time_risk_mod[tod], 0.08), 0, 1)
    risk_score.append(risk)
sessions["behavior_context"] = behavior_context
sessions["risk_score"] = risk_score
RISK_SCORE_THRESHOLD = 0.6

# AI and Non-AI access decisions
sessions["access_granted_ai"] = (sessions["risk_score"] < RISK_SCORE_THRESHOLD)
# No AI baseline: role-based error rates
role_fa = {"User": 0.07, "Admin": 0.13, "Fleet": 0.16}  # false accept
role_fr = {"User": 0.03, "Admin": 0.06, "Fleet": 0.08}  # false reject
sessions["access_granted_noai"] = sessions["behavior_context"] == "normal"
for role in ["User", "Admin", "Fleet"]:
    fa_noai = np.random.rand(NUM_SESSIONS) < role_fa[role]
    fr_noai = np.random.rand(NUM_SESSIONS) < role_fr[role]
    mask_attack = (sessions["role"] == role) & (sessions["behavior_context"] == "anomalous")
    mask_legit = (sessions["role"] == role) & (sessions["behavior_context"] == "normal")
    sessions.loc[mask_attack & fa_noai, "access_granted_noai"] = True
    sessions.loc[mask_legit & fr_noai, "access_granted_noai"] = False

# False acceptance/rejection (simulate AI imperfection)
FAI = np.random.rand(NUM_SESSIONS) < 0.03  # 3% false acceptance (attack granted)
FRI = np.random.rand(NUM_SESSIONS) < 0.02  # 2% false rejection (legit denied)
sessions.loc[(sessions["behavior_context"] == "anomalous") & (FAI), "access_granted_ai"] = True
sessions.loc[(sessions["behavior_context"] == "normal") & (FRI), "access_granted_ai"] = False

# Latency, blockchain, PET
sessions["decision_latency_ai"] = np.random.normal(180, 25, NUM_SESSIONS)
sessions["decision_latency_noai"] = np.random.normal(120, 20, NUM_SESSIONS)
sessions["blockchain_delay"] = np.random.normal(200, 40, NUM_SESSIONS)
sessions["pet_time"] = np.random.normal(80, 15, NUM_SESSIONS)

# AI override
sessions["ai_override"] = sessions["access_granted_ai"] != sessions["access_granted_noai"]

# Session validity (replay/spoof): maximum realism
# Only 2% of all sessions are invalid, with higher probability for anomalous
validity = []
for idx, row in sessions.iterrows():
    if row["behavior_context"] == "anomalous":
        # 8% of anomalous sessions are invalid
        validity.append("invalid" if np.random.rand() < 0.08 else "valid")
    else:
        # 0.8% of normal sessions are invalid (rare false invalids)
        validity.append("invalid" if np.random.rand() < 0.008 else "valid")
sessions["session_validity"] = validity

# Save to CSV for reproducibility
os.makedirs("logs", exist_ok=True)
sessions.to_csv("logs/realistic_sim_data.csv", index=False)

# 1. Access Accuracy vs Sessions
sessions["correct_ai"] = (
    (sessions["behavior_context"] == "normal") & (sessions["access_granted_ai"]) |
    (sessions["behavior_context"] == "anomalous") & (~sessions["access_granted_ai"])
)
acc_ai = sessions["correct_ai"].rolling(200).mean() * 100
sessions["correct_noai"] = (
    (sessions["behavior_context"] == "normal") & (sessions["access_granted_noai"]) |
    (sessions["behavior_context"] == "anomalous") & (~sessions["access_granted_noai"])
)
acc_noai = sessions["correct_noai"].rolling(200).mean() * 100
plt.figure(figsize=(10,6))
plt.plot(acc_noai, label="No AI")
plt.plot(acc_ai, label="AI-enabled")
plt.xlabel("Sessions")
plt.ylabel("Accuracy (%)")
plt.title("Access Accuracy vs Sessions")
plt.legend()
plt.tight_layout()
plt.savefig("logs/access_accuracy_vs_sessions.png", dpi=150)
plt.close()

# 2. FAR & FRR Comparison
far_ai = ((sessions["behavior_context"] == "anomalous") & (sessions["access_granted_ai"])).rolling(200).mean()
far_noai = ((sessions["behavior_context"] == "anomalous") & (sessions["access_granted_noai"])).rolling(200).mean()
frr_ai = ((sessions["behavior_context"] == "normal") & (~sessions["access_granted_ai"])).rolling(200).mean()
frr_noai = ((sessions["behavior_context"] == "normal") & (~sessions["access_granted_noai"])).rolling(200).mean()
plt.figure(figsize=(10,6))
plt.plot(far_noai, label="FAR No AI")
plt.plot(frr_noai, label="FRR No AI")
plt.plot(far_ai, label="FAR AI")
plt.plot(frr_ai, label="FRR AI")
plt.ylabel("Rate (%)")
plt.xlabel("Sessions")
plt.title("FAR & FRR Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("logs/far_frr_comparison.png", dpi=150)
plt.close()

# 3. Risk Score Distribution
plt.figure(figsize=(10,6))
sns.histplot(sessions[sessions["behavior_context"]=="normal"]["risk_score"], bins=20, color="#3b82f6", label="Legitimate", kde=False)
sns.histplot(sessions[sessions["behavior_context"]=="anomalous"]["risk_score"], bins=20, color="#ff9100", label="Malicious", kde=False)
plt.legend()
plt.xlabel("Risk Score")
plt.ylabel("Count")
plt.title("Risk Score Distribution (AI)")
plt.tight_layout()
plt.savefig("logs/risk_score_distribution.png", dpi=150)
plt.close()

# 4. Access Denial by Risk Buckets
risk_bins = pd.cut(sessions["risk_score"], bins=[0,0.2,0.4,0.6,0.8,1.0], include_lowest=True)
denials = sessions.loc[~sessions["access_granted_ai"]]
denial_counts = denials.groupby(risk_bins).size()
plt.figure(figsize=(10,6))
denial_counts.plot(kind="bar")
plt.xlabel("Risk Score Bin")
plt.ylabel("# of Denials")
plt.title("Access Denials by Risk Buckets (AI)")
plt.tight_layout()
plt.savefig("logs/access_denial_by_risk.png", dpi=150)
plt.close()

# 5. Policy Type Usage
plt.figure(figsize=(8,6))
(sessions["policy_type"].value_counts(normalize=True)).plot(kind="bar")
plt.ylabel("% of Matches")
plt.title("Policy Type Usage")
plt.tight_layout()
plt.savefig("logs/policy_type_usage.png", dpi=150)
plt.close()

# 6. Decision Latency Over Time
plt.figure(figsize=(10,8))
plt.plot(sessions["decision_latency_noai"], label="No AI", alpha=0.6)
plt.plot(sessions["decision_latency_ai"], label="AI", alpha=0.6)
plt.xlabel("Timestamp")
plt.ylabel("Latency (ms)")
plt.title("Decision Latency Over Time")
plt.legend()
plt.tight_layout()
plt.savefig("logs/decision_latency_over_time.png", dpi=150)
plt.close()

# 7. ADR vs Time of Day
time_order = ["morning", "afternoon", "evening", "off_hours"]
adr_ai = 1 - sessions.groupby("time_of_day")["access_granted_ai"].mean().reindex(time_order)
adr_noai = 1 - sessions.groupby("time_of_day")["access_granted_noai"].mean().reindex(time_order)
plt.figure(figsize=(8,6))
width = 0.35
x = np.arange(len(time_order))
plt.bar(x - width/2, adr_noai, width, label="No AI", color="#60a5fa")
plt.bar(x + width/2, adr_ai, width, label="AI-enabled", color="#a78bfa")
plt.xticks(x, time_order)
plt.title("Access Denial Rate vs Time of Day (ADR)")
plt.ylabel("% Denied")
plt.xlabel("Time of Day")
plt.ylim(0, 1)
plt.legend()
plt.tight_layout()
plt.savefig("logs/adr_vs_timeofday_compare.png", dpi=150)
plt.close()

# 8. Access Decisions by Role
roles = ["User", "Admin", "Fleet"]
accept_ai = sessions.groupby("role")["access_granted_ai"].mean().reindex(roles)
accept_noai = sessions.groupby("role")["access_granted_noai"].mean().reindex(roles)
plt.figure(figsize=(8,6))
x = np.arange(len(roles))
plt.bar(x - width/2, accept_noai, width, label="No AI", color="#60a5fa")
plt.bar(x + width/2, accept_ai, width, label="AI-enabled", color="#a78bfa")
plt.xticks(x, roles)
plt.ylabel("Acceptance Rate")
plt.title("Access Decisions by Role (With & Without AI)")
plt.ylim(0, 1)
plt.legend()
plt.tight_layout()
plt.savefig("logs/access_by_role_compare.png", dpi=150)
plt.close()

# 12. PET – IAM Decision Time
plt.figure(figsize=(10,6))
plt.plot(sessions["pet_time"], label="AI-enabled", color="#a78bfa", alpha=0.8)
plt.plot(np.random.normal(60, 10, len(sessions)), label="No AI", color="#60a5fa", alpha=0.8)
plt.title("Policy Evaluation Time (PET) With & Without AI")
plt.ylabel("Time (ms)")
plt.xlabel("Sessions")
plt.legend()
plt.tight_layout()
plt.savefig("logs/pet_iam_decision_time_compare.png", dpi=150)
plt.close()

# 8b. Access Decisions by Behavior Type (show error rates)
plt.figure(figsize=(7,5))
behavior_types = ["normal", "anomalous"]
results = []
for behavior in behavior_types:
    total = (sessions["behavior_context"] == behavior).sum()
    granted = ((sessions["behavior_context"] == behavior) & (sessions["access_granted_ai"])).sum()
    denied = ((sessions["behavior_context"] == behavior) & (~sessions["access_granted_ai"])).sum()
    results.append({"behavior": behavior, "decision": "Granted", "rate": granted/total})
    results.append({"behavior": behavior, "decision": "Denied", "rate": denied/total})
df_plot = pd.DataFrame(results)
sns.barplot(data=df_plot, x="behavior", y="rate", hue="decision", palette=["#ff9100", "#2563eb"])
plt.ylim(0,1)
plt.ylabel("Proportion")
plt.title("Access Decisions by Behavior Type (AI)")
plt.tight_layout()
plt.savefig("logs/access_by_behavior_type.png", dpi=150)
plt.close()

# 9. Session Validity Ratio
plt.figure(figsize=(10,6))
sessions["valid_numeric"] = (sessions["session_validity"] == "valid").astype(int)
plt.plot(sessions["valid_numeric"]) 
plt.title("Session Validity Ratio")
plt.ylabel("Valid=1 / Invalid=0")
plt.xlabel("Session Index")
plt.tight_layout()
plt.savefig("logs/session_validity_ratio.png", dpi=150)
plt.close()

# 10. Blockchain Logging Delay
plt.figure(figsize=(10,6))
plt.plot(sessions["blockchain_delay"])
plt.title("Blockchain Logging Delay (AI)")
plt.ylabel("Time (ms)")
plt.xlabel("Sessions")
plt.tight_layout()
plt.savefig("logs/blockchain_logging_delay.png", dpi=150)
plt.close()

# 11. AI Override Frequency
plt.figure(figsize=(10,6))
plt.plot(sessions["ai_override"].rolling(200).mean())
plt.title("AI Override Frequency (AI)")
plt.ylabel("% Override")
plt.xlabel("Sessions")
plt.tight_layout()
plt.savefig("logs/ai_override_frequency.png", dpi=150)
plt.close()

# 12. PET – IAM Decision Time
plt.figure(figsize=(10,6))
plt.plot(sessions["pet_time"])
plt.title("Policy Evaluation Time (PET)")
plt.ylabel("Time (ms)")
plt.xlabel("Sessions")
plt.tight_layout()
plt.savefig("logs/pet_iam_decision_time.png", dpi=150)
plt.close()

print("All realistic, publication-ready graphs generated in logs/ directory.")
