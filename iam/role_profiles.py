# iam/role_profiles.py

import json
import os

def load_profiles():
    file_path = os.path.join(os.path.dirname(__file__), 'role_profiles.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def get_user_policies(user_id):
    profiles = load_profiles()
    return profiles.get(user_id, [])

# ✅ Add this function to fix the error
def get_user_role(user_id):
    """
    Returns a merged role object with all policy types for the user.
    Used for hybrid IAM evaluation.
    """
    policies = get_user_policies(user_id)
    role = {"RBAC": None, "ABAC": None, "MAC": None, "DAC": None}
    for p in policies:
        role[p["type"]] = p
    return role
