import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "WHO_Dengue_Global_2026_Working.xlsx"

print("Loading WHO dengue dataset...")
print(f"File: {DATA_FILE}")

# Load Excel file
df = pd.read_excel(DATA_FILE)

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

print("\nColumns:")
for column in df.columns:
    print(f" - {column}")

print("\n" + "=" * 60)
print("FIRST 5 RECORDS")
print("=" * 60)

print(df.head().to_string())

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if len(missing) == 0:
    print("No missing values found.")
else:
    for column, count in missing.items():
        percentage = count / len(df) * 100
        print(f"{column}: {count:,} ({percentage:.1f}%)")

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates:,}")

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print(df.dtypes)

print("\nAudit completed.")