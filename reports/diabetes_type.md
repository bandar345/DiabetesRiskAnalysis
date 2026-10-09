# Diabetes type among respondents with diabetes

Source: CDC BRFSS 2024 combined landline and cell phone file, thin table from Task 3 (`data/processed/brfss2024_thin.parquet`).

## Who is in the table

The thin table is the 40,000-interview modeling sample defined in `reports/contract.md`: interviews with `DIABETE4` in {1, 3, 4} and a real sugary-soda answer (`SSBSUGR2`). Sugary soda and diabetes type are both optional modules, so this table only covers respondents from states that asked both.

- Interviews in the thin table: 40,000
- Reported diabetes (`DIABETE4` = 1): 5,638
- Of those, asked the diabetes type question (`DIABTYPE` not blank): 496
- Excluded because the diabetes module was not fielded in their state: 5,142

Pregnancy-only diabetes, prediabetes, no diabetes, don't know, and refused on `DIABETE4` are not in this table.

## Result

Weighted percents use the survey weight `_LLCPWT`. They are shares of respondents with diabetes who were asked the type question, not shares of all interviews.

| Code | Type | Count | Weighted percent |
| --- | --- | --- | --- |
| 1 | Type 1 | 37 | 7.00% |
| 2 | Type 2 | 418 | 84.00% |
| 7 | Don't know/Not Sure | 40 | 8.91% |
| 9 | Refused | 1 | 0.09% |

Full numbers are in [diabetes_type.csv](diabetes_type.csv). The 2024 codebook has no "other type" code.

## Comparison with the full public file

The 2024 codebook (`USCODE24_LLCP_082125`) reports `DIABTYPE` over all 457,670 interviews. Use it to judge how far the sample result can be trusted.

| Code | Type | Sample count | Sample weighted percent | Codebook count | Codebook weighted percent |
| --- | --- | --- | --- | --- | --- |
| 1 | Type 1 | 37 | 7.00% | 1,236 | 9.90% |
| 2 | Type 2 | 418 | 84.00% | 11,301 | 80.10% |
| 7 | Don't know/Not Sure | 40 | 8.91% | 1,243 | 9.70% |
| 9 | Refused | 1 | 0.09% | 38 | 0.31% |

## Limits

- Type is self-reported in a phone interview, not a lab result.
- Only states that used the optional diabetes module asked `DIABTYPE`.
- The sample has few respondents per type, so its percents move more than the full-file percents. Type 1 is the smallest group.
- Weighted percents describe respondents in the sample who were asked the type question. They are not U.S. population rates.
