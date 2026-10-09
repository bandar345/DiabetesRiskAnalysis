# Diabetes type among respondents with diabetes

Source: CDC BRFSS 2024 combined landline and cell phone file, thin table from Task 3.

## Who is in the table

- Interviews in the thin table: 457,670
- Reported diabetes (`DIABETE4` = 1): 65,809
- Of those, asked the diabetes type question (`DIABTYPE` not blank): 13,818
- Excluded because the diabetes module was not fielded in their state: 51,991

Pregnancy-only diabetes, prediabetes, no diabetes, don't know, and refused on `DIABETE4` are not in this table.

## Result

Weighted percents use the survey weight `_LLCPWT`. They are shares of respondents with diabetes who were asked the type question, not shares of all interviews.

| Code | Type | Count | Weighted percent |
| --- | --- | --- | --- |
| 1 | Type 1 | 1,236 | 9.90% |
| 2 | Type 2 | 11,301 | 80.10% |
| 7 | Don't know/Not Sure | 1,243 | 9.70% |
| 9 | Refused | 38 | 0.31% |

Full numbers are in [diabetes_type.csv](diabetes_type.csv). Counts and weighted percents match the `DIABTYPE` entry in the 2024 codebook (`USCODE24_LLCP_082125`). The 2024 codebook has no "other type" code.

## Limits

- Type is self-reported in a phone interview, not a lab result.
- Only states that used the optional diabetes module asked `DIABTYPE`.
