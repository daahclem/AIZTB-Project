from iam.role_profiles import get_user_policies
from iam.conflict_resolver import resolve_conflict

def match_abac(policy, context):
    return all(context.get(k) == v for k, v in policy.get("attributes", {}).items())

def match_dac(policy, context):
    user = context.get("user")
    return user in policy.get("shared_with", []) or user == policy.get("owner")

def evaluate_policies(user_id, context, risk_score):
    policies = get_user_policies(user_id)
    applicable = []
    for p in policies:
        if not (p["min_risk"] <= risk_score <= p["max_risk"]):
            continue
        if context["action"] not in p["resources"] and "*" not in p["resources"]:
            continue
        if p["type"] == "ABAC" and not match_abac(p, context):
            continue
        if p["type"] == "DAC" and not match_dac(p, context):
            continue
        applicable.append(p)

    if not applicable:
        return False, None

    final_decision = resolve_conflict(applicable)
    chosen_policy_type = applicable[0]['type']
    return final_decision, chosen_policy_type
