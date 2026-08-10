from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dengue_early_warning_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "visualizations"
)


def load_results():
    """Load early-warning analysis results."""
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_FILE}"
        )

    df = pd.read_csv(RESULTS_FILE)

    required_columns = {
        "country",
        "iso3",
        "cases_for_analysis",
        "case_growth",
        "risk_score",
        "risk_level",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df


def prepare_output_directory():
    """Create the visualization output directory."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def create_risk_distribution(df):
    """Create a chart showing the number of countries by risk level."""
    risk_order = ["HIGH", "MEDIUM", "LOW"]

    counts = (
        df["risk_level"]
        .value_counts()
        .reindex(
            risk_order,
            fill_value=0
        )
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Dengue Early-Warning Risk Distribution"
    )

    ax.set_xlabel(
        "Risk Level"
    )

    ax.set_ylabel(
        "Number of Countries"
    )

    ax.tick_params(
        axis="x",
        rotation=0
    )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR
        / "risk_distribution.png"
    )

    fig.savefig(
        output_file,
        dpi=300
    )

    plt.close(fig)

    return output_file


def create_top_risk_chart(df):
    """Create a chart showing the highest-risk countries."""
    top = (
        df.sort_values(
            ["risk_score", "case_growth"],
            ascending=[False, False]
        )
        .head(10)
        .sort_values("risk_score")
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        top["country"],
        top["risk_score"]
    )

    ax.set_title(
        "Top 10 Dengue Early-Warning Risk Scores"
    )

    ax.set_xlabel(
        "Risk Score"
    )

    ax.set_ylabel(
        "Country"
    )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR
        / "top_risk_countries.png"
    )

    fig.savefig(
        output_file,
        dpi=300
    )

    plt.close(fig)

    return output_file


def create_case_growth_chart(df):
    """Create a chart showing the largest positive case-growth signals."""
    growth = df[
        (df["cases_for_analysis"] > 0)
        & (df["case_growth"] > 0)
    ].copy()

    growth = (
        growth.sort_values(
            "case_growth",
            ascending=False
        )
        .head(10)
        .sort_values("case_growth")
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        growth["country"],
        growth["case_growth"]
    )

    ax.set_title(
        "Top 10 Dengue Case-Growth Signals"
    )

    ax.set_xlabel(
        "Case Growth Ratio"
    )

    ax.set_ylabel(
        "Country"
    )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR
        / "case_growth_signals.png"
    )

    fig.savefig(
        output_file,
        dpi=300
    )

    plt.close(fig)

    return output_file


def create_visualizations():
    """Generate all dengue early-warning visualizations."""
    prepare_output_directory()

    df = load_results()

    risk_distribution = create_risk_distribution(df)

    top_risk = create_top_risk_chart(df)

    case_growth = create_case_growth_chart(df)

    return {
        "risk_distribution": risk_distribution,
        "top_risk_countries": top_risk,
        "case_growth_signals": case_growth,
    }


def main():
    print("=" * 70)
    print("DENGUE EARLY-WARNING VISUALIZATION")
    print("=" * 70)

    print("\nLoading early-warning results...")

    df = load_results()

    print(
        f"Rows loaded: {len(df):,}"
    )

    print(
        f"Countries: {df['country'].nunique():,}"
    )

    print("\nCreating visualizations...")

    outputs = create_visualizations()

    print("\nVisualization files created:")

    for name, path in outputs.items():
        print(
            f"{name}: {path}"
        )

    print("\n" + "=" * 70)
    print("Visualization completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()