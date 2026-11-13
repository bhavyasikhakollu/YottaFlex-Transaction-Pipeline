
# Transaction Pipeline Architecture

```text
        Raw Transaction CSV
                |
                v
          Data Ingestion
                |
                v
       Schema and Data Validation
                |
          +-----+-----+
          |           |
          v           v
     Valid Data   Rejected Data
          |           |
          v           v
     Transformation  Quarantine CSV
          |
          v
     Parquet Publishing
          |
          v
     DuckDB Reporting
          |
          v
     Metrics and Reconciliation
```

## Components

1. Ingestion: Reads transaction records from CSV.
2. Validation: Checks schema, duplicates, balances, currency, event ordering and transfers.
3. Quarantine: Stores rejected records with reasons.
4. Transformation: Converts timestamps and derives transaction dates.
5. Publishing: Writes valid transactions to Parquet.
6. Reporting: Uses DuckDB to query published data.
7. Monitoring: Tracks counts, execution time, run ID and logs.
