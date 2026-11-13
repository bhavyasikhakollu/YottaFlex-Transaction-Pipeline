

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


def run_with_retry(operation, operation_name, max_attempts=3, delay=2):
    """Retry temporary I/O failures up to three times."""

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()

        except (OSError, TimeoutError, ConnectionError):
            logging.exception(
                "%s failed on attempt %s",
                operation_name,
                attempt
            )

            if attempt == max_attempts:
                raise

            print(
                f"Retrying {operation_name}: "
                f"attempt {attempt + 1}/{max_attempts}"
            )

            time.sleep(delay)


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
    status = "FAILED"

    logging.info("Pipeline started. Run ID: %s", run_id)

    try:
        print("Starting transaction pipeline...")
        print("Run ID:", run_id)

        # 1. Ingestion with retry
        df = run_with_retry(
            lambda: ingest_transactions(
                "data/raw/transactions.csv"
            ),
            "data ingestion"
        )

        # 2. Validation
        valid_df, rejected_df = validate_transactions(df)

        # 3. Transformation
        transformed_df = transform_transactions(valid_df)

        # 4. Publishing with retry
        run_with_retry(
            lambda: publish_transactions(
                transformed_df,
                rejected_df
            ),
            "publishing"
        )

        # 5. Metrics
        calculate_metrics(
            len(df),
            len(valid_df),
            len(rejected_df)
        )

        status = "SUCCESS"

        print("Pipeline completed successfully.")
        print("Total records:", len(df))
        print("Valid records:", len(valid_df))
        print("Rejected records:", len(rejected_df))

    except Exception:
        logging.exception(
            "Pipeline failed. Run ID: %s",
            run_id
        )
        print("Pipeline failed. Check outputs/pipeline.log")
        raise

    finally:
        duration = (datetime.now() - start_time).total_seconds()

        logging.info(
            "Pipeline finished. Run ID: %s | Status: %s | Duration: %.2f seconds",
            run_id,
            status,
            duration
        )

        print("Pipeline status:", status)
        print(f"Execution time: {duration:.2f} seconds")


if __name__ == "__main__":
    run_pipeline()
