# Data Dictionary: BRFSS 2024 Diabetes Risk Analysis

This document outlines the column specifications for the thin dataset extracted from the 2024 Behavioral Risk Factor Surveillance System (BRFSS) public-use data. It defines column meanings, valid value domains, missingness and refusal codes, and their respective modeling roles.

---

| Column Name | Meaning & Description | Valid Values | Missing / Refused / Blank Codes | Model Role |
| :--- | :--- | :--- | :--- | :--- |
| **`DIABETE4`** | (Ever told) you had diabetes? Core question on diagnosed diabetes status. | `1` = Yes<br>`2` = Yes, female only during pregnancy<br>`3` = No<br>`4` = Pre-diabetes / borderline diabetes | `7` = Don’t know / Not sure<br>`9` = Refused<br>`BLANK` = Not asked or Missing | **Target Variable** (Mapped to `diabetes`, `no_diabetes`, `prediabetes`. Codes 2, 7, 9, BLANK excluded). |
| **`_AGE80`** | Imputed age value collapsed for respondents aged 80 and older. | `18` to `80` (where `80` represents age $\ge$ 80). | `BLANK` / System Missing | **Model Feature** (Continuous integer input). |
| **`_BMI5`** | Computed Body Mass Index (BMI). Calculated from reported height and weight. | `1200` to `9999` (Integer with 2 implied decimals). | `BLANK` = Don't know / Refused / Missing height or weight | **Model Feature** (Continuous numerical input, scaled by dividing by 100). |
| **`EXERANY2`** | Exercise or physical activity during past 30 days other than regular job. | `1` = Yes<br>`2` = No | `7` = Don’t know / Not sure<br>`9` = Refused<br>`BLANK` = Not asked or Missing | **Model Feature** (Binary indicator: `1` $\rightarrow$ 1, `2` $\rightarrow$ 0, others $\rightarrow$ `NaN`). |
| **`DIABTYPE`** | Type of diabetes (Type 1, Type 2, or Other). | `1` = Type 1 diabetes<br>`2` = Type 2 diabetes<br>`3` = Other type | `7` = Don’t know / Not sure<br>`9` = Refused<br>`BLANK` = Not asked or Missing | **Descriptive Only** (Used in Task 9. Excluded from model features). |
| **`HEIGHT3`** | Reported height in feet/inches or metric. | `200`–`711` (Feet & inches: `0` / `feet` / `inches`)<br>`9061`–`9998` (Metric meters/cm; leading 9) | `7777` = Don’t know / Not sure<br>`9999` = Refused<br>`BLANK` = Not asked or Missing | **Descriptive / Audit Only** (Used to audit `_BMI5`; excluded from model). |
| **`WEIGHT2`** | Reported weight in pounds or kilograms. | `0050`–`0776` (Pounds)<br>`9023`–`9352` (Kilograms; leading 9) | `7777` = Don’t know / Not sure<br>`9999` = Refused<br>`BLANK` = Not asked or Missing | **Descriptive / Audit Only** (Excluded from model to prevent collinearity with BMI). |
| **`_LLCPWT`** | Final survey sampling weight (Landline and cell-phone combined weight). | Positive floating-point values assigned by the CDC. | None (Every interview record receives a calculated weight). | **Descriptive Weighting Only** (Used in descriptive rates in Tasks 8 & 9; unweighted in classifier). |

---

### Detailed Variable Notes & Audit Checks

#### 1. `_BMI5` Scale Confirmation & Worked Example
* **Representation:** In the raw BRFSS dataset, `_BMI5` stores BMI values with **two implied decimal places** (no actual decimal point is present in the integer data).
* **Formula:** $\text{True BMI} = \frac{\text{\_BMI5}}{100}$
* **Worked Example:** A respondent with a recorded raw value of `2750` in `_BMI5` represents an actual BMI of:
  $$\frac{2750}{100} = 27.50\text{ kg/m}^2$$
* **Audit Rule:** Values must be divided by 100 during data preparation in Task 5 before calculating descriptive statistics or model training.

#### 2. `DIABTYPE` Scope Restriction
* **Field Scope:** This question originates from the optional diabetes module. It is **not** fielded nationwide; it is administered only by states that chose to include the module in their 2024 survey.
* **Filter Criteria:** Only asked to individuals who explicitly affirmed having diabetes (`DIABETE4 == 1`). Respondents who reported gestational diabetes, prediabetes, or no diabetes are coded as `BLANK` (Missing).

#### 3. Weight Variable Confirmation
* The survey weight confirmed in the 2024 Codebook Report is **`_LLCPWT`**. This represents the dual-frame (landline + cell phone) post-stratification sampling weight.
