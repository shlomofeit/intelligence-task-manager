def risk_calculator(difficulty: int, importance: int):

    risk = difficulty * 2 + importance

    if risk >= 25:
        result = "CRITICAL"
    elif risk >= 18:
        result = "HIGH"
    elif risk >= 10:
        result = "MEDIUM"
    else:
        result = "LOW"

    return result