import os
import sys
import pandas as pd
import pytest

sys.path.insert(0, "src")
from publishing import publish_transactions


def test_partial_publish_failure_rolls_back(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    os.makedirs("outputs")
    os.makedirs("data/quarantine")

    valid_path = "outputs/transactions.parquet"
    rejected_path = "data/quarantine/rejected_transactions.csv"

    pd.DataFrame({"old": [1]}).to_parquet(valid_path)
    pd.DataFrame({"old": [1]}).to_csv(rejected_path, index=False)

    with open(valid_path, "rb") as f:
        original_valid = f.read()

    with open(rejected_path, "rb") as f:
        original_rejected = f.read()

    real_replace = os.replace
    calls = 0

    def failing_replace(src, dst):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("Simulated publishing failure")
        return real_replace(src, dst)

    monkeypatch.setattr(os, "replace", failing_replace)

    with pytest.raises(OSError):
        publish_transactions(
            pd.DataFrame({"new": [2]}),
            pd.DataFrame({"new": [2]})
        )

    with open(valid_path, "rb") as f:
        assert f.read() == original_valid

    with open(rejected_path, "rb") as f:
        assert f.read() == original_rejected
