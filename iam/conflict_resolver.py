def resolve_conflict(policies):
    """
    Resolves conflicts between multiple applicable policies.
    Uses majority vote (grant > deny), and returns the type of the first granting policy based on priority.
    """
    priority = ["MAC", "RBAC", "ABAC", "DAC"]
    grant_policies = [p for p in policies if p.get("decision") is True]

    if len(grant_policies) > len(policies) / 2:
        for level in priority:
            for policy in grant_policies:
                if policy["type"] == level:
                    return {"decision": True, "type": level}

    return {"decision": False, "type": "None"}
