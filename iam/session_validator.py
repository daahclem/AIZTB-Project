# session_validator.py - Checks Zero Trust context (time, location)

def validate_context(context):
    """
    Validates context parameters such as time, location, device type.
    Returns True if valid, False otherwise.
    """
    valid_hours = range(6, 23)  # Only allow daytime charging
    current_hour = context.get("hour", 12)
    location = context.get("location", "").lower()
    trusted_locations = {"uk", "eu", "us"}

    if current_hour not in valid_hours:
        return False
    if location not in trusted_locations:
        return False

    return True
