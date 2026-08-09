from src.early_warning import calculate_risk_score


def test_high_risk_score():
    score = calculate_risk_score(
        cases=8095,
        previous_cases=2595,
        rolling_3m=4347
    )
    assert score >= 6


def test_medium_risk_score():
    score = calculate_risk_score(
        cases=3992,
        previous_cases=1782,
        rolling_3m=2478.33
    )
    assert 4 <= score <= 5


def test_low_risk_score():
    score = calculate_risk_score(
        cases=100,
        previous_cases=100,
        rolling_3m=100
    )
    assert score <= 3


def test_zero_previous_cases():
    score = calculate_risk_score(
        cases=25,
        previous_cases=0,
        rolling_3m=9.67
    )
    assert score >= 0


def test_risk_score_is_integer():
    score = calculate_risk_score(
        cases=2907,
        previous_cases=714,
        rolling_3m=1420.33
    )
    assert isinstance(score, int)
