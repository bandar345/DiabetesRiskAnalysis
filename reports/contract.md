# Analysis contract

This page defines the diabetes risk analysis: the target, the main inputs, the sample, the metric, and the split. It does not fix the model type. Later tasks follow these definitions.

Codes below are from the CDC 2024 BRFSS codebook for the combined landline and cell phone file (`USCODE24_LLCP_082125`), variable `DIABETE4`. Source: [2024 BRFSS codebook (ZIP)](https://www.cdc.gov/brfss/annual_data/2024/zip/codebook24_llcp-v2-508.zip), linked from the [2024 BRFSS survey data page](https://www.cdc.gov/brfss/annual_data/annual_2024.html).

## Target

`DIABETE4` is the interview question "(Ever told) (you had) diabetes?" The model uses three classes. Pregnancy-only diabetes is a different condition and stays out.

| Code | Codebook label | Class |
| --- | --- | --- |
| 1 | Yes | `diabetes` |
| 3 | No | `no_diabetes` |
| 4 | No, pre-diabetes or borderline diabetes | `prediabetes` |

These codes are left out. They are not assigned a class.

| Code | Codebook label | Why it is left out |
| --- | --- | --- |
| 2 | Yes, but female told only during pregnancy | Pregnancy-only |
| 7 | Don't know/Not Sure | Don't know |
| 9 | Refused | Refused |
| BLANK | Not asked or Missing | Blank |

In the 2024 combined file the codebook frequencies are 65,809 (code 1), 3,395 (code 2), 376,125 (code 3), 11,307 (code 4), 798 (code 7), 232 (code 9), and 4 (blank).

## Main model inputs

These are the main inputs. They are not a closed list. Another column from the 2024 codebook can be added here. Non-answer codes are missing, not real values. Record how many rows are missing each main input, and record which rows are used when a model is fit.

| Column | Meaning | Cleaned name |
| --- | --- | --- |
| `_AGE80` | Age | `age` |
| `_BMI5` | BMI | `bmi` |
| `EXERANY2` | Any exercise in the past 30 days | `any_exercise` |
| `_SMOKER3` | Four-level cigarette smoking status | `smoker_status` |
| `USENOW3` | Smokeless tobacco (chewing tobacco, snuff, or snus) | `smokeless_tobacco` |
| `ECIGNOW3` | E-cigarette or other vaping product use | `ecigarette` |
| `_RFDRHV9` | Heavy alcohol consumption | `heavy_drinker` |
| `SEXVAR` | Sex of respondent | `sex` |
| `SSBSUGR2` | Regular soda or pop that contains sugar | `sugar_drinks` |

`_SMOKER3` is the four-level smoking status calculated from `SMOKE100` and `SMOKDAY2`. `_RFSMOK3` is that same status collapsed to current smoker or not.

Heavy drinking (`_RFDRHV9`) means more than 14 drinks per week for men and more than 7 drinks per week for women, using the 2024 calculated-variable definition.

### Smoking status (`_SMOKER3`)

| Code | Codebook label | Use |
| --- | --- | --- |
| 1 | Current smoker, now smokes every day | Keep |
| 2 | Current smoker, now smokes some days | Keep |
| 3 | Former smoker | Keep |
| 4 | Never smoked | Keep |
| 9 | Don't know/Refused/Missing | Missing |

Code 9 covers 32,022 interviews in the 2024 combined file.

### Smokeless tobacco (`USENOW3`)

Core section 11. Question: "Do you currently use chewing tobacco, snuff, or snus every day, some days, or not at all?"

| Code | Codebook label | Use |
| --- | --- | --- |
| 1 | Every day | Keep |
| 2 | Some days | Keep |
| 3 | Not at all | Keep |
| 7 | Don't know/Not Sure | Missing |
| 9 | Refused | Missing |
| BLANK | Not asked or Missing | Missing |

Blank covers 29,641 interviews.

### E-cigarettes (`ECIGNOW3`)

Core section 11. Question: whether the respondent never used e-cigarettes or other electronic vaping products, uses them every day, uses them some days, or used them in the past.

| Code | Codebook label | Use |
| --- | --- | --- |
| 1 | Never used e-cigarettes in your entire life | Keep |
| 2 | Use them every day | Keep |
| 3 | Use them some days | Keep |
| 4 | Used them in the past but do not currently use them at all | Keep |
| 7 | Don't know / Not sure | Missing |
| 9 | Refused | Missing |
| BLANK | Not asked or Missing | Missing |

Blank covers 30,676 interviews.

### Heavy drinking (`_RFDRHV9`)

| Code | Codebook label | Use |
| --- | --- | --- |
| 1 | No | Keep |
| 2 | Yes | Keep |
| 9 | Don't know/Refused/Missing | Missing |

Code 9 covers 46,698 interviews.

### Sex (`SEXVAR`)

| Code | Codebook label | Use |
| --- | --- | --- |
| 1 | Male | Keep |
| 2 | Female | Keep |

In the 2024 combined file these two codes cover all 457,670 interviews.

### Sugar-sweetened soda (`SSBSUGR2`)

Optional module 18. Question: "During the past 30 days, how often did you drink regular soda or pop that contains sugar? Do not include diet soda or diet pop."

The code uses three digits. The first digit is the time unit, and the last two digits are the count. The cleaned column `sugar_drinks` is times per day.

| Code | Codebook label | Cleaned value |
| --- | --- | --- |
| 101–199 | Times per day | Last two digits. Example: 102 is 2 times per day. |
| 201–299 | Times per week | Last two digits divided by 7. Example: 201 is 1/7 time per day. |
| 301–399 | Times per month | Last two digits divided by 30. Example: 330 is 1 time per day. |
| 888 | Never | 0 |
| 777 | Don't know/Not sure | Missing |
| 999 | Refused | Missing |
| BLANK | Not asked or Missing | Missing |

In the full file, 53,299 interviews are never (888) and 342,068 are blank because the module was not asked. The analysis sample below keeps only interviews where the module was asked.

`SSBFRUT3` is the sweetened-fruit-drink question in the same module. It can be added on this page.

### Descriptive columns

Height and weight are descriptive columns. `_BMI5` is the body-size input because CDC already computed it from height and weight.

| Column | Meaning | Use |
| --- | --- | --- |
| `HEIGHT3` | Height | Descriptive-only |
| `WEIGHT2` | Weight | Descriptive-only |

Blood pressure, cholesterol, and sleep are not in the 2024 combined codebook. Heart disease and kidney disease can be consequences of diabetes; if either is used, add its codes on this page.

## Analysis sample

The public file has 457,670 interviews. The modeling table uses 40,000 of them.

Eligible rows have `DIABETE4` code 1, 3, or 4, and `SSBSUGR2` in 101–399 or 888. The 40,000 rows are a sample of those eligible interviews, stratified on the three-class target. The sample size and the seed live in `src/diabetes_risk/config.py`. One draw is saved, and every later task uses that file.

## Metric

The decision metric is macro F1 on the validation split. Report per-class recall beside it. Record accuracy as well. Accuracy is not the selection metric, because most respondents report no diabetes.

## Models

Model type is not fixed. Any classifier may be fit on the train split and scored on the validation split.

The reference model predicts the most common class in the train split. The chosen model is the one with the highest validation macro F1. Write the model name next to that metric.

## Split

Split labeled rows 60% train, 20% validation, and 20% test, stratified on the target. Selection uses the validation split. The test split is scored once for the final write-up.

The seed and the split fractions live in `src/diabetes_risk/config.py` (import name `diabetes_risk.config`).

## What the prediction is

The model predicts interview responses. It is not a diagnosis and it is not a clinical tool.
