import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from diabetes_risk.config import SAMPLE_SEED, SAMPLE_SIZE
from diabetes_risk.load import draw_sample, is_eligible


def test_config_names_the_sample_size_and_seed():
    assert SAMPLE_SIZE == 40_000
    assert isinstance(SAMPLE_SEED, int)


def test_eligible_keeps_three_classes_with_a_real_soda_answer():
    frame = pd.DataFrame(
        {
            "DIABETE4": [1, 3, 4, 1, 2, 7, 9, 1, 3, 4, 1],
            "SSBSUGR2": [102, 201, 888, 777, 102, 102, 102, 999, None, 100, 399],
        }
    )
    kept = frame.index[is_eligible(frame)].tolist()
    assert kept == [0, 1, 2, 10]


def test_eligible_accepts_sas_float_codes():
    frame = pd.DataFrame({"DIABETE4": [1.0, 3.0], "SSBSUGR2": [888.0, 101.0]})
    assert is_eligible(frame).tolist() == [True, True]


def test_draw_sample_matches_class_shares_and_repeats():
    diabetes = [1] * 30 + [3] * 60 + [4] * 10
    frame = pd.DataFrame(
        {
            "row_id": range(1, 101),
            "DIABETE4": diabetes,
            "SSBSUGR2": [888] * 100,
        }
    )
    first = draw_sample(frame, sample_size=20, seed=2024)
    second = draw_sample(frame, sample_size=20, seed=2024)
    pd.testing.assert_frame_equal(first, second)
    counts = first["DIABETE4"].value_counts().sort_index()
    assert len(first) == 20
    assert counts.to_dict() == {1: 6, 3: 12, 4: 2}
    assert set(first["row_id"]).issubset(set(frame["row_id"]))


def test_draw_sample_uses_largest_remainder_for_class_quotas():
    frame = pd.DataFrame(
        {
            "row_id": range(1, 11),
            "DIABETE4": [1] * 5 + [3] * 3 + [4] * 2,
            "SSBSUGR2": [888] * 10,
        }
    )
    drawn = draw_sample(frame, sample_size=4, seed=7)
    counts = drawn["DIABETE4"].value_counts().sort_index()
    assert counts.to_dict() == {1: 2, 3: 1, 4: 1}


def test_draw_sample_drops_ineligible_rows():
    frame = pd.DataFrame(
        {
            "row_id": [1, 2, 3, 4],
            "DIABETE4": [2, 2, 3, 3],
            "SSBSUGR2": [888, 888, 777, 102],
        }
    )
    drawn = draw_sample(frame, sample_size=1, seed=1)
    assert drawn["row_id"].tolist() == [4]


def test_draw_sample_refuses_a_short_eligible_pool():
    frame = pd.DataFrame({"DIABETE4": [1, 3], "SSBSUGR2": [888, 888]})
    with pytest.raises(ValueError, match="40,000"):
        draw_sample(frame, sample_size=40_000, seed=1)
