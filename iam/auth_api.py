# auth_api.py - Handles user/device authentication and MFA verification

def verify_credentials(user_id, password):
    # Simulated check against secure store
    return user_id == "evuser" and password == "secure123"

def verify_mfa(token):
    # Simulated MFA token
    return token == "123456"

def authenticate_user(user_id, password, mfa_token):
    if not verify_credentials(user_id, password):
        return False, "Invalid credentials"
    if not verify_mfa(mfa_token):
        return False, "MFA failed"
    return True, "Authentication successful"

