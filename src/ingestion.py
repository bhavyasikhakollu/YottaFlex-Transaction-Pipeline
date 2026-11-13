
import os
import pandas as pd


def ingest_transactions(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    try:
        df = pd.read_csv(
            file_path,
            dtype={"reference_id": "string"}
        )

    except pd.errors.EmptyDataError:
        raise ValueError("Input CSV file is empty")

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Malformed CSV file: {error}"
        ) from error

    print("Data ingestion completed successfully!")
    print("Total records loaded:", len(df))

    return df


if __name__ == "__main__":

    df = ingest_transactions("data/raw/transactions.csv")
    print(df.head())
