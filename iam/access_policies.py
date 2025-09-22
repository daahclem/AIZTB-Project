# iam/access_policies.py

def check_access_policy(policy_type, role, resource, attributes):
    """
    Dummy logic to simulate policy evaluation for RBAC, ABAC, MAC, DAC.
    Returns "allow" or "deny" based on simple rules.
    """
    if policy_type == "RBAC":
        return "allow" if resource in role.get("resources", []) else "deny"
    
    elif policy_type == "ABAC":
        required_attrs = role.get("attributes", {})
        return "allow" if all(attributes.get(k) == v for k, v in required_attrs.items()) else "deny"
    
    elif policy_type == "MAC":
        return "allow" if resource in role.get("resources", []) else "deny"
    
    elif policy_type == "DAC":
        owner = role.get("owner")
        shared = role.get("shared_with", [])
        if attributes.get("user") == owner or attributes.get("user") in shared:
            return "allow"
        return "deny"
    
    return "deny"
