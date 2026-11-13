
import os
import uuid
import logging
import time
from datetime import datetime

from ingestion import ingest_transactions
from validation import validate_transactions
from transformation import transform_transactions
from publishing import publish_transactions
from metrics import calculate_metrics


def run_pipeline():

    os.makedirs("outputs", exist_ok=True)

    logging.basicConfig(
        filename="outputs/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )

    run_id = str(uuid.uuid4())
    start_time = datetime.now()
    start_clock = time.perf_counter()

    print("\n--- PIPELINE STARTED ---")
    print("Run ID:", run_id)
    print("Start time:", start_time)

    logging.info("Pipeline started. Run ID: %s", run_id)

    status = "FAILED"

    try:
        df = ingest_transactions("data/raw/transactions.csv")

        valid_df, rejected_df = validate_transactions(df)

        transformed_df = transform_transactions(valid_df)

        publish_transactions(transformed_df, rejected_df)

        calculate_metrics(
            len(df),
            len(valid_df),
            len(rejected_df)
        )

        status = "SUCCESS"

        print("\n--- PIPELINE COMPLETED ---")
        print("Total records:", len(df))
        print("Valid records:", len(valid_df))
        print("Rejected records:", len(rejected_df))

    except Exception:
        logging.exception("Pipeline failed. Run ID: %s", run_id)
        print("Pipeline failed. Check outputs/pipeline.log")
        raise

    finally:
        end_time = datetime.now()
        duration = time.perf_counter() - start_clock

        print("Status:", status)
        print("End time:", end_time)
        print("Execution time:", round(duration, 2), "seconds")

        logging.info(
            "Pipeline ended. Run ID: %s | Status: %s | Duration: %.2f seconds",
            run_id, status, duration
        )


if __name__ == "__main__":
    run_pipeline()
