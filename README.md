# Global Dengue Early-Warning System

A data-driven early-warning system for identifying countries showing potential increases in reported dengue cases.

The system processes global dengue surveillance data, calculates month-to-month case growth, computes a 3-month rolling average, and assigns a risk score and risk level to countries showing increasing dengue activity.

## Project Status

Current dataset: WHO dengue surveillance data

Latest available month: June 2026

Countries analyzed: 197

Automated tests: 5 passed

## Key Features

- Loads and processes global dengue surveillance data
- Identifies the latest available month for each country
- Calculates previous-month dengue cases
- Calculates case growth
- Calculates 3-month rolling averages
- Generates dengue risk scores
- Classifies countries into HIGH, MEDIUM, and LOW risk levels
- Saves processed early-warning results as CSV
- Includes automated tests using pytest

## Risk Classification

HIGH risk:
Risk score >= 6

MEDIUM risk:
Risk score >= 3

LOW risk:
Risk score < 3

## Example Results

The June 2026 analysis identified:

HIGH risk countries: 2

MEDIUM risk countries: 29

LOW risk countries: 166

Examples of countries with high or medium early-warning signals include:

- Cambodia
- Bangladesh
- United Republic of Tanzania
- Thailand
- India
- Sri Lanka
- Benin
- Ghana
- Côte d'Ivoire

These results represent signals generated from reported surveillance data. They are not medical diagnoses or official outbreak declarations.

## Project Structure

Global-Early-Warning-System/

```
data/
    Local datasets and processed data

docs/
    Project documentation

src/
    data_audit.py
    data_profile.py
    early_warning.py

tests/
    test_early_warning.py

.gitignore
README.md
```

## How It Works

The system follows these main steps:

1. Load the dengue surveillance dataset.
2. Convert dates and case counts into usable formats.
3. Sort observations by country and date.
4. Calculate previous-month cases.
5. Calculate month-to-month case growth.
6. Calculate the 3-month rolling average.
7. Identify the latest observation for each country.
8. Calculate a risk score.
9. Assign a risk level.
10. Save the results as a CSV file.

## Installation

Create and activate a Python virtual environment:

```
python -m venv .venv
```

Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Install the required packages:

```
pip install pandas openpyxl pytest
```

## Running the Early-Warning System

From the project root:

```
python src/early_warning.py
```

The processed results are saved under:

```
data/processed/
```

## Running Tests

Run the complete test suite:

```
python -m pytest tests/test_early_warning.py -v
```

Current test result:

```
5 passed
```

## Data

The project uses dengue surveillance data from the World Health Organization.

The original local dataset is excluded from Git through .gitignore.

This repository therefore contains the analysis code and documentation without distributing the local dataset.

## Technologies

Python

Pandas

OpenPyXL

Pytest

Git

GitHub

## Future Improvements

- Add automated data updates
- Add dengue trend visualizations
- Add country-level dashboards
- Add geographic risk maps
- Add time-series forecasting
- Add anomaly detection
- Add automated GitHub Actions testing
- Improve risk scoring using statistical and machine-learning methods

## Disclaimer

This project is intended for data analysis and early-warning research. Risk classifications are analytical signals based on reported surveillance data and should not be treated as clinical advice or official public-health alerts.
