# Anomaly Detection Report

This report summarizes baseline local anomaly detection on the processed synthetic feature dataset.

## Model Summary

- Model: `IsolationForest`
- Rows scored: 500
- Feature count: 25
- Anomaly count: 35
- Anomaly rate: 7.0%

## Risk Band Distribution

- `High`: 21
- `Low`: 333
- `Medium`: 146

## Top First-Driver Distribution For Flagged Anomalies

- `total_transaction_amount`: 14
- `average_transaction_amount`: 4
- `average_resolution_time_hours`: 4
- `days_since_last_login`: 3
- `complaint_count`: 3
- `max_transaction_amount`: 2
- `failed_transaction_count`: 2
- `support_ticket_count`: 2
- `region_encoded`: 1

## Interpretation

- The anomaly score is normalized so higher values indicate more unusual records.
- Driver columns identify the largest feature deviations compared with the normal population.
- This is a local baseline for investigation evidence, not a production alerting system.
- No AWS services are used in this milestone.
