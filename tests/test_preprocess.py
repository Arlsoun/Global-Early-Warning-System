from src.preprocess import prepare_analysis_data


def test_preprocessing_returns_dataframe():
    df = prepare_analysis_data()

    assert df is not None


def test_preprocessed_data_is_not_empty():
    df = prepare_analysis_data()

    assert len(df) > 0


def test_cases_for_analysis_column_exists():
    df = prepare_analysis_data()

    assert "cases_for_analysis" in df.columns


def test_negative_cases_are_removed_from_analysis():
    df = prepare_analysis_data()

    valid_cases = df["cases_for_analysis"].dropna()

    assert (valid_cases >= 0).all()


def test_valid_case_values_are_preserved():
    df = prepare_analysis_data()

    valid_cases = df["cases_for_analysis"].dropna()

    assert (valid_cases > 0).any()


def test_required_columns_exist():
    df = prepare_analysis_data()

    required_columns = [
        "date",
        "country",
        "iso3",
        "cases",
        "cases_for_analysis",
    ]

    assert all(
        column in df.columns
        for column in required_columns
    )


def test_dates_are_valid():
    df = prepare_analysis_data()

    assert df["date"].notna().all()


def test_country_identifiers_are_available():
    df = prepare_analysis_data()

    assert df["country"].notna().all()
    assert df["iso3"].notna().all()


def test_latest_date_is_june_2026():
    df = prepare_analysis_data()

    latest_date = df["date"].max()

    assert latest_date.year == 2026
    assert latest_date.month == 6


def test_usable_case_records_are_10369():
    df = prepare_analysis_data()

    usable_cases = df["cases_for_analysis"].notna().sum()

    assert usable_cases == 10369