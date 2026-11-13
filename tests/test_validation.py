
import pandas as pd
import sys
sys.path.insert(0, "src")
from validation import validate_transactions


def test_valid_transaction():
    df = pd.DataFrame([{
        "transaction_id": "TXN001",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 1000,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 5000,
        "balance_after": 4000,
        "reference_id": None
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_negative_amount():
    df = pd.DataFrame([{
        "transaction_id": "TXN002",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": -500,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 5000,
        "balance_after": 4500,
        "reference_id": None
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 0
    assert len(rejected) == 1

def test_invalid_currency():
    df = pd.DataFrame([{
        "transaction_id": "TXN003",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 1000,
        "currency": "USD",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 5000,
        "balance_after": 4000,
        "reference_id": None
    }])

    valid, rejected = validate_transactions(df)
    assert len(rejected) == 1


def test_incorrect_balance():
    df = pd.DataFrame([{
        "transaction_id": "TXN004",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 1000,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 5000,
        "balance_after": 4500,
        "reference_id": None
    }])

    valid, rejected = validate_transactions(df)
    assert len(rejected) == 1

def test_duplicate_transaction():
    record = {
        "transaction_id": "TXN005",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 1000,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 5000,
        "balance_after": 4000,
        "reference_id": None
    }

    df = pd.DataFrame([record, record.copy()])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 1
    assert len(rejected) == 1

def test_missing_required_value():
    df = pd.DataFrame([{
        "transaction_id": "TXN006",
        "account_id": None,
        "transaction_type": "DEBIT",
        "amount": 500,
        "currency": "INR",
        "event_time": "2026-11-13 10:00:00",
        "balance_before": 5000,
        "balance_after": 4500
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 0
    assert len(rejected) == 1

def test_missing_transaction_id():
    df = pd.DataFrame([{
        "transaction_id": None,
        "account_id": "ACC001",
        "transaction_type": "DEBIT",
        "amount": 500,
        "currency": "INR",
        "event_time": "2026-11-13",
        "balance_before": 5000,
        "balance_after": 4500
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 0
    assert len(rejected) == 1

def test_unmatched_transfer_reference():
    df = pd.DataFrame([{
        "transaction_id": "TXN007",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 500,
        "currency": "INR",
        "event_time": "2026-11-13T11:00:00",
        "balance_before": 5000,
        "balance_after": 4500,
        "reference_id": "TRF999"
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid transfer pair" in rejected.iloc[0]["rejection_reason"]
def test_out_of_order_transaction():
    first = {
        "transaction_id": "TXN101",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 100,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 1000,
        "balance_after": 900,
        "reference_id": None
    }

    second = first.copy()
    second.update({
        "transaction_id": "TXN102",
        "event_time": "2026-11-13T09:00:00"
    })

    valid, rejected = validate_transactions(pd.DataFrame([first, second]))

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Out-of-order transaction" in rejected.iloc[0]["rejection_reason"]


def test_valid_transfer_pair():
    debit = {
        "transaction_id": "TXN201",
        "account_id": "ACC101",
        "transaction_type": "DEBIT",
        "amount": 500,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "balance_before": 1000,
        "balance_after": 500,
        "reference_id": "TRF201"
    }

    credit = debit.copy()
    credit.update({
        "transaction_id": "TXN202",
        "account_id": "ACC102",
        "transaction_type": "CREDIT",
        "balance_before": 200,
        "balance_after": 700
    })

    valid, rejected = validate_transactions(pd.DataFrame([debit, credit]))

    assert len(valid) == 2
    assert len(rejected) == 0
