
def calculate_metrics(total, valid, rejected):

    success_rate = (
        valid / total * 100
        if total > 0 else 0
    )

    print("\n--- PIPELINE METRICS ---")
    print("Total transactions:", total)
    print("Valid transactions:", valid)
    print("Rejected transactions:", rejected)
    print("Success rate:", round(success_rate, 2), "%")

    reconciled = total == valid + rejected

    if reconciled:
        print("Reconciliation: PASSED")
    else:
        print("Reconciliation: FAILED")
        raise ValueError(
            "Reconciliation failed: total does not equal valid + rejected"
        )

    return {
        "total": total,
        "valid": valid,
        "rejected": rejected,
        "success_rate": round(success_rate, 2),
        "reconciliation": reconciled
    }
