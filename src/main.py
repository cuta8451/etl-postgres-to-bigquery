# src/main.py
from extract import extract_transactions
from transform import transform_transactions
from load import load_to_bigquery_idempotent
from logger import get_logger

logger = get_logger("etl_pipeline")

def run_pipeline(start_date: str, end_date: str):
    logger.info("Pipeline started")

    logger.info("Extract step started")
    df_raw = extract_transactions(start_date, end_date)
    logger.info(f"Extract completed: {len(df_raw)} rows")

    logger.info("Transform step started")
    df_transformed = transform_transactions(df_raw)
    logger.info("Transform completed")

    logger.info("Load step started")
    load_to_bigquery_idempotent(
        df=df_transformed,
        project_id="data-platform-483701",
        dataset_id="etl_demo",
        target_table="O_transactions_p",
    )
    logger.info("Load completed")

    logger.info("Pipeline finished successfully")

if __name__ == "__main__":
    run_pipeline("2025-12-24", "2025-12-24")
