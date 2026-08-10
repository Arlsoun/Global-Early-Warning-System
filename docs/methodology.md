\# Dengue Early-Warning Methodology



\## 1. Purpose



The Global Dengue Early-Warning System analyzes reported dengue cases and identifies countries showing potential increases in dengue activity.



The system uses historical monthly case data to calculate indicators of recent transmission activity and assigns an early-warning risk score to each country.



The system is designed as an analytical early-warning tool. Risk classifications represent signals from the available data and are not clinical diagnoses or official outbreak declarations.



\## 2. Data Source



The system uses a WHO global dengue dataset.



The dataset contains monthly dengue reporting information for countries and territories across multiple WHO regions.



The current dataset contains 11,841 records and covers January 2010 through June 2026.



The latest available reporting month is June 2026.



\## 3. Data Preparation



Before analysis, the system performs the following steps:



1\. Loads the WHO dengue Excel dataset.

2\. Converts the date field into a datetime format.

3\. Converts dengue case counts into numeric values.

4\. Removes records without a valid date, country, or ISO3 code.

5\. Sorts records by country and date.

6\. Calculates previous reported cases for each country.

7\. Calculates case growth.

8\. Calculates a three-month rolling average.

9\. Selects the latest available record for each country.



\## 4. Previous Cases



For each country, the system obtains the previous available case count.



This value is used to measure the change in dengue cases between consecutive reporting periods.



The field is stored as:



`previous\_cases`



\## 5. Case Growth



Case growth measures the relative change between the current and previous case counts.



The calculation is:



```text

case\_growth = (current\_cases - previous\_cases) / previous\_cases

```



For example, if a country reports 2,000 cases after previously reporting 1,000 cases:



```text

case\_growth = (2000 - 1000) / 1000

&#x20;           = 1.0

```



This represents a 100% increase.



When the previous case count is zero, the system avoids division by zero and treats the current positive case count as a new signal.



\## 6. Three-Month Rolling Average



The system calculates a three-month rolling average for each country.



The rolling average helps compare the latest case count with recent historical activity.



The calculation uses the available observations within a three-record window.



The resulting field is:



`rolling\_3m`



A country receives an additional risk point when its current cases exceed its three-month rolling average.



\## 7. Risk Score



The risk score combines three indicators:



1\. Current dengue case volume.

2\. Increase compared with the previous reporting period.

3\. Current cases compared with the three-month rolling average.



The maximum score is 7.



\## 8. Current Case Volume Score



Countries receive points according to the latest reported case count.



|  Current Cases | Points |

| -------------: | -----: |

|  5,000 or more |      3 |

| 1,000 to 4,999 |      2 |

|     100 to 999 |      1 |

|      Below 100 |      0 |



This component gives greater weight to countries with larger reported dengue burdens.



\## 9. Case Growth Score



Countries receive additional points according to the increase from the previous reporting period.



|          Growth | Points |

| --------------: | -----: |

|    200% or more |      3 |

| 100% to 199.99% |      2 |

|   50% to 99.99% |      1 |

|       Below 50% |      0 |



When previous cases are zero and current cases are greater than zero, the system assigns 2 points.



\## 10. Rolling Average Score



If current cases are greater than the three-month rolling average, the system adds:



```text

+1 point

```



Otherwise:



```text

+0 points

```



\## 11. Risk Classification



The final risk score is converted into three categories.



|  Risk Score | Risk Level |

| ----------: | ---------- |

| 6 or higher | HIGH       |

|      3 to 5 | MEDIUM     |

|      0 to 2 | LOW        |



The classification is applied independently to each country.



\## 12. Early-Warning Signal Selection



The system identifies countries with:



```text

cases > 0

```



and:



```text

case\_growth > 0

```



These countries are treated as potential early-warning signals because their latest reported case count increased compared with the previous available observation.



Signals are ordered by:



1\. Risk score, descending.

2\. Case growth, descending.



The system displays the top 20 signals.



\## 13. Example



Suppose a country reports:



```text

Current cases:       8,095

Previous cases:      2,595

Three-month average: 4,347

```



Current case volume contributes:



```text

3 points

```



Case growth is approximately:



```text

2.12

```



This corresponds to an increase of more than 200%, contributing:



```text

3 points

```



Current cases are also above the three-month average:



```text

1 point

```



Total:



```text

3 + 3 + 1 = 7

```



The resulting risk level is:



```text

HIGH

```



\## 14. Output



The system produces a processed CSV file containing the latest country-level results.



Output location:



```text

data/processed/dengue\_early\_warning\_results.csv

```



The output contains both original epidemiological fields and calculated early-warning fields.



\## 15. Interpretation



A HIGH risk classification indicates a strong statistical signal based on the scoring rules.



A MEDIUM classification indicates a moderate signal.



A LOW classification indicates a weaker signal.



The classification should be interpreted together with reporting completeness, surveillance quality, seasonality, population size, testing practices, and other epidemiological information.



The system does not establish causality and does not independently confirm dengue outbreaks.



\## 16. Limitations



The system has several limitations.



\### Reporting Differences



Countries differ in surveillance systems, reporting frequency, testing capacity, and completeness.



\### Reporting Delays



Recent months may contain incomplete or delayed reports.



\### Seasonality



Dengue transmission varies seasonally. A rise in cases may therefore reflect expected seasonal patterns.



\### Population Differences



Raw case counts do not account for population size.



A country with a large population will generally report more cases than a smaller country even when incidence rates are lower.



\### No Incidence Rate



The current model uses reported case counts rather than cases per population.



\### No Climate Variables



The current scoring system does not directly incorporate rainfall, temperature, humidity, mosquito density, or other environmental variables.



\### No Spatial Transmission Model



The current system evaluates countries independently and does not model transmission between neighboring countries.



\## 17. Future Improvements



Future versions of the system may include:



\* Population-adjusted incidence rates.

\* Seasonal baseline models.

\* Anomaly detection.

\* Climate and weather variables.

\* Geographic transmission patterns.

\* Time-series forecasting.

\* Machine-learning models.

\* Automated WHO data updates.

\* Interactive dashboards.

\* Confidence and uncertainty indicators.

\* Country-specific alert thresholds.



\## 18. Reproducibility



The analysis is implemented in Python.



Core dependencies are listed in:



```text

requirements.txt

```



The main analysis module is:



```text

src/early\_warning.py

```



Automated tests are located in:



```text

tests/test\_early\_warning.py

```



Run the tests with:



```powershell

python -m pytest tests/test\_early\_warning.py -v

```



A successful test run should report:



```text

5 passed

```



