def dummy_risk_score(context):
    score = 0.1
    if context['behavior_context'] == 'anomalous':
        score += 0.3
    if 'spoofed' in context['device'] or 'unknown' in context['device']:
        score += 0.2
    if context['time_of_day'] in ['night', 'off_hours']:
        score += 0.2
    if context['user_id'].startswith('evuser_attacker'):
        score += 0.2
    return min(score, 1.0)