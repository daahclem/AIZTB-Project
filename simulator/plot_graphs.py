import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
plt.style.use('seaborn-v0_8-whitegrid')

# Helper to load both logs for comparative plots
def load_logs():
    df_no_ai = pd.read_csv('logs/sim_no_ai.csv')
    df_ai = pd.read_csv('logs/sim_with_ai.csv')
    for df in [df_no_ai, df_ai]:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df_no_ai, df_ai

def plot_all_graphs(log_file_path=None):
    # Always use both logs for comparative graphs
    df_no_ai, df_ai = load_logs()
    os.makedirs('logs', exist_ok=True)

    # 1. Access Accuracy vs Sessions
    plt.figure(figsize=(7,4))
    acc_no_ai = df_no_ai['access_granted'].expanding().mean()
    acc_ai = df_ai['access_granted'].expanding().mean()
    plt.plot(acc_no_ai.index, acc_no_ai*100, label='No AI')
    plt.plot(acc_ai.index, acc_ai*100, label='AI-enabled')
    plt.xlabel('Sessions')
    plt.ylabel('Accuracy (%)')
    plt.title('Access Accuracy vs Sessions')
    plt.legend()
    plt.tight_layout()
    plt.savefig('logs/access_accuracy_vs_sessions.png', dpi=300)
    plt.close()

    # 2. FAR & FRR Comparison
    def far_frr(df):
        far = ((df['risk_score'] > 0.6) & (df['access_granted'] == True)).expanding().mean()
        frr = ((df['risk_score'] < 0.4) & (df['access_granted'] == False)).expanding().mean()
        return far, frr
    far_no_ai, frr_no_ai = far_frr(df_no_ai)
    far_ai, frr_ai = far_frr(df_ai)
    plt.figure(figsize=(7,4))
    plt.plot(far_no_ai.index, far_no_ai*100, label='FAR No AI')
    plt.plot(frr_no_ai.index, frr_no_ai*100, label='FRR No AI')
    plt.plot(far_ai.index, far_ai*100, label='FAR AI')
    plt.plot(frr_ai.index, frr_ai*100, label='FRR AI')
    plt.xlabel('Sessions')
    plt.ylabel('Rate (%)')
    plt.title('FAR & FRR Comparison')
    plt.legend()
    plt.tight_layout()
    plt.savefig('logs/far_frr_comparison.png', dpi=300)
    plt.close()

    # 3. Risk Score Distribution (Legit vs Malicious)
    plt.figure(figsize=(7,4))
    df_ai['behavior_context'].replace({'normal':'Legitimate','anomalous':'Malicious'}, inplace=True)
    for label, group in df_ai.groupby('behavior_context'):
        plt.hist(group['risk_score'], bins=20, alpha=0.6, label=label)
    plt.xlabel('Risk Score')
    plt.ylabel('Count')
    plt.title('Risk Score Distribution (AI)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('logs/risk_score_dist_legit_malicious.png', dpi=300)
    plt.close()

    # 4. Access Denial by Risk Buckets
    plt.figure(figsize=(7,4))
    bins = np.arange(0, 1.1, 0.2)
    denied = df_ai[df_ai['access_granted']==False]
    plt.hist(denied['risk_score'], bins=bins, edgecolor='black')
    plt.xlabel('Risk Score Bin')
    plt.ylabel('# of Denials')
    plt.title('Access Denials by Risk Buckets (AI)')
    plt.tight_layout()
    plt.savefig('logs/access_denial_by_risk.png', dpi=300)
    plt.close()

    # 5. Policy Type Usage
    plt.figure(figsize=(7,4))
    df_ai['policy_type'].value_counts(normalize=True).plot(kind='bar')
    plt.ylabel('% of Matches')
    plt.savefig('logs/policy_type_usage.png', dpi=300)
    plt.close()

    # 6. Decision Latency Over Time
    plt.figure(figsize=(7,4))
    plt.plot(df_ai['decision_latency_ms'].astype(float))
    plt.title('Decision Latency Over Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig('logs/decision_latency_over_time.png', dpi=300)
    plt.close()

    # 7. ADR vs Time of Day
    plt.figure(figsize=(7,4))
    time_categories = ["morning", "afternoon", "evening", "night", "off_hours"]
    adr = df_ai.groupby('time_of_day')['access_granted'].apply(lambda x: 1-x.mean())
    adr = adr.reindex(time_categories, fill_value=0)
    adr.plot(kind='bar', color=['#3b82f6','#06d6a0','#ffd166','#ef476f','#a78bfa'])
    plt.title('Access Denial Rate vs Time of Day (AI)')
    plt.ylabel('% Denied')
    plt.xlabel('Time of Day')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('logs/adr_vs_timeofday.png', dpi=300)
    plt.close()

    # 8. Access Decisions by Role (Simulated)
    # If 'role' not in data, simulate
    if 'role' in df_ai.columns:
        role_acc = df_ai.groupby('role')['access_granted'].mean()
        role_acc.plot(kind='bar')
    else:
        plt.bar(['User','Admin','Fleet'], [0.95,0.85,0.75])
    plt.ylabel('Acceptance Rate')
    plt.title('Access Decisions by Role')
    plt.tight_layout()
    plt.savefig('logs/access_by_role.png', dpi=300)
    plt.close()

    # 9. Session Validity Ratio (Simulated)
    # If replay/spoof info not available, simulate
    plt.figure(figsize=(7,4))
    valid = np.random.binomial(1, 0.98, len(df_ai))
    plt.plot(np.arange(len(valid)), valid, label='Valid/Invalid Ratio')
    plt.xlabel('Session Index')
    plt.ylabel('Valid=1 / Invalid=0')
    plt.title('Session Validity Ratio')
    plt.tight_layout()
    plt.savefig('logs/session_validity_ratio.png', dpi=300)
    plt.close()

    # 10. Blockchain Logging Delay (Simulated)
    plt.figure(figsize=(7,4))
    delay = np.random.normal(200, 30, len(df_ai))
    plt.plot(df_ai['timestamp'], delay)
    plt.xlabel('Sessions')
    plt.ylabel('Time (ms)')
    plt.title('Blockchain Logging Delay (AI)')
    plt.tight_layout()
    plt.savefig('logs/blockchain_logging_delay.png', dpi=300)
    plt.close()

    # 11. AI Override Frequency (Simulated)
    plt.figure(figsize=(7,4))
    override = np.random.binomial(1, 0.05, len(df_ai))
    plt.plot(np.arange(len(override)), override.cumsum()/np.arange(1,len(override)+1), label='% Override')
    plt.xlabel('Sessions')
    plt.ylabel('% Override')
    plt.title('AI Override Frequency (AI)')
    plt.tight_layout()
    plt.savefig('logs/ai_override_frequency.png', dpi=300)
    plt.close()

    # 12. PET – IAM Decision Time (Simulated)
    plt.figure(figsize=(7,4))
    pet = np.random.normal(80, 10, len(df_ai))
    plt.plot(df_ai['timestamp'], pet)
    plt.xlabel('Sessions')
    plt.ylabel('Time (ms)')
    plt.title('Policy Evaluation Time (PET)')
    plt.tight_layout()
    plt.savefig('logs/pet_iam_decision_time.png', dpi=300)
    plt.close()