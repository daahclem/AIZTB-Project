import random

def generate_attack_contexts(user_prefix, count):
    attacks = []
    for i in range(count):
        attacks.append({
            "user_id": f"{user_prefix}_attacker_{i}",
            "action": random.choice(["charge_request", "override_control", "alter_billing"]),
            "device": random.choice(["spoofed_device", "unknown_device"]),
            "location": random.choice(["unknown", "foreign"]),
            "time_of_day": random.choice(["night", "off_hours"]),
            "behavior_context": "anomalous"
        })
    return attacks