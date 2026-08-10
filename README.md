# Global Dengue Early-Warning System

A data-driven early-warning system for identifying countries showing potential increases in reported dengue cases.

The system processes global dengue surveillance data, calculates month-to-month case growth, computes a 3-month rolling average, assigns risk scores, and classifies countries into HIGH, MEDIUM, and LOW risk levels.

## Project Status

Current dataset: WHO dengue surveillance data

Latest available month: June 2026

Countries analyzed: 174

HIGH risk countries: 2

MEDIUM risk countries: 29

LOW risk countries: 143

Automated tests: 61 passed

## Key Features

- Loads and processes global dengue surveillance data
- Identifies the latest available month for each country
- Calculates previous-month dengue cases
- Calculates month-to-month case growth
- Calculates 3-month rolling averages
- Generates dengue risk scores
- Classifies countries into HIGH, MEDIUM, and LOW risk levels
- Generates a global dengue risk map
- Generates dengue risk distribution visualizations
- Identifies countries with the strongest case-growth signals
- Provides an interactive Streamlit dashboard
- Provides country-level risk details
- Allows filtering by risk level and country
- Allows users to download complete or filtered risk results
- Includes automated testing using pytest
- Includes automated GitHub Actions testing

## Risk Classification

HIGH risk: Risk score >= 6

MEDIUM risk: Risk score >= 3

LOW risk: Risk score < 3

## June 2026 Results

The June 2026 analysis identified:

HIGH risk countries: 2

MEDIUM risk countries: 29

LOW risk countries: 143

Countries with high or medium early-warning signals include:

- Cambodia
- Bangladesh
- United Republic of Tanzania
- Thailand
- India
- Sri Lanka
- Benin
- Ghana
- Côte d'Ivoire

These results represent analytical signals generated from reported surveillance data. They are not medical diagnoses or official outbreak declarations.

## Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard provides:

- Global dengue risk summary
- Risk distribution chart
- Global dengue risk map
- Highest-risk countries
- Strongest case-growth signals
- Country risk details
- Risk-level filtering
- Country search
- Filtered country results
- Downloadable CSV results

### Start the Dashboard

From the project root, create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the dashboard:

```powershell
streamlit run app\dashboard_app.py
```

The dashboard will be available at:

http://localhost:8501

## Running the Early-Warning System

From the project root:

```powershell
python src\early_warning.py
```

The processed results are saved under:

```text
data/processed/
```

## Running the Full Test Suite

Run:

```powershell
python -m pytest -v
```

Current result:

```text
61 passed
```

The tests cover:

- Early-warning risk scoring
- Data preprocessing
- Data quality validation
- Map visualization
- Risk visualizations
- Dashboard functionality
- Output file creation
- Data validation

## Continuous Integration

The project uses GitHub Actions to automatically run the test suite when changes are pushed to the main branch or submitted through a pull request.

The workflow installs the project dependencies and runs:

```powershell
python -m pytest -v
```

This helps verify that new changes do not break the existing system.

## Project Structure

```text
Global-Early-Warning-System/

├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   └── dashboard_app.py
│
├── data/
│   └── processed/
│
├── docs/
│   ├── data-dictionary.md
│   ├── methodology.md
│   └── project-definition.txt
│
├── src/
│   ├── data_audit.py
│   ├── data_profile.py
│   ├── early_warning.py
│   ├── map_visualization.py
│   ├── preprocess.py
│   ├── visualization.py
│   └── dashboard.py
│
├── tests/
│   ├── test_dashboard.py
│   ├── test_data_quality.py
│   ├── test_early_warning.py
│   ├── test_map_visualization.py
│   ├── test_preprocess.py
│   └── test_visualization.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## How It Works

The system follows these steps:

1. Load the dengue surveillance dataset.
2. Convert dates and case counts into usable formats.
3. Sort observations by country and date.
4. Calculate previous-month cases.
5. Calculate month-to-month case growth.
6. Calculate the 3-month rolling average.
7. Identify the latest observation for each country.
8. Calculate the risk score.
9. Assign a risk level.
10. Generate visualizations and risk maps.
11. Save processed results as CSV.
12. Display results through the Streamlit dashboard.

## Data

The project uses dengue surveillance data from the World Health Organization.

The original local dataset is excluded from Git through `.gitignore`.

The repository therefore contains the analysis code, tests, documentation, and dashboard without distributing the local source dataset.

## Technologies

- Python
- Pandas
- OpenPyXL
- Matplotlib
- Streamlit
- Pytest
- Git
- GitHub
- GitHub Actions

## Future Improvements

- Automated data updates
- Time-series forecasting
- Anomaly detection
- Improved statistical risk scoring
- Machine-learning-based risk prediction
- Interactive time-series charts
- Country comparison tools
- Historical risk tracking
- Deployment of the Streamlit dashboard

## Disclaimer

This project is intended for data analysis and early-warning research.

Risk classifications are analytical signals based on reported surveillance data. They should not be treated as clinical advice, medical diagnosis, or official public-health alerts.
