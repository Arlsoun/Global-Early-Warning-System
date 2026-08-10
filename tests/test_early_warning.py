from src.early_warning import calculate_risk_score
from src.early_warning import risk_level


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


def test_zero_cases():
    score = calculate_risk_score(
        cases=0,
        previous_cases=0,
        rolling_3m=0
    )

    assert score == 0


def test_no_case_growth():
    score = calculate_risk_score(
        cases=100,
        previous_cases=100,
        rolling_3m=100
    )

    assert score == 1


def test_cases_below_previous_month():
    score = calculate_risk_score(
        cases=100,
        previous_cases=200,
        rolling_3m=150
    )

    assert score == 1


def test_high_risk_level():
    assert risk_level(6) == "HIGH"


def test_medium_risk_level():
    assert risk_level(3) == "MEDIUM"


def test_low_risk_level():
    assert risk_level(2) == "LOW"


def test_high_risk_boundary():
    assert risk_level(7) == "HIGH"


def test_medium_risk_boundary():
    assert risk_level(5) == "MEDIUM"


def test_low_risk_boundary():
    assert risk_level(0) == "LOW"


def test_score_with_cases_above_rolling_average():
    score = calculate_risk_score(
        cases=1000,
        previous_cases=1000,
        rolling_3m=500
    )

    assert score == 3


def test_new_cases_after_zero_previous():
    score = calculate_risk_score(
        cases=100,
        previous_cases=0,
        rolling_3m=50
    )

    assert score == 4