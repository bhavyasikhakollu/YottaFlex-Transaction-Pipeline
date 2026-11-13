
# Reliability, Retry and Recovery

## 1. Rerun Safety

The pipeline overwrites the existing Parquet output instead of appending records.

Running the same input again does not create duplicate output records.

## 2. Failure Handling

The main pipeline uses exception handling.

If an unexpected error occurs:
- The error is recorded in outputs/pipeline.log.
- The Run ID is recorded for traceability.
- The pipeline reports failure and stops.

## 3. Rejected Records

Invalid transactions are stored separately in the quarantine CSV file with rejection reasons.

Valid records continue through the publishing process.

## 4. Retry Strategy

Automatic retry is not implemented in the current version.

For recovery, the operator can correct the input or environment issue and rerun the pipeline.

## 5. Partial Failure Limitation

Publishing currently writes the Parquet and quarantine outputs separately. It does not provide an atomic transaction across both files.

A production implementation could use temporary output files, atomic replacement, run-specific folders and checkpoint-based recovery.

## 6. Backfill

Historical input files can be processed again by updating the input path and rerunning the pipeline.
