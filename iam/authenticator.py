from iam.role_profiles import get_user_policies
from iam.conflict_resolver import resolve_conflict
from iam.access_policies import check_access_policy

def authenticate_user(context):
    user = context.get("user_id")
    resource = context.get("action")
    attributes = context
    policies = get_user_policies(user)
    decisions = {}
    for p in policies:
        decisions[p['type']] = check_access_policy(p['type'], p, resource, attributes)
    return resolve_conflict(decisions)