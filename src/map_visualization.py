from pathlib import Path

import geopandas as gpd
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

WORLD_GEOJSON_URL = (
    "https://naturalearth.s3.amazonaws.com/"
    "110m_cultural/ne_110m_admin_0_countries.zip"
)


def load_results():
    """Load dengue early-warning results."""
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_FILE}"
        )

    return pd.read_csv(RESULTS_FILE)


def load_world_map():
    """Load world country boundaries."""
    return gpd.read_file(WORLD_GEOJSON_URL)


def create_risk_map():
    """Create a world map showing dengue risk levels."""
    df = load_results()
    world = load_world_map()

    merged = world.merge(
        df,
        left_on="ISO_A3",
        right_on="iso3",
        how="left"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    fig, ax = plt.subplots(
        figsize=(16, 9)
    )

    risk_colors = {
        "HIGH": "red",
        "MEDIUM": "orange",
        "LOW": "green",
    }

    for risk_level, color in risk_colors.items():
        subset = merged[
            merged["risk_level"] == risk_level
        ]

        if not subset.empty:
            subset.plot(
                ax=ax,
                color=color,
                edgecolor="black",
                linewidth=0.3,
                label=risk_level,
            )

    no_data = merged[
        merged["risk_level"].isna()
    ]

    if not no_data.empty:
        no_data.plot(
            ax=ax,
            color="lightgray",
            edgecolor="black",
            linewidth=0.2,
            label="NO DATA",
        )

    ax.set_title(
        "Global Dengue Early-Warning Risk Map",
        fontsize=16,
    )

    ax.set_axis_off()

    ax.legend(
        title="Risk Level",
        loc="lower left",
    )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR
        / "global_dengue_risk_map.png"
    )

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    return output_file


def main():
    print("=" * 70)
    print("GLOBAL DENGUE RISK MAP")
    print("=" * 70)

    print("\nLoading early-warning results...")

    df = load_results()

    print(
        f"Countries in results: "
        f"{df['country'].nunique():,}"
    )

    print("\nLoading world map...")

    output_file = create_risk_map()

    print("\nMap created:")
    print(output_file)

    print("\n" + "=" * 70)
    print("Map visualization completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()