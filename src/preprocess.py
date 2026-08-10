from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "WHO_Dengue_Global_2026_Working.xlsx"
)


def load_raw_data():
    """Load the raw WHO dengue dataset."""
    return pd.read_excel(DATA_FILE)


def clean_data(df):
    """Clean and standardize the dengue dataset."""

    df = df.copy()

    # Standardize dates
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Standardize numeric columns
    numeric_columns = [
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
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Remove rows without essential identifiers
    df = df.dropna(
        subset=[
            "date",
            "country",
            "iso3",
        ]
    )

    # Negative case values represent reporting corrections.
    # Keep them in the raw dataset, but exclude them from
    # outbreak-risk calculations.
    df["cases_for_analysis"] = df["cases"].where(
        df["cases"] >= 0
    )

    # Sort chronologically by country
    df = df.sort_values(
        ["country", "date"]
    ).reset_index(drop=True)

    return df


def prepare_analysis_data():
    """Load and prepare dengue data for analysis."""

    df = load_raw_data()

    df = clean_data(df)

    return df


if __name__ == "__main__":
    df = prepare_analysis_data()

    print("=" * 70)
    print("DENGUE DATA PREPROCESSING")
    print("=" * 70)

    print(f"Rows loaded: {len(df):,}")
    print(
        f"Countries: {df['country'].nunique():,}"
    )

    print(
        f"Negative case records: "
        f"{(df['cases'] < 0).sum():,}"
    )

    print(
        f"Usable case records: "
        f"{df['cases_for_analysis'].notna().sum():,}"
    )

    print(
        f"Latest date: "
        f"{df['date'].max().strftime('%B %Y')}"
    )

    print("=" * 70)