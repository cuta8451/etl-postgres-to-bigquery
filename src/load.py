from google.cloud import bigquery
import pandas as pd
import uuid

def load_to_bigquery_idempotent(df: pd.DataFrame,   project_id: str,    dataset_id: str,    target_table: str,):
    client = bigquery.Client(project=project_id)

    # 1️⃣ staging table（每次跑都不一樣）
    staging_table = f"_staging_transactions_{uuid.uuid4().hex}"
    staging_ref = f"{project_id}.{dataset_id}.{staging_table}"
    target_ref = f"{project_id}.{dataset_id}.{target_table}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE",)  # 如果目標 table 已存在：刪掉裡面所有資料，然後再寫入新資料
    # 2️⃣ Load DataFrame → staging
    load_job = client.load_table_from_dataframe(df, staging_ref, job_config=job_config,)
    load_job.result()

    # 3️⃣ MERGE（idempotent 核心）
    merge_sql = f"""
    MERGE `{target_ref}` T
    USING `{staging_ref}` S
    ON T.transid = S.transid

    WHEN MATCHED THEN
      UPDATE SET
        stake = S.stake,
        status = S.status,
        winlostdate = S.winlostdate,
        actualrate = S.actualrate,
        inserttime = S.inserttime,
        etl_load_time = S.etl_load_time

    WHEN NOT MATCHED THEN
      INSERT ROW
    """

    client.query(merge_sql).result()

    # 4️⃣ 清 staging table
    client.delete_table(staging_ref, not_found_ok=True)

    print(f"MERGE completed into {target_ref}")
