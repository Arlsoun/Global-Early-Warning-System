from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent


RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dengue_early_warning_results.csv"
)


DASHBOARD_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dashboard"
)


DASHBOARD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_results():
    return pd.read_csv(RESULTS_FILE)


def create_risk_summary(df):
    summary = (
        df["risk_level"]
        .value_counts()
        .reindex(
            ["HIGH", "MEDIUM", "LOW"],
            fill_value=0
        )
    )

    return summary


def create_dashboard_summary(df=None):
    if df is None:
        df = load_results()

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    latest_date = df["date"].max()

    risk_summary = create_risk_summary(df)

    summary = {
        "latest_date": latest_date,
        "countries_analyzed": df["country"].nunique(),
        "high_risk": int(risk_summary["HIGH"]),
        "medium_risk": int(risk_summary["MEDIUM"]),
        "low_risk": int(risk_summary["LOW"]),
    }

    return summary


def create_top_risk_table(df=None):
    if df is None:
        df = load_results()

    columns = [
        "country",
        "iso3",
        "cases_for_analysis",
        "previous_cases",
        "case_growth",
        "rolling_3m",
        "risk_score",
        "risk_level",
    ]

    available_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    table = df[available_columns].copy()

    table = table.sort_values(
        ["risk_score", "case_growth"],
        ascending=[False, False]
    )

    return table.head(20)


def create_dashboard_chart(df=None):
    if df is None:
        df = load_results()

    summary = create_risk_summary(df)

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 10)
    )

    # ========================================================
    # RISK DISTRIBUTION
    # ========================================================

    axes[0, 0].bar(
        summary.index,
        summary.values
    )

    axes[0, 0].set_title(
        "Dengue Risk Distribution"
    )

    axes[0, 0].set_ylabel(
        "Number of Countries"
    )

    # ========================================================
    # TOP RISK COUNTRIES
    # ========================================================

    top = (
        df.sort_values(
            "risk_score",
            ascending=False
        )
        .head(10)
    )

    axes[0, 1].barh(
        top["country"].iloc[::-1],
        top["risk_score"].iloc[::-1]
    )

    axes[0, 1].set_title(
        "Top 10 Risk Countries"
    )

    axes[0, 1].set_xlabel(
        "Risk Score"
    )

    # ========================================================
    # CASE GROWTH
    # ========================================================

    growth = (
        df[
            (df["cases_for_analysis"] > 0)
            & (df["case_growth"] > 0)
        ]
        .sort_values(
            "case_growth",
            ascending=False
        )
        .head(10)
    )

    axes[1, 0].barh(
        growth["country"].iloc[::-1],
        growth["case_growth"].iloc[::-1]
    )

    axes[1, 0].set_title(
        "Top Case-Growth Signals"
    )

    axes[1, 0].set_xlabel(
        "Case Growth"
    )

    # ========================================================
    # RISK SCORE DISTRIBUTION
    # ========================================================

    axes[1, 1].hist(
        df["risk_score"].dropna(),
        bins=range(
            int(df["risk_score"].min()),
            int(df["risk_score"].max()) + 2
        )
    )

    axes[1, 1].set_title(
        "Risk Score Distribution"
    )

    axes[1, 1].set_xlabel(
        "Risk Score"
    )

    axes[1, 1].set_ylabel(
        "Countries"
    )

    fig.suptitle(
        "GLOBAL DENGUE EARLY-WARNING SYSTEM",
        fontsize=16
    )

    fig.tight_layout()

    output_file = (
        DASHBOARD_DIR
        / "dengue_dashboard_summary.png"
    )

    fig.savefig(
        output_file,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    return output_file


def save_dashboard_table(df=None):
    if df is None:
        df = load_results()

    table = create_top_risk_table(df)

    output_file = (
        DASHBOARD_DIR
        / "top_risk_countries.csv"
    )

    table.to_csv(
        output_file,
        index=False
    )

    return output_file


def main():

    print("=" * 70)
    print("GLOBAL DENGUE EARLY-WARNING DASHBOARD")
    print("=" * 70)

    print("\nLoading early-warning results...")

    df = load_results()

    print(
        f"Countries in results: "
        f"{df['country'].nunique():,}"
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = create_dashboard_summary(df)

    print("\n" + "=" * 70)
    print("DASHBOARD SUMMARY")
    print("=" * 70)

    print(
        f"\nLatest available month: "
        f"{summary['latest_date'].strftime('%B %Y')}"
    )

    print(
        f"Countries analyzed: "
        f"{summary['countries_analyzed']:,}"
    )

    print(
        f"HIGH risk countries: "
        f"{summary['high_risk']}"
    )

    print(
        f"MEDIUM risk countries: "
        f"{summary['medium_risk']}"
    )

    print(
        f"LOW risk countries: "
        f"{summary['low_risk']}"
    )

    # ========================================================
    # CREATE DASHBOARD CHART
    # ========================================================

    print("\nCreating dashboard chart...")

    dashboard_chart = create_dashboard_chart(df)

    print(
        "\nDashboard chart created:"
    )

    print(dashboard_chart)

    # ========================================================
    # SAVE TOP RISK TABLE
    # ========================================================

    print("\nSaving top-risk country table...")

    table_file = save_dashboard_table(df)

    print(
        "\nTop-risk table created:"
    )

    print(table_file)

    print("\n" + "=" * 70)
    print("Dashboard generation completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()