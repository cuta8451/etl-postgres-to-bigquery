from google.cloud import bigquery
import pandas as pd

def load_to_bigquery(df: pd.DataFrame,   project_id: str,    dataset_id: str,    table_id: str):
    client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND",)  # 先 append，Day 6 再談 MERGE

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config,)

    job.result()  # 等待 job 完成

    print(f"Loaded {len(df)} rows into {table_ref}")


from extract import extract_transactions
from transform import transform_transactions
from load import load_to_bigquery

if __name__ == "__main__":
    df_raw = extract_transactions("2025-12-24", "2025-12-24")
    df_transformed = transform_transactions(df_raw)

    load_to_bigquery(
        df=df_transformed,
        project_id="data-platform-483701",
        dataset_id="etl_demo",
        table_id="O_transactions",
    )
