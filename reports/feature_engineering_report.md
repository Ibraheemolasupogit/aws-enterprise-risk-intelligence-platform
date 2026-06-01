# Feature Engineering Report

This report summarizes the local ML-ready feature dataset created from synthetic customer, transaction, support, behavioral, and experimentation data.

## Dataset Summary

- Row count: 500
- Column count: 31
- Duplicate `customer_id` count: 0
- Missing value count: 0

## Feature Groups

- `customer_features`: `account_age_days`, `customer_segment_encoded`, `region_encoded`, `acquisition_channel_encoded`
- `transaction_features`: `transaction_count`, `average_transaction_amount`, `max_transaction_amount`, `total_transaction_amount`, `failed_transaction_count`, `high_value_transaction_flag`, `transaction_risk_score`
- `support_features`: `support_ticket_count`, `average_resolution_time_hours`, `complaint_count`, `satisfaction_score`, `support_risk_score`
- `behavioural_features`: `login_count_30d`, `days_since_last_login`, `session_count_30d`, `activity_decline_score`, `engagement_risk_score`
- `experimentation_features`: `treatment_flag`, `experiment_group_encoded`, `pre_post_period_encoded`, `intervention_exposed`, `conversion_flag`, `retention_flag`
- `target_columns`: `fraud_label`, `churn_label`, `anomaly_label`

## Target Distributions

- `fraud_label`: 0: 403, 1: 97
- `churn_label`: 0: 452, 1: 48
- `anomaly_label`: 0: 465, 1: 35

## Feature Quality Notes

- Encoded categorical features use deterministic local mappings for reproducibility.
- Risk score features are lightweight proxies for later modeling and interpretation.
- Experimentation fields are retained so A/B testing and pre/post analysis can use the same feature table.
- No ML models are trained in this milestone.

## Risk Score Summary

| Feature | Mean | Min | Max |
| --- | ---: | ---: | ---: |
| `transaction_risk_score` | 0.2050 | 0.0014 | 0.7475 |
| `support_risk_score` | 0.1848 | 0.0000 | 0.6995 |
| `engagement_risk_score` | 0.2620 | 0.0504 | 0.8076 |
