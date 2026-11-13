import pandas as pd
from validation import validate_transactions

df = pd.read_csv("data/raw/transactions.csv", dtype={"reference_id": "string"})

df.loc[0, "amount"] = -100

valid_df, rejected_df = validate_transactions(df)

print("Rejected records:", len(rejected_df))
print(rejected_df[["transaction_id", "rejection_reason"]])