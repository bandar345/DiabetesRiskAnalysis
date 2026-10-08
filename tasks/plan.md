# Implementation Plan: Diabetes risk model

## Overview

Build a reproducible classifier that predicts self-reported diabetes status (no diabetes, prediabetes, or diabetes) from age, BMI, and physical activity in the 2024 CDC BRFSS public file. A second, separate summary answers what diabetes type people with diabetes report. Entry-level teammates each own one task at a time. Shared results live in Python modules and saved files. Notebooks are for exploration and error review only.

This is an analysis of survey self-report. It does not diagnose diabetes and it is not a clinical tool.

## How the team organizes the work

Use a small project, not one shared notebook.

| Place | What goes here | Who may edit it |
| --- | --- | --- |
| `src/diabetes_risk/` | Loading, cleaning, the split, training, and evaluation | The owner of the current task, reviewed by one teammate |
| `notebooks/` | Plots, questions, and error review | Only the author of that notebook |
| `data/raw/` | The CDC file, unchanged | Nobody edits it |
| `data/processed/` | The modeling table and the frozen split ids | Produced by a script |
| `reports/` | Tables, figures, and the short results write-up | The owner of the task that creates them |
| `models/` | The saved model and its metrics | Produced by the training command |

Rules that keep a junior team from blocking each other:

1. Agree the contract in Task 2 before anyone fits a model. The contract is the target definition, the columns, and the metric. After that, descriptive work and modeling can proceed on the same table.
2. One task has one owner. A second person reviews the change before the next task depends on it.
3. A notebook cell is a draft. If another person needs that result, move it into `src/diabetes_risk/` or save a file under `data/` or `reports/` the same day.
4. Everyone trains and scores on the split file from Task 6. Nobody draws a new random split inside a notebook.
5. Hand off work as files with column names, not as "run my notebook from the top."
6. Any number of people can work. Whoever is free takes the next task whose dependencies are done. One owner per task.

## Architecture Decisions

- **Target.** Three classes from `DIABETE4`: no diabetes, prediabetes, and diabetes. Interviews coded as diabetes only during pregnancy, don't know, refused, or blank stay out of the model. Pregnancy-only diabetes is a different condition from the three statuses in the project question.
- **Model inputs.** `_AGE80` (age), `_BMI5` (BMI), and `EXERANY2` (any exercise). Height and weight stay in the descriptive analysis. BMI is already computed from height and weight, so putting all three in one model makes the coefficients hard to read.
- **Metric.** Choose the model with macro F1 on the validation split. Report per-class recall beside it. Record accuracy, and do not use it to pick the model: most respondents report no diabetes.
- **Split.** 60% train, 20% validation, 20% test, stratified on the target, one fixed seed. Selection happens on validation. The test set is scored once for the final write-up.
- **Models.** A majority-class baseline, then multinomial logistic regression, then one tree model. Keep the model that wins on validation macro F1. No large tuning search.
- **Survey weights.** Use the interview weight (expect `_LLCPWT`; confirm the name in the codebook) for the descriptive rates in Tasks 8 and 9. The classifier is scored as a predictor of interview records. The write-up says that plainly so nobody treats unweighted accuracy as a U.S. population rate.
- **Stack.** Python, pandas, and scikit-learn. Save the thin table as Parquet. Read the SAS transport file once, keep only the contract columns, and do not reload all 345 columns in later tasks.

## Dependency Graph

```
Task 1 layout ─────────────┐
                           ├── Task 3 load thin table ── Task 4 dictionary
Task 2 contract ───────────┤                                    │
                           │                                    ├── Task 5 cleaning ── Task 6 split ── Task 10 baseline ── Task 11 comparison
                           │                                    │         │                                    │
                           │                                    │         ├── Task 7 quality                    ├── Task 12 error review
                           │                                    │         └── Task 8 relationships               └── Task 13 train command
                           └────────────────────────────────────┴── Task 9 diabetes type                              │
                                                                                                                       └── Task 14 results page
```

Tasks 8 and 9 can run at the same time as Task 10 once cleaning exists. Task 9 can start as soon as the thin table and dictionary exist.

## Task List

### Phase 1: Foundation

- [ ] Task 1: Create the project layout
- [ ] Task 2: Write the analysis contract

### Checkpoint: Foundation

- [ ] The team has read the contract and agrees on the target, the exclusions, the three model inputs, and macro F1
- [ ] Folders exist and raw data is listed in `.gitignore`

### Phase 2: Shared table

- [ ] Task 3: Load BRFSS into a thin Parquet table
- [ ] Task 4: Write the column dictionary
- [ ] Task 5: Implement cleaning as importable functions
- [ ] Task 6: Freeze the train, validation, and test ids

### Checkpoint: Shared table

- [ ] One command rebuilds the modeling table from `data/raw`
- [ ] The same split file is the only split the team uses
- [ ] Cleaning special codes are covered by tests

### Phase 3: Answer the question descriptively

- [ ] Task 7: Data-quality notebook and saved summary
- [ ] Task 8: Relationship charts for age, body size, and activity
- [ ] Task 9: Diabetes-type table for respondents with diabetes

### Checkpoint: Descriptive answer

- [ ] Charts and the type table are files under `reports/`, not only notebook output
- [ ] Weighted rates say which weight column was used

### Phase 4: Model

- [ ] Task 10: Majority baseline and logistic regression
- [ ] Task 11: One tree model and a comparison table
- [ ] Task 12: Error-analysis notebook on saved predictions
- [ ] Task 13: Single training command for the chosen model

### Checkpoint: Model

- [ ] The chosen model beats the majority baseline on validation macro F1
- [ ] `python -m diabetes_risk.train` rewrites the model file and `reports/metrics.json`
- [ ] Test-set metrics are computed once and match the write-up

### Phase 5: Close

- [ ] Task 14: Results page with limitations

### Checkpoint: Complete

- [ ] A new teammate can run the training command from the README and get the same metrics
- [ ] The page states self-report, exclusions, the unused test set rule, and that this is not a diagnosis

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The SAS file has 345 columns and 457,670 rows | High | Task 3 keeps only contract columns and writes Parquet |
| BRFSS uses 7, 9, 777, 999, and blank as non-answers | High | Dictionary plus tested cleaning functions; notebooks do not reimplement this |
| `HEIGHT3` and `WEIGHT2` mix feet/inches and meters in one field | High | Model uses CDC's `_BMI5`. Raw height and weight are an audit, not model inputs |
| `_BMI5` is often stored with implied decimals | Med | Dictionary confirms the scale; a test checks a known value |
| `DIABTYPE` is missing outside the diabetes module | Med | Task 9 restricts to respondents who were asked and reports how many that is |
| Class imbalance makes accuracy look strong | Med | Macro F1 and per-class recall are the decision metrics |
| Unweighted metrics get described as U.S. rates | Med | Weights are for descriptive tables only; the results page says so |
| Two people edit one notebook | Med | Notebooks stay personal; shared logic moves to `src/` |
| Gestational diabetes is folded into "yes" | Med | Contract excludes code for pregnancy-only diabetes |

## Open Questions

- Confirm in the 2024 codebook: `DIABETE4` and `DIABTYPE` code lists, the `_BMI5` scale, and the weight variable name.
- Should pregnancy-only diabetes stay excluded, as this plan recommends?

## Assumptions

1. The finished product is a classical classifier plus a short written answer, not a web app.
2. The label is self-reported `DIABETE4`, not a lab result.
3. The team is entry-level, so the model set stays at a majority baseline, logistic regression, and one tree model.
4. There is no calendar. Order follows the dependencies above. Tasks 8 and 9 can proceed beside modeling after Task 5.
