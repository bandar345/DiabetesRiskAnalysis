"""Task 9: diabetes type among respondents who reported diabetes.

Reads the thin table from Task 3 and writes:
  reports/diabetes_type.csv  (count and weighted percent per DIABTYPE code)
  reports/diabetes_type.md   (short note with the row counts and exclusions)

Run from the project root:
  python src/diabetes_risk/diabetes_type.py
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
THIN_TABLE_PATH = BASE_DIR / "data" / "processed" / "brfss2024_thin.parquet"
CSV_PATH = BASE_DIR / "reports" / "diabetes_type.csv"
NOTE_PATH = BASE_DIR / "reports" / "diabetes_type.md"

WEIGHT_COLUMN = "_LLCPWT"

# DIABETE4 code 1 = "Yes" (told they have diabetes). See reports/contract.md.
DIABETES_YES = 1

# DIABTYPE codes from the 2024 BRFSS codebook (USCODE24_LLCP_082125). Blank means not asked.
# 2024 has no "other type" code.
DIABTYPE_LABELS = {
    1: "Type 1",
    2: "Type 2",
    7: "Don't know/Not Sure",
    9: "Refused",
}


def diabetes_type_table(df):
    """Return (table, counts) for respondents with DIABETE4 == 1 who were asked DIABTYPE.

    table has one row per DIABTYPE code: code, label, count, weighted_count, weighted_percent.
    counts holds the row counts used in the note.
    """
    with_diabetes = df[df["DIABETE4"] == DIABETES_YES]
    asked = with_diabetes[with_diabetes["DIABTYPE"].notna()]

    total_weight = asked[WEIGHT_COLUMN].sum()
    rows = []
    for code, label in DIABTYPE_LABELS.items():
        group = asked[asked["DIABTYPE"] == code]
        weighted_count = group[WEIGHT_COLUMN].sum()
        rows.append({
            "code": code,
            "label": label,
            "count": len(group),
            "weighted_count": round(weighted_count, 1),
            "weighted_percent": round(100 * weighted_count / total_weight, 2) if total_weight else 0.0,
        })
    table = pd.DataFrame(rows)

    counts = {
        "all_interviews": len(df),
        "with_diabetes": len(with_diabetes),
        "asked_type": len(asked),
        "not_asked_type": len(with_diabetes) - len(asked),
        "unexpected_codes": int((~asked["DIABTYPE"].isin(DIABTYPE_LABELS)).sum()),
    }
    return table, counts


def write_note(table, counts, path):
    lines = [
        "# Diabetes type among respondents with diabetes",
        "",
        "Source: CDC BRFSS 2024 combined landline and cell phone file, thin table from Task 3.",
        "",
        "## Who is in the table",
        "",
        f"- Interviews in the thin table: {counts['all_interviews']:,}",
        f"- Reported diabetes (`DIABETE4` = 1): {counts['with_diabetes']:,}",
        f"- Of those, asked the diabetes type question (`DIABTYPE` not blank): {counts['asked_type']:,}",
        f"- Excluded because the diabetes module was not fielded in their state: {counts['not_asked_type']:,}",
        "",
        "Pregnancy-only diabetes, prediabetes, no diabetes, don't know, and refused on `DIABETE4` are not in this table.",
        "",
        "## Result",
        "",
        f"Weighted percents use the survey weight `{WEIGHT_COLUMN}`. They are shares of respondents "
        "with diabetes who were asked the type question, not shares of all interviews.",
        "",
        "| Code | Type | Count | Weighted percent |",
        "| --- | --- | --- | --- |",
    ]
    for row in table.itertuples():
        lines.append(f"| {row.code} | {row.label} | {row.count:,} | {row.weighted_percent:.2f}% |")
    lines += [
        "",
        "Full numbers are in [diabetes_type.csv](diabetes_type.csv). "
        "Counts and weighted percents match the `DIABTYPE` entry in the 2024 codebook (`USCODE24_LLCP_082125`). "
        "The 2024 codebook has no \"other type\" code.",
        "",
        "## Limits",
        "",
        "- Type is self-reported in a phone interview, not a lab result.",
        "- Only states that used the optional diabetes module asked `DIABTYPE`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if not THIN_TABLE_PATH.exists():
        raise FileNotFoundError(
            f"Thin table not found at {THIN_TABLE_PATH}. Run src/diabetes_risk/load.py first."
        )
    df = pd.read_parquet(THIN_TABLE_PATH, columns=["DIABETE4", "DIABTYPE", WEIGHT_COLUMN])
    table, counts = diabetes_type_table(df)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(CSV_PATH, index=False)
    write_note(table, counts, NOTE_PATH)

    print(table.to_string(index=False))
    print(counts)
    if counts["unexpected_codes"]:
        print(f"Warning: {counts['unexpected_codes']} rows have a DIABTYPE code not in the codebook list.")
    print(f"Saved {CSV_PATH} and {NOTE_PATH}")


if __name__ == "__main__":
    main()
