# Root-Cause Analysis Report

This report summarizes simple root-cause style explanations for customers flagged as anomalous.

## Summary

- Anomalous records explained: 35
- Explanation logic: compare anomalous feature values with normal-population averages and rank largest relative deviations.

## Most Common Top Drivers

- `total_transaction_amount`: 14
- `average_resolution_time_hours`: 4
- `average_transaction_amount`: 4
- `complaint_count`: 3
- `days_since_last_login`: 3
- `max_transaction_amount`: 2
- `failed_transaction_count`: 2
- `support_ticket_count`: 2
- `region_encoded`: 1

## Example Explanations

- CUST-000015: total_transaction_amount is unusually high (3249.45 vs baseline 305.441); max_transaction_amount is unusually high (1306.39 vs baseline 146.7427); average_transaction_amount is unusually high (361.05 vs baseline 79.5133).
- CUST-000018: average_resolution_time_hours is unusually high (63.85 vs baseline 10.3351); failed_transaction_count is unusually high (5.0 vs baseline 1.7247); acquisition_channel_encoded is unusually high (4.0 vs baseline 1.5634).
- CUST-000042: average_resolution_time_hours is unusually high (39.59 vs baseline 10.3351); failed_transaction_count is unusually high (6.0 vs baseline 1.7247); max_transaction_amount is unusually high (423.11 vs baseline 146.7427).
- CUST-000043: total_transaction_amount is unusually high (1763.39 vs baseline 305.441); average_transaction_amount is unusually high (293.8983 vs baseline 79.5133); max_transaction_amount is unusually high (455.65 vs baseline 146.7427).
- CUST-000058: total_transaction_amount is unusually high (1509.48 vs baseline 305.441); failed_transaction_count is unusually high (7.0 vs baseline 1.7247); max_transaction_amount is unusually high (457.87 vs baseline 146.7427).
- CUST-000079: average_resolution_time_hours is unusually high (53.45 vs baseline 10.3351); days_since_last_login is unusually high (23.9 vs baseline 9.2959); failed_transaction_count is unusually high (4.0 vs baseline 1.7247).
- CUST-000081: total_transaction_amount is unusually high (847.11 vs baseline 305.441); days_since_last_login is unusually high (25.1 vs baseline 9.2959); max_transaction_amount is unusually high (385.99 vs baseline 146.7427).
- CUST-000090: max_transaction_amount is unusually high (2261.48 vs baseline 146.7427); total_transaction_amount is unusually high (3504.55 vs baseline 305.441); average_transaction_amount is unusually high (700.91 vs baseline 79.5133).
- CUST-000118: complaint_count is unusually high (2.0 vs baseline 0.3054); support_ticket_count is unusually high (3.0 vs baseline 1.1849); failed_transaction_count is unusually high (4.0 vs baseline 1.7247).
- CUST-000127: total_transaction_amount is unusually high (2268.75 vs baseline 305.441); max_transaction_amount is unusually high (740.28 vs baseline 146.7427); average_transaction_amount is unusually high (378.125 vs baseline 79.5133).

## Limitations

- These explanations are heuristic and compare feature deviations against local synthetic baselines.
- Driver rankings are not causal explanations.
- The logic is intended for portfolio evidence and future investigation workflows, not production decisions.
