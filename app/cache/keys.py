from datetime import date


def idem_key(txn_id, user_id, merchant_id):
    """Generate idempotency key."""
    return f"idem:{txn_id}:{user_id}:{merchant_id}"


def persona_key(user_id):
    """Generate persona cache key."""
    return f"persona:{user_id}"


def last_reward_key(user_id):
    """Generate last reward cache key."""
    return f"last_reward:{user_id}"


def cac_key(user_id):
    """Generate daily CAC tracking key."""
    today = date.today().isoformat()
    return f"cac:{user_id}:{today}"
