
import os
import shutil
import pandas as pd


def publish_transactions(valid_df, rejected_df):

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data/quarantine", exist_ok=True)

    paths = [
        ("outputs/transactions.parquet", valid_df, "parquet"),
        ("data/quarantine/rejected_transactions.csv", rejected_df, "csv")
    ]

    temp_files = []
    backups = {}
    published = []

    try:
        # Prepare temporary outputs and backups
        for path, df, file_type in paths:

            temp = path + ".tmp"
            backup = path + ".bak"

            if file_type == "parquet":
                df.to_parquet(temp, index=False)
            else:
                df.to_csv(temp, index=False)

            temp_files.append(temp)

            if os.path.exists(path):
                shutil.copy2(path, backup)
                backups[path] = backup
            else:
                backups[path] = None

        # Publish outputs
        for path, df, file_type in paths:
            temp = path + ".tmp"
            os.replace(temp, path)
            published.append(path)

        print("Publishing completed!")
        print("Valid records published:", len(valid_df))
        print("Rejected records saved:", len(rejected_df))

    except Exception:
        # Roll back already published outputs
        for path in reversed(published):

            backup = backups[path]

            if backup and os.path.exists(backup):
                os.replace(backup, path)
            elif os.path.exists(path):
                os.remove(path)

        raise

    finally:
        # Remove temporary and unused backup files
        for path, df, file_type in paths:
            for suffix in [".tmp", ".bak"]:
                file = path + suffix
                if os.path.exists(file):
                    os.remove(file)


if __name__ == "__main__":

    from ingestion import ingest_transactions
    from validation import validate_transactions
    from transformation import transform_transactions

    df = ingest_transactions("data/raw/transactions.csv")
    valid_df, rejected_df = validate_transactions(df)
    transformed_df = transform_transactions(valid_df)

    publish_transactions(transformed_df, rejected_df)
