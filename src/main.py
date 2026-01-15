from extract import extract_transactions
from transform import transform_transactions
from load import load_to_bigquery_idempotent

if __name__ == "__main__":
    df_raw = extract_transactions("2025-12-24", "2025-12-24")
    df_transformed = transform_transactions(df_raw)

    load_to_bigquery_idempotent(
        df=df_transformed,
        project_id="data-platform-483701",
        dataset_id="etl_demo",
        target_table="O_transactions_p",
    )
