import os
import glob
from pathlib import Path
import pandas as pd

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
    "_LLCPWT"
]

def load_and_save_thin_table():
    # البحث التلقائي عن أي ملف بامتداد xpt داخل مجلد raw
    xpt_files = list(RAW_DIR.glob("*.[xX][pP][tT]")) + list(RAW_DIR.glob("*LLCP*"))
    xpt_files = [f for f in xpt_files if f.is_file() and not f.name.startswith('.')]
    
    if not xpt_files:
        raise FileNotFoundError(f"لم يتم العثور على أي ملف XPT داخل المجلد: {RAW_DIR}")

    target_file = xpt_files[0]
    print(f"تم العثور على الملف: {target_file.name}")
    print("جاري قراءة البيانات، يرجى الانتظار ثوانٍ...")
    
    df_raw = pd.read_sas(str(target_file), format="xport", encoding="latin-1")
    df_raw.columns = [col.upper() for col in df_raw.columns]
    
    cols_to_keep = [col.upper() for col in REQUIRED_COLUMNS]
    df_thin = df_raw[cols_to_keep].copy()
    df_thin.insert(0, "row_id", range(1, len(df_thin) + 1))
    
    os.makedirs(PROCESSED_DATA_PATH.parent, exist_ok=True)
    df_thin.to_parquet(str(PROCESSED_DATA_PATH), index=False)
    
    print("\n✅ تم إنشاء ملف Parquet بنجاح!")
    print(f"عدد الصفوف: {len(df_thin)}")
    print(f"الأعمدة المحفوظة: {list(df_thin.columns)}")
    print(f"مسار الحفظ: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    load_and_save_thin_table()
