import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "WHO_Dengue_Global_2026_Working.xlsx"

df = pd.read_excel(DATA_FILE)

print("=" * 60)
print("GLOBAL DENGUE DATA PROFILE")
print("=" * 60)

print(f"\nDate range:")
print(f"Start: {df['date'].min()}")
print(f"End:   {df['date'].max()}")

print(f"\nCountries: {df['country'].nunique()}")
print(f"Countries: {', '.join(sorted(df['country'].dropna().unique()))}")

print(f"\nWHO regions: {df['who_region'].nunique()}")
print(df['who_region_long'].value_counts().to_string())

print("\n" + "=" * 60)
print("TOTAL CASES BY COUNTRY")
print("=" * 60)

country_cases = (
    df.groupby("country")["cases"]
    .sum()
    .sort_values(ascending=False)
)

print(country_cases.head(20).to_string())

print("\n" + "=" * 60)
print("TOTAL DEATHS BY COUNTRY")
print("=" * 60)

country_deaths = (
    df.groupby("country")["deaths"]
    .sum()
    .sort_values(ascending=False)
)

print(country_deaths.head(20).to_string())

print("\n" + "=" * 60)
print("MONTHLY GLOBAL CASES")
print("=" * 60)

monthly_cases = (
    df.groupby("date")["cases"]
    .sum()
    .sort_index()
)

print(monthly_cases.tail(24).to_string())

print("\n" + "=" * 60)
print("LATEST AVAILABLE DATA")
print("=" * 60)

latest_date = df["date"].max()
latest = df[df["date"] == latest_date]

print(f"Latest date: {latest_date}")
print(f"Countries reporting: {latest['country'].nunique()}")
print(f"Total cases: {latest['cases'].sum():,.0f}")
print(f"Total deaths: {latest['deaths'].sum():,.0f}")

print("\nData profiling completed.")