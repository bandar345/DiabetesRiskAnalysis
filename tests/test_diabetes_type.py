import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from diabetes_risk.diabetes_type import diabetes_type_table


def make_rows():
    # DIABETE4, DIABTYPE, weight
    return pd.DataFrame(
        [
            (1, 1, 100.0),   # diabetes, type 1
            (1, 2, 300.0),   # diabetes, type 2
            (1, 2, 500.0),   # diabetes, type 2
            (1, 9, 100.0),   # diabetes, refused type
            (1, None, 50.0),  # diabetes, module not asked
            (2, None, 70.0),  # pregnancy only
            (3, None, 900.0),  # no diabetes
            (4, None, 400.0),  # prediabetes
        ],
        columns=["DIABETE4", "DIABTYPE", "_LLCPWT"],
    )


def test_counts_only_people_with_diabetes_who_were_asked():
    table, counts = diabetes_type_table(make_rows())
    assert counts["with_diabetes"] == 5
    assert counts["asked_type"] == 4
    assert counts["not_asked_type"] == 1
    assert table["count"].sum() == 4


def test_weighted_percent_uses_weights():
    table, _ = diabetes_type_table(make_rows())
    by_code = table.set_index("code")["weighted_percent"]
    # asked weights: 100 + 300 + 500 + 100 = 1000
    assert by_code[1] == 10.0
    assert by_code[2] == 80.0
    assert by_code[9] == 10.0
    assert by_code[7] == 0.0
    assert round(table["weighted_percent"].sum(), 2) == 100.0
