# Data Dictionary — BRFSS 2024 Thin Table

This document details every column extracted into `data/processed/brfss2024_thin.parquet` from the CDC BRFSS 2024 survey, defining valid responses, missing/refusal codes, and model usage eligibility.

---

## 1. Column Specifications Table

| Column Name | Description / Meaning | Valid Range / Values | Missing / Refused Codes | Model Input? |
| :--- | :--- | :--- | :--- | :--- |
| **`row_id`** | Unique sequential integer assigned per extracted interview row | 1 to 40,000 | None | No (Identifier only) |
| **`DIABETE4`** | Diabetes status (Ever told had diabetes) | 1 (Yes), 2 (Yes, but female told only during pregnancy), 3 (No), 4 (No, prediabetes or borderline) | 7 (Don't know/Not Sure), 9 (Refused), Blank/NaN | Target source only (maps to 3-class target) |
| **`DIABTYPE`** | Diabetes type (Type 1 or Type 2) | 1 (Type 1), 2 (Type 2) | 7 (Don't know), 9 (Refused), Blank/NaN | No (Descriptive analysis only) |
| **`_AGE80`** | Imputed age in years | 18 to 80 (values 80 and above are capped at 80) | None (fully imputed in BRFSS) | **Yes** (Model Feature) |
| **`HEIGHT3`** | Reported height (mixed metric and imperial encoding) | Feet/inches (e.g., 500-711) or metric (9000-9998: cm) | 7777 (Don't know), 9999 (Refused), Blank/NaN | No (Descriptive / audit only) |
| **`WEIGHT2`** | Reported weight (mixed metric and imperial encoding) | Pounds (0050-0999) or kilograms (9000-9998) | 7777 (Don't know), 9999 (Refused), Blank/NaN | No (Descriptive / audit only) |
| **`_BMI5`** | Computed Body Mass Index (BMI) | Real values approx. 12.00 to 99.99 (stored with 2 implied decimal places) | Blank/NaN (raw values >= 9999 or missing in survey) | **Yes** (Model Feature) |
| **`EXERANY2`** | Exercise in past 30 days (other than regular job) | 1 (Yes), 2 (No) | 7 (Don't know/Not Sure), 9 (Refused), Blank/NaN | **Yes** (Model Feature) |
| **`_SMOKER3`** | Four-level smoker status | 1 (Current daily), 2 (Current some days), 3 (Former), 4 (Never) | 9 (Don't know/Refused/Missing), Blank/NaN | No (Contract limited to Age, BMI, Exercise) |
| **`USENOW3`** | Smokeless tobacco use | 1 (Every day), 2 (Some days), 3 (Not at all) | 7 (Don't know/Not Sure), 9 (Refused), Blank/NaN | No (Contract limited to Age, BMI, Exercise) |
| **`ECIGNOW3`** | E-cigarette or vaping device usage | 1 (Every day), 2 (Some days), 3 (Not at all) | 7 (Don't know/Not Sure), 9 (Refused), Blank/NaN | No (Contract limited to Age, BMI, Exercise) |
| **`_RFDRHV9`** | Heavy alcohol consumption calculated variable | 1 (No: <=14 drinks/wk men, <=7 women), 2 (Yes: >14 drinks/wk men, >7 women) | 9 (Don't know/Refused/Missing), Blank/NaN | No (Contract limited to Age, BMI, Exercise) |
| **`SEXVAR`** | Sex of respondent | 1 (Male), 2 (Female) | None / Refused recorded in raw questions | No (Descriptive / stratification) |
| **`SSBSUGR2`** | Sugar-sweetened beverages consumption frequency | Categorical frequency (drinks per day/week/month) | 777 (Don't know), 999 (Refused), Blank/NaN | No (Descriptive only) |
| **`_LLCPWT`** | Final survey sample weight variable | Positive float values (sampling weight for population representation) | None | No (Used for weighted statistics & descriptive charts) |

---

## 2. Scale Confirmation for `_BMI5`
- **CDC Definition:** The variable `_BMI5` contains the calculated Body Mass Index with **two implied decimal places** (the decimal point is omitted in the raw numeric integer).
- **Transformation Formula:**
  $$\text{BMI} = \frac{\_BMI5}{100}$$
- **Worked Example:**
  - A raw table value of `2845` represents a true BMI of:
    $$\frac{2845}{100} = 28.45 \text{ kg/m}^2$$
  - A raw value of `3500` corresponds to:
    $$\frac{3500}{100} = 35.00 \text{ kg/m}^2$$

---

## 3. Important Contextual Notes

- **`DIABTYPE` (Diabetes Module Fielding):**
  The question `DIABTYPE` ("Was this type 1 or type 2 diabetes?") was not asked to all respondents nationwide. It was included as an optional module and asked **only in states and territories that chose to field the diabetes module**, and strictly among individuals who answered `DIABETE4 == 1`. Non-participating states leave this column empty (`NaN`).

- **Survey Weight Variable (`_LLCPWT`):**
  Confirmed with the BRFSS 2024 codebook: `_LLCPWT` is the official final weight variable assigned to landline and cellular combined survey respondents. It must be utilized for descriptive aggregations (Task 8 & Task 9) to ensure representativeness, but excluded as an input feature for the predictive model.
