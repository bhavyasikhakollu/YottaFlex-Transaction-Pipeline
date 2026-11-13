# YottaFlex Transaction Pipeline

## 1. Project Overview

This project implements a transaction data pipeline that processes financial transaction records.

It ingests transaction data, validates records, separates valid and rejected transactions, transforms valid data and publishes the output in Parquet format.

The pipeline also generates operational metrics, logs execution details and supports safe reruns.

## 2. Project Objectives

- Validate financial transactions using defined business rules.
- Identify and quarantine invalid records with rejection reasons.
- Validate debit and credit transfer pairs.
- Publish valid transactions in Parquet format.
- Maintain transaction count reconciliation.
- Track pipeline execution using logs, run IDs and metrics.
- Support repeatable processing without appending duplicate output records.

## 3. Technologies Used

- Python â€“ Main programming language
- Pandas â€“ Data processing and validation
- PyArrow â€“ Parquet file support
- DuckDB â€“ Data querying and analysis
- Pytest â€“ Automated testing
- Git â€“ Version control

## 4. Pipeline Workflow

1. Generate sample transaction data.
2. Ingest transaction records from CSV.
3. Validate schema and transaction fields.
4. Separate valid and rejected records.
5. Validate balances, duplicates and transfer pairs.
6. Transform valid transactions.
7. Publish valid records as Parquet.
8. Save rejected records in quarantine.
9. Calculate operational metrics.
10. Perform reconciliation and reporting.

## 5. Data Validation Rules

The pipeline validates:

1. Required fields must be present.
2. Transaction IDs must be unique.
3. Account IDs must not be empty.
4. Transaction amounts must be positive and finite.
5. Transaction type must be DEBIT or CREDIT.
6. Currency must be INR.
7. Account balances must be calculated correctly.
8. Event timestamps must follow account event ordering.
9. Transfer transactions must contain matching debit and credit legs.
10. Transfer legs must have matching amounts and currencies.

Invalid records are stored separately in the quarantine folder with rejection reasons.

## 6. Project Structure

```text
YottaFlex-Transaction-Pipeline/
|
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- quarantine/
|
|-- src/
|   |-- generate_data.py
|   |-- ingestion.py
|   |-- validation.py
|   |-- transformation.py
|   |-- publishing.py
|   |-- metrics.py
|   |-- report.py
|   |-- main.py
|
|-- tests/
|-- docs/
|   |-- architecture.md
|   |-- data_dictionary.md
|   |-- reliability.md
|
|-- outputs/
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## 7. How to Run the Project

### Step 1: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Generate sample data

Generate 100,000 normal transactions and 20 transfer legs:

```powershell
python src/generate_data.py --records 100000 --seed 42
```

### Step 4: Run the pipeline

```powershell
python src/main.py
```

### Step 5: Run DuckDB reports

```powershell
python src/report.py
```

### Step 6: Run automated tests

```powershell
pytest -v
```

## 8. Output

- Valid transactions: `outputs/transactions.parquet`
- Rejected transactions: `data/quarantine/rejected_transactions.csv`
- Pipeline execution log: `outputs/pipeline.log`
- DuckDB reports: Transaction counts and amount statistics.

## 9. Sample Execution Results

**Dataset size:** 100,020 records

| Metric | Result |
|---|---:|
| Total transactions | 100,020 |
| Valid transactions | 100,020 |
| Rejected transactions | 0 |
| Success rate | 100% |
| Reconciliation | PASSED |
| Automated tests | 14 PASSED |

### DuckDB Report

| Metric | Result |
|---|---:|
| CREDIT records | 50,254 |
| DEBIT records | 49,766 |
| Total transaction amount | 104,704,652 |
| Highest transaction amount | 2,000 |
| Lowest transaction amount | 100 |
| Average transaction amount | 1,046.84 |

## 10. Testing and Reliability

- 14 automated tests passed using Pytest.
- Tested duplicate transaction IDs.
- Tested invalid transaction amounts and currencies.
- Tested missing required values.
- Tested out-of-order transactions.
- Tested incomplete transfer pairs.
- Tested empty and malformed input scenarios.
- Verified schema validation.
- Verified rerun safety: repeated execution overwrites previous output instead of appending duplicate records.
- Verified Parquet output using DuckDB.
- Verified reconciliation: total records = valid records + rejected records.

## 11. Reliability and Recovery

- Pipeline execution is tracked using a unique Run ID.
- Start time, end time and execution duration are recorded.
- Unexpected failures are logged in `outputs/pipeline.log`.
- Invalid records are stored separately with rejection reasons.
- Manual retry is supported by correcting the issue and rerunning the pipeline.
- Historical input data can be processed again for backfills.

Automatic retries and atomic publishing across both output files are not implemented in this version.

## 12. Documentation

Additional project documentation is available in the `docs/` folder:

- `architecture.md` â€“ Pipeline architecture and components.
- `data_dictionary.md` â€“ Column names, data types and descriptions.
- `reliability.md` â€“ Rerun safety, failure handling, retry and recovery.

## 13. Conclusion

The YottaFlex Transaction Pipeline demonstrates an end-to-end transaction processing workflow using Python, Pandas, PyArrow and DuckDB.

It includes data ingestion, validation, transformation, quarantine handling, Parquet publishing, operational metrics, reconciliation and automated testing.

The project focuses on data quality, reliability, traceability and repeatable processing.


### Performance Measurement

A local execution processed 100,020 transactions in 30.65 seconds.

| Metric | Result |
|---|---:|
| Records processed | 100,020 |
| Execution time | 30.65 seconds |
| Throughput | Approximately 3,265 records/second |

Performance may vary depending on hardware and execution environment.
