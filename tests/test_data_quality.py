from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "WHO_Dengue_Global_2026_Working.xlsx"
)


def load_data():
    return pd.read_excel(DATA_FILE)


def test_dataset_exists():
    assert DATA_FILE.exists()


def test_dataset_has_expected_columns():
    df = load_data()

    expected_columns = {
        "date",
        "date_lab",
        "who_region",
        "who_region_long",
        "country",
        "iso3",
        "cases",
        "confirmed_cases",
        "severe_cases",
        "deaths",
        "cfr",
        "prop_sev",
        "cfr_ci_lower",
        "cfr_ci_upper",
        "prop_sev_ci_lower",
        "prop_sev_ci_upper",
    }

    assert expected_columns.issubset(df.columns)


def test_dataset_is_not_empty():
    df = load_data()

    assert len(df) > 0


def test_no_duplicate_rows():
    df = load_data()

    assert df.duplicated().sum() == 0


def test_required_identifier_columns_have_no_missing_values():
    df = load_data()

    required_columns = [
        "date",
        "country",
        "iso3",
    ]

    assert df[required_columns].notna().all().all()


def test_cases_are_non_negative():
    df = load_data()

    valid_cases = df["cases"].dropna()

    assert (valid_cases >= 0).all()


def test_dates_are_valid():
    df = load_data()

    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    assert dates.notna().all()


def test_iso3_codes_have_three_characters():
    df = load_data()

    iso3 = df["iso3"].dropna().astype(str)

    assert iso3.str.len().eq(3).all()


def test_country_count_is_reasonable():
    df = load_data()

    country_count = df["country"].nunique()

    assert country_count >= 100


def test_latest_date_is_2026():
    df = load_data()

    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    assert dates.max().year == 2026