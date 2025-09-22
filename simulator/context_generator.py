import random

def generate_legitimate_contexts(user_ids, count):
    legit = []
    roles = ['User', 'Admin', 'Fleet']
    policies = ['RBAC', 'ABAC', 'MAC', 'DAC']
    for _ in range(count):
        user_id = random.choice(user_ids)
        role = random.choices(roles, weights=[0.7, 0.2, 0.1])[0]
        policy_type = random.choices(policies, weights=[0.5, 0.2, 0.2, 0.1])[0]
        session_validity = 'valid' if random.random() > 0.02 else random.choice(['spoof', 'replay'])
        # Weighted random for time_of_day (most legitimate sessions during day, few at night/off_hours)
        times = ["morning", "afternoon", "evening", "night", "off_hours"]
        time_weights = [0.3, 0.3, 0.2, 0.1, 0.1]
        time_of_day = random.choices(times, weights=time_weights)[0]
        legit.append({
            "user_id": user_id,
            "action": random.choice(["charge_request", "view_usage", "access_battery"]),
            "device": random.choice(["mobile", "tablet", "dashboard"]),
            "location": random.choice(["london", "manchester", "birmingham"]),
            "time_of_day": time_of_day,
            "behavior_context": "normal",
            "role": role,
            "policy_type": policy_type,
            "session_validity": session_validity
        })
    return legit
