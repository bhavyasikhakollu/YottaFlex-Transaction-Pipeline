# Reliability, Retry and Recovery

## 1. Rerun Safety

The pipeline overwrites existing Parquet and quarantine outputs instead of appending records. Reprocessing the same input does not create duplicate output records.

## 2. Failure Handling

The main pipeline uses exception handling.

If an unexpected error occurs:
- The error is recorded in outputs/pipeline.log.
- The Run ID is recorded for traceability.
- The pipeline reports failure and stops.

## 3. Rejected Records

Invalid transactions are stored separately in the quarantine CSV file with rejection reasons. Valid transactions continue through publishing.

## 4. Retry Strategy

Automatic retry is not implemented.

The operator can correct the input or environment issue and rerun the pipeline. The pipeline overwrites previous outputs.

## 5. Partial Failure Recovery

Publishing first creates temporary output files and backups of existing outputs.

If publishing fails after one output has been replaced, the pipeline attempts to restore the previous output using its backup.

This is best-effort rollback, not a fully atomic transaction across both files. Recovery can still require operator intervention if rollback itself fails.

## 6. Backfill

Historical input files can be processed again by updating the input path and rerunning the pipeline.

## 7. Known Limitations

- Automatic retry is not implemented.
- There is no distributed transaction across output files.
- External reference-master validation is not implemented.
- Rollback is best-effort and depends on successful file operations.
