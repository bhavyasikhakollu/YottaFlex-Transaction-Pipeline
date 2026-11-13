import pandas as pd
from validation import validate_transactions

df = pd.read_csv("data/raw/transactions.csv", dtype={"reference_id": "string"})

account = df.loc[0, "account_id"]
rows = df.index[df["account_id"] == account].tolist()

df.loc[rows[1], "event_time"] = (
    pd.to_datetime(df.loc[rows[0], "event_time"])
    - pd.Timedelta(minutes=1)
).isoformat()

valid_df, rejected_df = validate_transactions(df)

print("Rejected records:", len(rejected_df))
print(rejected_df[["transaction_id", "rejection_reason"]])