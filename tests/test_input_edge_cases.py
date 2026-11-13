import pandas as pd
import pytest
import sys

sys.path.insert(0, "src")

from validation import validate_transactions


def test_empty_input():
    with pytest.raises(ValueError, match="Input data is empty"):
        validate_transactions(pd.DataFrame())


def test_malformed_input():
    df = pd.DataFrame({
        "transaction_id": ["TXN001"],
        "account_id": ["ACC001"]
    })

    with pytest.raises(ValueError, match="Missing columns"):
        validate_transactions(df)


def test_blank_reference_id():
    df = pd.DataFrame([{
        "transaction_id": "TXN001",
        "account_id": "ACC001",
        "transaction_type": "CREDIT",
        "amount": 100,
        "currency": "INR",
        "event_time": "2026-11-13T10:00:00",
        "reference_id": " ",
        "balance_before": 1000,
        "balance_after": 1100
    }])

    valid, rejected = validate_transactions(df)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid reference ID" in rejected.iloc[0]["rejection_reason"]
