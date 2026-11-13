import pandas as pd
from validation import validate_transactions

df = pd.read_csv("data/raw/transactions.csv", dtype={"reference_id": "string"})

ref = df["reference_id"].dropna().iloc[0]
idx = df[df["reference_id"] == ref].index[0]

df = df.drop(idx)

valid_df, rejected_df = validate_transactions(df)

print("Rejected records:", len(rejected_df))
print(rejected_df)