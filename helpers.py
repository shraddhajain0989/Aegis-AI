def is_protective_action(action):
    return action in ["warn", "block"]


def is_safe_action(action):
    return action in ["ignore", "verify", "educate"]