
import pandas as pd


def transform_transactions(df):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        return df.copy()

    required_columns = [
        "event_time",
        "transaction_type"
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing transformation columns: {sorted(missing)}"
        )

    transformed_df = df.copy()

    transformed_df["event_time"] = pd.to_datetime(
        transformed_df["event_time"],
        errors="raise"
    )

    transformed_df["transaction_date"] = (
        transformed_df["event_time"].dt.date
    )

    transformed_df["transaction_type"] = (
        transformed_df["transaction_type"]
        .str.strip()
        .str.upper()
    )

    return transformed_df


if __name__ == "__main__":

    from ingestion import ingest_transactions
    from validation import validate_transactions

    df = ingest_transactions("data/raw/transactions.csv")

    valid_df, rejected_df = validate_transactions(df)

    transformed_df = transform_transactions(valid_df)

    print("\nTransformation completed!")
    print("Total transformed records:", len(transformed_df))
    print(transformed_df.head())

