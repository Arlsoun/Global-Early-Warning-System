from pathlib import Path

import pandas as pd

from src.dashboard import (
    load_results,
    create_dashboard_chart,
    create_top_risk_table,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DASHBOARD_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dashboard"
)

SUMMARY_FILE = (
    DASHBOARD_DIR
    / "dengue_dashboard_summary.png"
)

TOP_RISK_FILE = (
    DASHBOARD_DIR
    / "top_risk_countries.csv"
)


def test_results_file_exists():
    df = load_results()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_results_have_expected_columns():
    df = load_results()

    expected_columns = {
        "country",
        "iso3",
        "cases_for_analysis",
        "previous_cases",
        "case_growth",
        "rolling_3m",
        "risk_score",
        "risk_level",
    }

    assert expected_columns.issubset(df.columns)


def test_risk_levels_are_valid():
    df = load_results()

    valid_levels = {"HIGH", "MEDIUM", "LOW"}

    assert set(df["risk_level"].dropna()).issubset(
        valid_levels
    )


def test_country_count_is_174():
    df = load_results()

    assert df["country"].nunique() == 174


def test_dashboard_directory_exists():
    DASHBOARD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    assert DASHBOARD_DIR.exists()


def test_dashboard_chart_is_created():
    create_dashboard_chart()

    assert SUMMARY_FILE.exists()
    assert SUMMARY_FILE.stat().st_size > 0


def test_top_risk_table_is_created():
    create_top_risk_table()

    assert TOP_RISK_FILE.exists()
    assert TOP_RISK_FILE.stat().st_size > 0


def test_top_risk_table_has_expected_columns():
    create_top_risk_table()

    df = pd.read_csv(TOP_RISK_FILE)

    expected_columns = {
        "country",
        "iso3",
        "risk_score",
        "risk_level",
    }

    assert expected_columns.issubset(df.columns)


def test_top_risk_table_is_not_empty():
    create_top_risk_table()

    df = pd.read_csv(TOP_RISK_FILE)

    assert len(df) > 0