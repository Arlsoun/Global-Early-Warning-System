from pathlib import Path

from src.visualization import (
    RESULTS_FILE,
    OUTPUT_DIR,
    load_results,
    create_risk_distribution,
    create_top_risk_chart,
    create_case_growth_chart,
)


def test_results_file_exists():
    assert RESULTS_FILE.exists()


def test_load_results_returns_data():
    df = load_results()

    assert df is not None
    assert len(df) > 0


def test_required_visualization_columns_exist():
    df = load_results()

    required_columns = {
        "country",
        "iso3",
        "cases_for_analysis",
        "case_growth",
        "risk_score",
        "risk_level",
    }

    assert required_columns.issubset(df.columns)


def test_risk_levels_are_valid():
    df = load_results()

    valid_levels = {
        "HIGH",
        "MEDIUM",
        "LOW",
    }

    assert set(df["risk_level"].dropna()).issubset(
        valid_levels
    )


def test_output_directory_exists_after_creation():
    df = load_results()

    create_risk_distribution(df)

    assert OUTPUT_DIR.exists()


def test_risk_distribution_chart_is_created():
    df = load_results()

    output_file = create_risk_distribution(df)

    assert output_file.exists()
    assert output_file.suffix == ".png"


def test_top_risk_chart_is_created():
    df = load_results()

    output_file = create_top_risk_chart(df)

    assert output_file.exists()
    assert output_file.suffix == ".png"


def test_case_growth_chart_is_created():
    df = load_results()

    output_file = create_case_growth_chart(df)

    assert output_file.exists()
    assert output_file.suffix == ".png"


def test_visualization_files_are_non_empty():
    expected_files = [
        OUTPUT_DIR / "risk_distribution.png",
        OUTPUT_DIR / "top_risk_countries.png",
        OUTPUT_DIR / "case_growth_signals.png",
    ]

    for file_path in expected_files:
        assert file_path.exists()
        assert file_path.stat().st_size > 0