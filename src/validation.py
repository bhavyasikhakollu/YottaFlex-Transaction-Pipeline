
import math
import pandas as pd


def validate_transactions(df):

    # 1. Check input format
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        raise ValueError("Input data is empty")

    # 2. Check required columns
    required_columns = [
        "transaction_id",
        "account_id",
        "transaction_type",
        "amount",
        "currency",
        "event_time",
        "balance_before",
        "balance_after"
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {sorted(missing)}"
        )

    df = df.copy()

    if "reference_id" not in df.columns:
        df["reference_id"] = None

    records = df.to_dict(orient="records")

    results = []
    seen_ids = set()
    last_event_time = {}

    def is_missing(value):
        return pd.isna(value) or str(value).strip() == ""

    def finite_number(value):
        try:
            number = float(value)

            if math.isfinite(number):
                return number

        except (ValueError, TypeError, OverflowError):
            pass

        return None

    # 3. Validate individual transactions
    for record in records:

        errors = []

        # Required values
        for field in required_columns:
            if is_missing(record[field]):
                errors.append(f"Missing {field}")

        # Transaction ID and duplicate check
        transaction_id = record["transaction_id"]

        if not is_missing(transaction_id):

            transaction_id = str(transaction_id).strip()

            if transaction_id in seen_ids:
                errors.append("Duplicate transaction ID")
            else:
                seen_ids.add(transaction_id)

        # Reference ID validation
        reference_id = record["reference_id"]

        if pd.notna(reference_id):

            if str(reference_id).strip() == "":
                errors.append("Invalid reference ID")

            else:
                reference_id = str(reference_id).strip()
                record["reference_id"] = reference_id

        # Event-time validation
        event_time = pd.to_datetime(
            record["event_time"],
            errors="coerce"
        )

        account_id = record["account_id"]

        if pd.isna(event_time):

            errors.append("Invalid event time")

        elif not is_missing(account_id):

            if account_id in last_event_time:

                if event_time < last_event_time[account_id]:
                    errors.append("Out-of-order transaction")

                else:
                    last_event_time[account_id] = event_time

            else:
                last_event_time[account_id] = event_time

        # Amount validation
        amount = finite_number(record["amount"])

        if amount is None or amount <= 0:
            errors.append("Invalid transaction amount")

        # Transaction type
        transaction_type = record["transaction_type"]

        if transaction_type not in ["DEBIT", "CREDIT"]:
            errors.append("Invalid transaction type")

        # Currency
        if record["currency"] != "INR":
            errors.append("Unsupported currency")

        # Balance validation
        before = finite_number(record["balance_before"])
        after = finite_number(record["balance_after"])

        if before is None or after is None:

            errors.append("Invalid balance information")

        elif amount is not None and transaction_type in [
            "DEBIT", "CREDIT"
        ]:

            if transaction_type == "DEBIT":
                expected = before - amount
            else:
                expected = before + amount

            if round(after, 2) != round(expected, 2):
                errors.append("Incorrect account balance")

        results.append({
            "record": record,
            "errors": errors,
            "amount": amount
        })

    # 4. Validate transfer pairs
    transfer_groups = {}

    for item in results:

        record = item["record"]
        reference_id = record["reference_id"]

        if not is_missing(reference_id):

            key = str(reference_id).strip()

            transfer_groups.setdefault(key, []).append(item)

    for reference_id, group in transfer_groups.items():

        correct = (
            len(group) == 2
            and all(not item["errors"] for item in group)
            and {
                item["record"]["transaction_type"]
                for item in group
            } == {"DEBIT", "CREDIT"}
            and group[0]["amount"] == group[1]["amount"]
            and group[0]["record"]["currency"]
                == group[1]["record"]["currency"]
            and group[0]["record"]["account_id"]
                != group[1]["record"]["account_id"]
        )

        if not correct:

            for item in group:

                if "Invalid transfer pair" not in item["errors"]:
                    item["errors"].append("Invalid transfer pair")

    # 5. Separate valid and rejected records
    valid_records = []
    rejected_records = []

    for item in results:

        record = item["record"].copy()

        if item["errors"]:

            record["rejection_reason"] = "; ".join(
                item["errors"]
            )

            rejected_records.append(record)

        else:
            valid_records.append(record)

    valid_df = pd.DataFrame(valid_records)
    rejected_df = pd.DataFrame(rejected_records)

    return valid_df, rejected_df
