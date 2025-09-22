import random

def generate_attack_contexts(user_prefix, count):
    attacks = []
    roles = ['User', 'Admin', 'Fleet']
    policies = ['RBAC', 'ABAC', 'MAC', 'DAC']
    times = ["morning", "afternoon", "evening", "night", "off_hours"]
    attacks_per_slot = count // 5
    remainder = count % 5
    slot_counts = [attacks_per_slot + (1 if i < remainder else 0) for i in range(5)]
    idx = 0
    for slot, n in enumerate(slot_counts):
        for _ in range(n):
            attack_type = random.choice(['spoof', 'replay', 'geo', 'escalation', 'odd_hour'])
            role = random.choices(roles, weights=[0.5, 0.3, 0.2])[0] if attack_type == 'escalation' else 'User'
            policy_type = random.choices(policies, weights=[0.4, 0.2, 0.2, 0.2])[0]
            session_validity = attack_type
            time_of_day = times[slot]
            attacks.append({
                "user_id": f"{user_prefix}_attacker_{idx}",
                "action": random.choice(["charge_request", "override_control", "alter_billing"]),
                "device": random.choice(["spoofed_device", "unknown_device"]),
                "location": random.choice(["unknown", "foreign"]),
                "time_of_day": time_of_day,
                "behavior_context": "anomalous",
                "role": role,
                "policy_type": policy_type,
                "session_validity": session_validity
            })
            idx += 1

    return attacks