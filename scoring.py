def calculate_points(
    predicted_home: int,
    predicted_away: int,
    actual_home: int,
    actual_away: int,
) -> int:
    """
    3 — exact score
    2 — correct goal difference
    1 — correct outcome (win/draw/loss)
    0 — wrong
    """
    if predicted_home == actual_home and predicted_away == actual_away:
        return 3

    predicted_diff = predicted_home - predicted_away
    actual_diff = actual_home - actual_away
    if predicted_diff == actual_diff:
        return 2

    predicted_outcome = _outcome(predicted_home, predicted_away)
    actual_outcome = _outcome(actual_home, actual_away)
    if predicted_outcome == actual_outcome:
        return 1

    return 0


def _outcome(home: int, away: int) -> str:
    if home > away:
        return "home"
    if home < away:
        return "away"
    return "draw"
