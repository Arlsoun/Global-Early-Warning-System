from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dengue_early_warning_results.csv"
)

MAP_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "visualizations"
    / "global_dengue_risk_map.png"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global Dengue Early-Warning System",
    page_icon="🌍",
    layout="wide",
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_results():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Required results file was not found: {RESULTS_FILE}"
        )

    df = pd.read_csv(RESULTS_FILE)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

    return df


df = load_results()


# ============================================================
# TITLE
# ============================================================

st.title("🌍 Global Dengue Early-Warning System")

st.caption(
    "WHO dengue surveillance data analysis and early-warning risk assessment"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

risk_options = [
    "HIGH",
    "MEDIUM",
    "LOW",
]

selected_risk = st.sidebar.multiselect(
    "Risk level",
    options=risk_options,
    default=risk_options,
)

country_search = st.sidebar.text_input(
    "Search country",
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["risk_level"].isin(selected_risk)
].copy()

if country_search:
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(
            country_search,
            case=False,
            na=False,
        )
    ]


# ============================================================
# GLOBAL SUMMARY
# ============================================================

latest_date = df["date"].max()

high_risk = int(
    (df["risk_level"] == "HIGH").sum()
)

medium_risk = int(
    (df["risk_level"] == "MEDIUM").sum()
)

low_risk = int(
    (df["risk_level"] == "LOW").sum()
)

total_countries = df["country"].nunique()


st.subheader("Global Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if pd.isna(latest_date):
        latest_date_display = "N/A"
    else:
        latest_date_display = latest_date.strftime("%B %Y")

    st.metric(
        "Latest Month",
        latest_date_display,
    )

with col2:
    st.metric(
        "Countries",
        f"{total_countries:,}",
    )

with col3:
    st.metric(
        "HIGH Risk",
        high_risk,
    )

with col4:
    st.metric(
        "MEDIUM Risk",
        medium_risk,
    )

with col5:
    st.metric(
        "LOW Risk",
        low_risk,
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader("Risk Distribution")

risk_summary = pd.DataFrame(
    {
        "Risk Level": [
            "HIGH",
            "MEDIUM",
            "LOW",
        ],
        "Countries": [
            high_risk,
            medium_risk,
            low_risk,
        ],
    }
)

st.bar_chart(
    risk_summary.set_index("Risk Level")
)


# ============================================================
# GLOBAL RISK MAP
# ============================================================

st.subheader("Global Dengue Risk Map")

if MAP_FILE.exists():

    map_col1, map_col2, map_col3 = st.columns(
        [1, 4, 1]
    )

    with map_col2:
        st.image(
            str(MAP_FILE),
            width="stretch",
        )

else:

    st.warning(
        "Global dengue risk map is not available."
    )


# ============================================================
# HIGHEST-RISK COUNTRIES
# ============================================================

st.subheader("Highest-Risk Countries")

top_risk = (
    df.sort_values(
        ["risk_score", "case_growth"],
        ascending=[False, False],
    )
    [
        [
            "country",
            "iso3",
            "cases_for_analysis",
            "previous_cases",
            "case_growth",
            "rolling_3m",
            "risk_score",
            "risk_level",
        ]
    ]
    .head(10)
    .copy()
)

top_risk["case_growth"] = top_risk[
    "case_growth"
].round(2)

top_risk["rolling_3m"] = top_risk[
    "rolling_3m"
].round(2)

st.dataframe(
    top_risk,
    width="stretch",
    hide_index=True,
)


# ============================================================
# CASE-GROWTH SIGNALS
# ============================================================

st.subheader("Strongest Case-Growth Signals")

growth_signals = (
    df[
        (df["cases_for_analysis"] > 0)
        & (df["case_growth"] > 0)
    ]
    .sort_values(
        "case_growth",
        ascending=False,
    )
    [
        [
            "country",
            "iso3",
            "cases_for_analysis",
            "previous_cases",
            "case_growth",
            "risk_score",
            "risk_level",
        ]
    ]
    .head(10)
    .copy()
)

growth_signals["case_growth"] = growth_signals[
    "case_growth"
].round(2)

st.dataframe(
    growth_signals,
    width="stretch",
    hide_index=True,
)


# ============================================================
# COUNTRY RISK DETAILS
# ============================================================

st.subheader("Country Risk Details")

if len(filtered_df) == 0:

    st.info(
        "No countries match the selected filters."
    )

else:

    selected_country = st.selectbox(
        "Select a country",
        sorted(
            filtered_df["country"].unique()
        ),
    )

    country_data = filtered_df[
        filtered_df["country"] == selected_country
    ].iloc[0]

    detail_col1, detail_col2, detail_col3, detail_col4 = (
        st.columns(4)
    )

    with detail_col1:
        st.metric(
            "Risk Level",
            country_data["risk_level"],
        )

    with detail_col2:
        st.metric(
            "Risk Score",
            int(country_data["risk_score"]),
        )

    with detail_col3:
        st.metric(
            "Current Cases",
            f"{country_data['cases_for_analysis']:,.0f}",
        )

    with detail_col4:

        previous_cases = country_data["previous_cases"]

        if pd.isna(previous_cases):
            previous_cases_display = "N/A"
        else:
            previous_cases_display = (
                f"{previous_cases:,.0f}"
            )

        st.metric(
            "Previous Cases",
            previous_cases_display,
        )

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write(
            f"Case growth: "
            f"{country_data['case_growth']:.2f}"
        )

    with detail_col2:
        st.write(
            f"3-month rolling average: "
            f"{country_data['rolling_3m']:.2f}"
        )


# ============================================================
# FILTERED DATA
# ============================================================

st.subheader("Filtered Countries")

filtered_columns = [
    "country",
    "iso3",
    "cases_for_analysis",
    "previous_cases",
    "case_growth",
    "rolling_3m",
    "risk_score",
    "risk_level",
]

filtered_table = (
    filtered_df[filtered_columns]
    .sort_values(
        ["risk_score", "case_growth"],
        ascending=[False, False],
    )
    .copy()
)

filtered_table["case_growth"] = filtered_table[
    "case_growth"
].round(2)

filtered_table["rolling_3m"] = filtered_table[
    "rolling_3m"
].round(2)

st.dataframe(
    filtered_table,
    width="stretch",
    hide_index=True,
)


# ============================================================
# DOWNLOAD RESULTS
# ============================================================

st.subheader("Download Results")

download_col1, download_col2 = st.columns(2)

with download_col1:

    full_csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Full Risk Results",
        data=full_csv,
        file_name="dengue_early_warning_results.csv",
        mime="text/csv",
    )


with download_col2:

    filtered_csv = filtered_table.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Results",
        data=filtered_csv,
        file_name="dengue_filtered_results.csv",
        mime="text/csv",
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

if pd.isna(latest_date):
    footer_date = "N/A"
else:
    footer_date = latest_date.strftime("%B %Y")

st.caption(
    "Global Dengue Early-Warning System | "
    "WHO dengue surveillance data | "
    f"Latest data: {footer_date}"
)