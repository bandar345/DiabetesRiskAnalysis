import os
import pandas as pd

# مسارات الملفات
RAW_DATA_PATH = "data/raw/LLCP2024.XPT"
PROCESSED_DATA_PATH = "data/processed/brfss2024_thin.parquet"

# الأعمدة المحددة في Contract و Data Dictionary
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
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"Raw data file not found at {RAW_DATA_PATH}. "
            "Please download the 2024 BRFSS XPT file from the CDC website and place it in data/raw/."
        )

    print(f"Reading raw data from: {RAW_DATA_PATH}...")
    df_raw = pd.read_sas(RAW_DATA_PATH, format="xport", encoding="latin-1")
    
    # توحيد أسماء الأعمدة بأحرف كبيرة لتفادي الأخطاء
    df_raw.columns = [col.upper() for col in df_raw.columns]
    
    # اختيار الأعمدة المطلوبة فقط
    cols_to_keep = [col.upper() for col in REQUIRED_COLUMNS]
    df_thin = df_raw[cols_to_keep].copy()
    
    # إضافة معرف فريد لكل صف
    df_thin.insert(0, "row_id", range(1, len(df_thin) + 1))
    
    # التأكد من وجود مجلد الحفظ
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    # حفظ الجدول بصيغة Parquet
    df_thin.to_parquet(PROCESSED_DATA_PATH, index=False)
    
    print("Thin Parquet table created successfully!")
    print(f"Row count: {len(df_thin)}")
    print(f"Columns: {list(df_thin.columns)}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    load_and_save_thin_table()
