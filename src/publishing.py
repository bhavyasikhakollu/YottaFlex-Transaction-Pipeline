
import os
import pandas as pd


def publish_transactions(valid_df, rejected_df):

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data/quarantine", exist_ok=True)

    valid_path = "outputs/transactions.parquet"
    rejected_path = "data/quarantine/rejected_transactions.csv"

    valid_temp = valid_path + ".tmp"
    rejected_temp = rejected_path + ".tmp"

    try:

        # Write temporary output files first
        valid_df.to_parquet(
            valid_temp,
            index=False
        )

        rejected_df.to_csv(
            rejected_temp,
            index=False
        )

        # Replace previous outputs after successful writes
        os.replace(valid_temp, valid_path)
        os.replace(rejected_temp, rejected_path)

        print("Publishing completed!")
        print("Valid records published:", len(valid_df))
        print("Rejected records saved:", len(rejected_df))

    except Exception:

        # Remove incomplete temporary files
        for path in [valid_temp, rejected_temp]:

            if os.path.exists(path):
                os.remove(path)

        raise


if __name__ == "__main__":

    from ingestion import ingest_transactions
    from validation import validate_transactions
    from transformation import transform_transactions

    df = ingest_transactions("data/raw/transactions.csv")

    valid_df, rejected_df = validate_transactions(df)

    transformed_df = transform_transactions(valid_df)

    publish_transactions(transformed_df, rejected_df)
