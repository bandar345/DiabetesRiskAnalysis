# Diabetes risk analysis

## 1. Question

How do age, height, weight, BMI, and physical activity relate to self-reported diabetes status (no diabetes, prediabetes, or diabetes), and what type of diabetes do people with diabetes report?

## 2. Data

| Item | Detail |
| --- | --- |
| Source | U.S. Centers for Disease Control and Prevention, Behavioral Risk Factor Surveillance System (BRFSS), combined landline and cell phone public-use file |
| Link | https://www.cdc.gov/brfss/annual_data/annual_2024.html |
| Time period | Interviews collected in 2024. Some states finished interviews in early 2025. CDC released the public file in August 2025. |
| Coverage | 49 states, the District of Columbia, Guam, Puerto Rico, and the U.S. Virgin Islands. |
| Rows | 457,670 interviews |
| Columns | 345 variables in the SAS transport file |

The diabetes status question is `DIABETE4` (yes, only during pregnancy, no, or prediabetes/borderline). Diabetes type is `DIABTYPE` and was asked only in states that used the diabetes module. Age, height, weight, BMI, and activity are in the same file (`_AGE80`, `HEIGHT3`, `WEIGHT2`, `_BMI5`, `EXERANY2`). The file does not ask whether a relative has diabetes.

The data are a U.S. government work in the public domain. Cite CDC when the results are shared.

## 3. Team members

- Abdulaziz -/owAziz

## 4. Status

Dataset selected. the analysis has not started.
