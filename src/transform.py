import pandas as pd
from dateutil import tz

def transform_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Datetime normalization
    df["transdate"] = pd.to_datetime(df["transdate"])
    df["winlostdate"] = pd.to_datetime(df["winlostdate"])

    # Numeric normalization
    df["stake"] = pd.to_numeric(df["stake"], errors="coerce") #「轉型失敗的值，不要報錯，直接變成 NaN」
    df["actualrate"] = pd.to_numeric(df["actualrate"], errors="coerce")

    #liveindicator cleanup transform to boolean
    df["liveindicator"] = df["liveindicator"].astype(bool)


    # Status cleanup
    df["status"] = df["status"].str.upper().str.strip()

    # ETL metadata
    company_tz = tz.gettz("Etc/GMT+4")
    df["etl_load_time"] = pd.Timestamp.now(tz=company_tz)
    return df


if __name__ == "__main__":
    """
    Local test only.
    Not executed when imported by main ETL pipeline.
    """
    from extract import extract_transactions

    # 1. 先抽原始資料
    raw_df = extract_transactions("2025-12-24", "2025-12-24")

    print("=== RAW DATA ===")
    print(raw_df.dtypes)
    print(raw_df.head())

    # 2. 做 transform
    transformed_df = transform_transactions(raw_df)

    print("\n=== TRANSFORMED DATA ===")
    print(transformed_df.dtypes)
    print(transformed_df.head())
    