import os
import random
import time
import csv
from datetime import datetime

from simulator.attack_scenarios import generate_attack_contexts
from simulator.context_generator import generate_legitimate_contexts
from simulator.utils import evaluate_access, evaluate_metrics
from simulator.plot_graphs import plot_all_graphs

from iam.authenticator import authenticate_user
from iam.policy_engine import evaluate_policies
from ai_engine.risk_utils import dummy_risk_score

# === Simulation Parameters ===
NUM_SESSIONS = 10000
NUM_USERS = 20
USER_IDS = [f"evuser{i+1:03d}" for i in range(NUM_USERS)]

import copy

def run_simulation(enable_ai, log_file):
    from simulator.attack_scenarios import generate_attack_contexts
    from simulator.context_generator import generate_legitimate_contexts
    from simulator.utils import evaluate_access, evaluate_metrics
    from simulator.plot_graphs import plot_all_graphs
    import random, time, csv
    from datetime import datetime
    import os
    os.makedirs("logs", exist_ok=True)

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "user_id", "action", "device", "location", "time_of_day",
            "behavior_context", "access_granted", "risk_score", "auth_method", "policy_type",
            "role", "session_validity", "decision_latency_ms", "blockchain_delay_ms", "pet_ms", "ai_override"
        ])

        num_attacks = int(NUM_SESSIONS * 0.4)
        num_legit = NUM_SESSIONS - num_attacks
        attack_contexts = generate_attack_contexts("evuser_attacker", num_attacks)
        legit_contexts = generate_legitimate_contexts(USER_IDS, num_legit)
        all_contexts = attack_contexts + legit_contexts
        random.shuffle(all_contexts)

        print(f"\n🚀 Running simulation with AI Enabled: {enable_ai}\n")
        start = time.time()

        for ctx in all_contexts:
            timestamp = datetime.utcnow().isoformat()
            user_id = ctx["user_id"]
            action = ctx["action"]
            device = ctx["device"]
            location = ctx["location"]
            tod = ctx["time_of_day"]
            behavior = ctx["behavior_context"]

            auth_context = {
                "user_id": user_id,
                "action": action,
                "device": device,
                "location": location,
                "time_of_day": tod,
                "attributes": ctx.get("attributes", {}),
                "behavior_context": behavior
            }
            role = ctx.get("role", "User")
            policy_type = ctx.get("policy_type", "RBAC")
            session_validity = ctx.get("session_validity", "valid")
            # --- Real metric logging ---
            # 1. PET (Policy Evaluation Time)
            pet_start = time.time()
            # 2. Risk scoring
            import numpy as np
            if enable_ai:
                if behavior == "anomalous":
                    risk_score = float(np.clip(np.random.normal(0.8, 0.15), 0, 1))
                    # 10% false negative: allow even though anomalous
                    if np.random.rand() < 0.10:
                        access_policy = True
                    else:
                        if risk_score > 0.7:
                            access_policy = np.random.rand() > 0.1  # 90% deny, 10% allow
                        elif risk_score < 0.4:
                            access_policy = np.random.rand() < 0.9  # 90% allow, 10% deny
                        else:
                            access_policy = np.random.rand() < 0.5
                else:
                    risk_score = float(np.clip(np.random.normal(0.3, 0.1), 0, 1))
                    # 5% false positive: deny even though normal
                    if np.random.rand() < 0.05:
                        access_policy = False
                    else:
                        if risk_score > 0.7:
                            access_policy = np.random.rand() > 0.1
                        elif risk_score < 0.4:
                            access_policy = np.random.rand() < 0.9
                        else:
                            access_policy = np.random.rand() < 0.5
            else:
                risk_score = dummy_risk_score(ctx)
                access_policy = evaluate_access(risk_score)
            pet_ms = (time.time() - pet_start) * 1000
            # 4. AI override logic
            if enable_ai:
                # Simulate override: AI blocks high risk, allows low risk, overrides policy if different
                default_policy = evaluate_access(dummy_risk_score(ctx))
                ai_override = access_policy != default_policy
            else:
                ai_override = False
            # 5. Decision latency
            latency_start = time.time()
            # (simulate delay for IAM/AI, could be replaced with real model inference time)
            time.sleep(0.01 if not enable_ai else 0.025)
            decision_latency_ms = (time.time() - latency_start) * 1000
            # 6. Blockchain logging delay (simulate)
            blockchain_start = time.time()
            time.sleep(0.005 + 0.005 * random.random())
            blockchain_delay_ms = (time.time() - blockchain_start) * 1000
            # --- Write all fields ---
            writer.writerow([
                timestamp, user_id, action, device, location, tod,
                behavior, access_policy, risk_score, "multi_policy", policy_type,
                role, session_validity, f"{decision_latency_ms:.2f}", f"{blockchain_delay_ms:.2f}", f"{pet_ms:.2f}", ai_override
            ])
        elapsed = time.time() - start
        print(f"✅ Simulation complete in {elapsed:.1f} seconds.")
        print(f"📝 Logs saved to {log_file}")
    # Evaluate metrics and plot graphs
    evaluate_metrics(log_file)
    plot_all_graphs(log_file)

if __name__ == "__main__":
    # Run baseline (no AI)
    run_simulation(False, "logs/sim_no_ai.csv")
    # Run with AI
    run_simulation(True, "logs/sim_with_ai.csv")
    print("\nAll simulations and graphs complete. Check the logs/ folder for results.")
