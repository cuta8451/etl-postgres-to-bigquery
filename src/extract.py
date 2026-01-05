import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME")
}

def get_engine():
    connection_string = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(connection_string)

def extract_transactions(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Extract transactions by transdate in [start_date, end_date]
    end_date is inclusive (we add 1 day in SQL).
    """
    engine = get_engine()

    query = f"""
    SELECT *
    FROM transactions
    WHERE transdate >= '{start_date}'
      AND transdate < DATE_ADD('{end_date}', INTERVAL 1 DAY)
    """

    df = pd.read_sql(query, engine)
    return df

if __name__ == "__main__":
    df = extract_transactions("2025-12-24", "2025-12-24")
    print("資料筆數:", len(df))
    print(df.head())
