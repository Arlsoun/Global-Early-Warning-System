# Dengue Dataset Data Dictionary

## Overview

This document describes the fields used in the WHO global dengue dataset for the Global Dengue Early-Warning System.

Dataset coverage:

- Source: World Health Organization (WHO)
- Period: January 2010 to June 2026
- Latest available month: June 2026
- Countries represented: 197
- Latest-month reporting countries: 169
- Total records: 11,841

## Dataset Fields

| Column            | Data Type | Description                                                          |
| ----------------- | --------- | -------------------------------------------------------------------- |
| date              | datetime  | Reporting month represented as the first day of the month.           |
| date_lab          | string    | Human-readable reporting month, such as `Jun 2026`.                  |
| who_region        | string    | WHO regional abbreviation, such as `SEAR` or `WPR`.                  |
| who_region_long   | string    | Full WHO regional name.                                              |
| country           | string    | Country or reporting territory name.                                 |
| iso3              | string    | Three-letter ISO country or territory code.                          |
| cases             | float     | Reported dengue cases for the country and reporting month.           |
| confirmed_cases   | float     | Number of laboratory-confirmed dengue cases when reported.           |
| severe_cases      | float     | Number of reported severe dengue cases when available.               |
| deaths            | float     | Reported dengue-related deaths when available.                       |
| cfr               | float     | Case fatality ratio, representing deaths relative to reported cases. |
| prop_sev          | float     | Proportion of reported cases classified as severe.                   |
| cfr_ci_lower      | float     | Lower confidence interval bound for the case fatality ratio.         |
| cfr_ci_upper      | float     | Upper confidence interval bound for the case fatality ratio.         |
| prop_sev_ci_lower | float     | Lower confidence interval bound for the severe-case proportion.      |
| prop_sev_ci_upper | float     | Upper confidence interval bound for the severe-case proportion.      |

## Missing Data

Several fields contain missing values.

Missing values occur because reporting availability differs across countries and months. In particular, confirmed cases, severe cases, deaths, case fatality ratio, severe-case proportion, and confidence intervals are not available for every record.

The early-warning analysis therefore uses the `cases` field as the primary epidemiological signal.

## Derived Early-Warning Fields

The early-warning system adds the following calculated fields.

| Field          | Description                                                            |
| -------------- | ---------------------------------------------------------------------- |
| previous_cases | Cases reported for the previous available record for the same country. |
| case_growth    | Relative change in cases compared with the previous available record.  |
| rolling_3m     | Three-record rolling average of reported cases for the country.        |
| risk_score     | Numerical score produced by the early-warning scoring function.        |
| risk_level     | Risk category derived from the risk score: HIGH, MEDIUM, or LOW.       |

## Risk Classification

The current system uses the following risk categories:

|       Score | Risk Level |
| ----------: | ---------- |
| 6 or higher | HIGH       |
|      3 to 5 | MEDIUM     |
|      0 to 2 | LOW        |

## Risk Score Components

The score considers three main signals.

### 1. Current Case Count

Higher current case counts receive more points.

|  Current cases | Points |
| -------------: | -----: |
|  5,000 or more |      3 |
| 1,000 to 4,999 |      2 |
|     100 to 999 |      1 |
|      Below 100 |      0 |

### 2. Increase From Previous Month

A stronger increase receives more points.

|          Growth | Points |
| --------------: | -----: |
|    200% or more |      3 |
| 100% to 199.99% |      2 |
|   50% to 99.99% |      1 |
|       Below 50% |      0 |

When previous cases are zero and current cases are greater than zero, the system assigns 2 points.

### 3. Cases Above Three-Month Average

If current cases exceed the country's three-month rolling average, the system assigns 1 additional point.

## Output

The processed early-warning results are saved as:

`data/processed/dengue_early_warning_results.csv`

The raw WHO dataset is excluded from Git tracking through `.gitignore`.

## Data Quality

The original dataset contains:

- 11,841 rows
- 16 columns
- 0 duplicate rows
- 197 countries or reporting territories
- 6 WHO regions

The dataset spans January 2010 through June 2026.
