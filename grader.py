def compute_score(total_reward, max_possible):
    if max_possible == 0:
        return 0.01
    score = total_reward / max_possible
    return max(0.01, min(0.99, float(score)))