
import pandas as pd
import random
import argparse
import os
from datetime import datetime, timedelta


def generate_transactions(num_records=1000, seed=42):

    random.seed(seed)

    records = []

    accounts = ["ACC001", "ACC002", "ACC003", "ACC004", "ACC005"]

    balances = {account: 10000 for account in accounts}

    base_time = datetime(2026, 11, 13, 9, 0, 0)

    # Generate normal debit and credit transactions
    for i in range(num_records):

        account = random.choice(accounts)
        transaction_type = random.choice(["DEBIT", "CREDIT"])
        amount = random.randint(100, 2000)

        balance_before = balances[account]

        if transaction_type == "DEBIT" and balance_before < amount:
            transaction_type = "CREDIT"

        if transaction_type == "DEBIT":
            balance_after = balance_before - amount
        else:
            balance_after = balance_before + amount

        balances[account] = balance_after

        records.append({
            "transaction_id": f"TXN{i+1:06d}",
            "account_id": account,
            "transaction_type": transaction_type,
            "amount": amount,
            "currency": "INR",
            "event_time": (
                base_time + timedelta(minutes=i)
            ).isoformat(),
            "reference_id": None,
            "balance_before": balance_before,
            "balance_after": balance_after
        })

    # Generate 10 balanced transfer pairs
    for i in range(10):

        eligible_accounts = [
            account for account in accounts
            if balances[account] >= 500
        ]

        sender = random.choice(eligible_accounts)

        receiver = random.choice([
            account for account in accounts
            if account != sender
        ])

        amount = 500
        reference = f"TRF{i+1:03d}"

        before = balances[sender]
        balances[sender] -= amount

        records.append({
            "transaction_id": f"TXN{num_records+i*2+1:06d}",
            "account_id": sender,
            "transaction_type": "DEBIT",
            "amount": amount,
            "currency": "INR",
            "event_time": (
                base_time + timedelta(minutes=num_records+i*2)
            ).isoformat(),
            "reference_id": reference,
            "balance_before": before,
            "balance_after": balances[sender]
        })

        before = balances[receiver]
        balances[receiver] += amount

        records.append({
            "transaction_id": f"TXN{num_records+i*2+2:06d}",
            "account_id": receiver,
            "transaction_type": "CREDIT",
            "amount": amount,
            "currency": "INR",
            "event_time": (
                base_time + timedelta(minutes=num_records+i*2+1)
            ).isoformat(),
            "reference_id": reference,
            "balance_before": before,
            "balance_after": balances[receiver]
        })

    return pd.DataFrame(records)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--records", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.records < 1:
        parser.error("--records must be at least 1")

    df = generate_transactions(args.records, args.seed)

    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/transactions.csv"

    df.to_csv(output_path, index=False)

    print("Transaction data generated successfully!")
    print("Requested normal records:", args.records)
    print("Total records including transfer legs:", len(df))
    print("Output file:", output_path)
