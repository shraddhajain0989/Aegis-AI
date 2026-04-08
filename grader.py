def compute_score(total_reward, max_possible):
    if max_possible == 0:
        return 0.0
    score = total_reward / max_possible
    return max(0.0, min(1.0, float(score)))