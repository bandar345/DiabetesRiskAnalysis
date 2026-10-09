import os
import glob
import sys
from pathlib import Path
import pandas as pd
import numpy as np

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from diabetes_risk.config import SAMPLE_SEED, SAMPLE_SIZE

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "brfss2024_thin.parquet"

REQUIRED_COLUMNS = [
    "DIABETE4",
    "DIABTYPE",
    "_AGE80",
    "HEIGHT3",
    "WEIGHT2",
    "_BMI5",
    "EXERANY2",
    "_SMOKER3",
    "USENOW3",
    "ECIGNOW3",
    "_RFDRHV9",
    "SEXVAR",
    "SSBSUGR2",
    "_LLCPWT"
]


def is_eligible(frame):
    """DIABETE4 in {1, 3, 4} and SSBSUGR2 in 101–399 or 888."""
    diabetes = pd.to_numeric(frame["DIABETE4"], errors="coerce").round()
    soda = pd.to_numeric(frame["SSBSUGR2"], errors="coerce").round()
    diabetes_ok = diabetes.isin([1, 3, 4])
    soda_ok = soda.between(101, 399) | soda.eq(888)
    return (diabetes_ok & soda_ok).fillna(False)


def _class_quotas(class_counts, sample_size):
    """Largest-remainder quotas so class shares match the eligible rows."""
    raw = class_counts.astype(float) / float(class_counts.sum()) * sample_size
    sizes = np.floor(raw).astype(int)
    shortfall = sample_size - int(sizes.sum())
    order = sorted(
        class_counts.index,
        key=lambda code: (-(float(raw[code]) - int(sizes[code])), int(code)),
    )
    for code in order[:shortfall]:
        sizes[code] += 1
    return {int(code): int(sizes[code]) for code in class_counts.index}


def draw_sample(frame, sample_size, seed):
    """Stratified sample of eligible interviews. Same seed, same rows."""
    eligible = frame.loc[is_eligible(frame)].copy()
    if len(eligible) < sample_size:
        raise ValueError(
            f"Need {sample_size:,} eligible interviews, found {len(eligible):,}."
        )

    classes = pd.to_numeric(eligible["DIABETE4"], errors="coerce").round().astype("Int64")
    quotas = _class_quotas(classes.value_counts(), sample_size)
    rng = np.random.default_rng(seed)
    picked = []
    for code in sorted(quotas):
        pool = np.sort(eligible.index[classes == code].to_numpy())
        chosen = rng.choice(pool, size=quotas[code], replace=False)
        picked.append(eligible.loc[chosen])

    sampled = pd.concat(picked)
    if "row_id" in sampled.columns:
        sampled = sampled.sort_values("row_id")
    else:
        sampled = sampled.sort_index()
    return sampled.reset_index(drop=True)


def load_and_save_thin_table():
    # البحث التلقائي عن أي ملف بامتداد xpt داخل مجلد raw
    xpt_files = list(RAW_DIR.glob("*.[xX][pP][tT]")) + list(RAW_DIR.glob("*LLCP*"))
    xpt_files = [f for f in xpt_files if f.is_file() and not f.name.startswith('.')]
    
    if not xpt_files:
        raise FileNotFoundError(f"داخل المجلد XPT لم يتم العثور على أي ملف :{RAW_DIR}")
        
    target_file = xpt_files[0]
    print(f"تم العثور على الملف: {target_file.name}")
    print("...جاري قراءة البيانات، يرجى الانتظار ثوانٍ")
    
    df_raw = pd.read_sas(str(target_file), format="xport", encoding="latin-1")
    df_raw.columns = [col.upper() for col in df_raw.columns]
    
    cols_to_keep = [col.upper() for col in REQUIRED_COLUMNS]
    df_thin = df_raw[cols_to_keep].copy()
    
    # 40,000 eligible interviews, stratified on DIABETE4. Size and seed are in config.py.
    df_thin = draw_sample(df_thin, SAMPLE_SIZE, SAMPLE_SEED)
        
    df_thin.insert(0, "row_id", range(1, len(df_thin) + 1))
    
    os.makedirs(PROCESSED_DATA_PATH.parent, exist_ok=True)
    df_thin.to_parquet(str(PROCESSED_DATA_PATH), index=False)
    
    print("\nتم إنشاء ملف Parquet بنجاح!")
    print(f"عدد الصفوف: {len(df_thin)}")
    print(f"الأعمدة المحفوظة: {list(df_thin.columns)}")
    print(f"مسار الحفظ: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    load_and_save_thin_table()
