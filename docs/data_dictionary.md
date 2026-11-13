
# Data Dictionary

| Column | Data Type | Description |
|---|---|---|
| transaction_id | String | Unique transaction identifier |
| account_id | String | Account involved in transaction |
| transaction_type | String | DEBIT or CREDIT |
| amount | Numeric | Transaction amount |
| currency | String | Transaction currency (INR) |
| event_time | Timestamp | Transaction event time |
| reference_id | String | Links transfer debit and credit legs |
| balance_before | Numeric | Account balance before transaction |
| balance_after | Numeric | Account balance after transaction |
| transaction_date | Date | Date extracted from event_time |
| rejection_reason | String | Reason for rejected transaction |
