# Data Validation Report

This report validates the local synthetic sample datasets before feature engineering and model development.

## Summary

| Dataset | Rows | Columns | Status |
| --- | ---: | ---: | --- |
| `customers` | 500 | 6 | PASS |
| `transactions` | 2019 | 8 | PASS |
| `support_activity` | 500 | 5 | PASS |
| `behavioural_activity` | 500 | 5 | PASS |
| `risk_training_dataset` | 500 | 28 | PASS |

## customers

- Dataset name: `customers`
- Row count: 500
- Column count: 6
- Pass/fail status: PASS
- Missing value summary: None
- Duplicate check result: No duplicate IDs found. (0 duplicates in `customer_id`)
- Required column result: PASS
- Label distribution summary: No label columns present.
- Experiment group distribution: Not applicable.

## transactions

- Dataset name: `transactions`
- Row count: 2019
- Column count: 8
- Pass/fail status: PASS
- Missing value summary: None
- Duplicate check result: No duplicate IDs found. (0 duplicates in `transaction_id`)
- Required column result: PASS
- Label distribution summary:
  - `fraud_label`: 0: 1912, 1: 107
- Experiment group distribution: Not applicable.

## support_activity

- Dataset name: `support_activity`
- Row count: 500
- Column count: 5
- Pass/fail status: PASS
- Missing value summary: None
- Duplicate check result: No duplicate IDs found. (0 duplicates in `customer_id`)
- Required column result: PASS
- Label distribution summary: No label columns present.
- Experiment group distribution: Not applicable.

## behavioural_activity

- Dataset name: `behavioural_activity`
- Row count: 500
- Column count: 5
- Pass/fail status: PASS
- Missing value summary: None
- Duplicate check result: No duplicate IDs found. (0 duplicates in `customer_id`)
- Required column result: PASS
- Label distribution summary: No label columns present.
- Experiment group distribution: Not applicable.

## risk_training_dataset

- Dataset name: `risk_training_dataset`
- Row count: 500
- Column count: 28
- Pass/fail status: PASS
- Missing value summary: None
- Duplicate check result: No duplicate IDs found. (0 duplicates in `customer_id`)
- Required column result: PASS
- Label distribution summary:
  - `fraud_label`: 0: 403, 1: 97
  - `churn_label`: 0: 452, 1: 48
  - `anomaly_label`: 0: 465, 1: 35
  - `treatment_flag`: 0: 246, 1: 254
  - `intervention_exposed`: 0: 365, 1: 135
  - `conversion_flag`: 0: 391, 1: 109
  - `retention_flag`: 0: 52, 1: 448
- Experiment group distribution: treatment: 254, control: 246
- Pre/post distribution: post: 273, pre: 227
