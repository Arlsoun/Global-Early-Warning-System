import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "WHO_Dengue_Global_2026_Working.xlsx"
)


# ============================================================
# RISK SCORE FUNCTION
# ============================================================

def calculate_risk_score(cases, previous_cases, rolling_3m):
    score = 0

    cases = float(cases)
    previous_cases = float(previous_cases)
    rolling_3m = float(rolling_3m)

    # Current case count
    if cases >= 5000:
        score += 3
    elif cases >= 1000:
        score += 2
    elif cases >= 100:
        score += 1

    # Increase from previous month
    if previous_cases > 0:
        growth = (cases - previous_cases) / previous_cases

        if growth >= 2:
            score += 3
        elif growth >= 1:
            score += 2
        elif growth >= 0.5:
            score += 1

    elif cases > 0:
        score += 2

    # Current cases above 3-month average
    if rolling_3m > 0 and cases > rolling_3m:
        score += 1

    return int(score)


# ============================================================
# RISK LEVEL FUNCTION
# ============================================================

def risk_level(score):
    score = int(score)

    if score >= 6:
        return "HIGH"

    if score >= 3:
        return "MEDIUM"

    return "LOW"


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():

    print("=" * 70)
    print("GLOBAL DENGUE EARLY-WARNING SYSTEM")
    print("=" * 70)

    print("\nLoading WHO dengue dataset...")
    print(f"File: {DATA_FILE}")

    df = pd.read_excel(DATA_FILE)

    print(f"Rows loaded: {len(df):,}")

    # ========================================================
    # PREPARE DATA
    # ========================================================

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["cases"] = pd.to_numeric(
        df["cases"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date", "country", "iso3"]
    )

    df = df.sort_values(
        ["country", "date"]
    )

    # ========================================================
    # PREVIOUS MONTH CASES
    # ========================================================

    df["previous_cases"] = (
        df.groupby("country")["cases"]
        .shift(1)
    )

    # ========================================================
    # CASE GROWTH
    # ========================================================

    previous = df["previous_cases"].fillna(0)

    df["case_growth"] = (
        (df["cases"] - previous)
        / previous.replace(0, 1)
    )

    # ========================================================
    # 3-MONTH ROLLING AVERAGE
    # ========================================================

    df["rolling_3m"] = (
        df.groupby("country")["cases"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1
            ).mean()
        )
    )

    # ========================================================
    # LATEST MONTH FOR EACH COUNTRY
    # ========================================================

    latest = (
        df.sort_values("date")
        .groupby("country", as_index=False)
        .tail(1)
        .copy()
    )

    # ========================================================
    # RISK SCORE
    # ========================================================

    latest["risk_score"] = latest.apply(
        lambda row: calculate_risk_score(
            cases=row["cases"],
            previous_cases=row["previous_cases"],
            rolling_3m=row["rolling_3m"]
        ),
        axis=1
    )

    # ========================================================
    # RISK LEVEL
    # ========================================================

    latest["risk_level"] = (
        latest["risk_score"]
        .apply(risk_level)
    )

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    latest_date = latest["date"].max()

    print("\n" + "=" * 70)
    print("LATEST DENGUE EARLY-WARNING SIGNALS")
    print("=" * 70)

    print(
        f"\nLatest available month: "
        f"{latest_date.strftime('%B %Y')}"
    )

    print(
        f"Countries analyzed: "
        f"{latest['country'].nunique():,}"
    )

    # ========================================================
    # FIND INCREASING SIGNALS
    # ========================================================

    signals = latest[
        (latest["cases"] > 0)
        & (latest["case_growth"] > 0)
    ].copy()

    signals = signals.sort_values(
        ["risk_score", "case_growth"],
        ascending=[False, False]
    )

    print("\nPotential early-warning signals:\n")

    if len(signals) == 0:

        print(
            "No increasing dengue signals detected."
        )

    else:

        display_columns = [
            "country",
            "iso3",
            "cases",
            "previous_cases",
            "case_growth",
            "rolling_3m",
            "risk_score",
            "risk_level"
        ]

        result = (
            signals[display_columns]
            .head(20)
            .copy()
        )

        result["cases"] = (
            result["cases"]
            .round(0)
        )

        result["previous_cases"] = (
            result["previous_cases"]
            .fillna(0)
            .round(0)
        )

        result["case_growth"] = (
            result["case_growth"]
            .replace(
                [float("inf"), -float("inf")],
                0
            )
            .round(2)
        )

        result["rolling_3m"] = (
            result["rolling_3m"]
            .round(2)
        )

        print(
            result.to_string(index=False)
        )

    # ========================================================
    # RISK SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("RISK SUMMARY")
    print("=" * 70)

    risk_summary = (
        latest["risk_level"]
        .value_counts()
        .reindex(
            ["HIGH", "MEDIUM", "LOW"],
            fill_value=0
        )
    )

    print(
        f"\nHIGH risk countries:   "
        f"{risk_summary['HIGH']}"
    )

    print(
        f"MEDIUM risk countries: "
        f"{risk_summary['MEDIUM']}"
    )

    print(
        f"LOW risk countries:    "
        f"{risk_summary['LOW']}"
    )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    OUTPUT_DIR = (
        PROJECT_ROOT
        / "data"
        / "processed"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_FILE = (
        OUTPUT_DIR
        / "dengue_early_warning_results.csv"
    )

    latest.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nResults saved to:")
    print(OUTPUT_FILE)

    print("\n" + "=" * 70)
    print("Analysis completed.")
    print("=" * 70)


# ============================================================
# RUN ONLY WHEN EXECUTED DIRECTLY
# ============================================================

if __name__ == "__main__":
    main()