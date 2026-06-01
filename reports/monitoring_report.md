# Monitoring Report

This report summarizes local monitoring evidence for data drift, prediction distributions, and risk bands.

## Data Drift Summary

- Features checked: 27
- Features flagged for drift: 0

## Top Drift Indicators

| Feature | Reference Mean | Current Mean | Mean Change | Drift Flag |
| --- | ---: | ---: | ---: | --- |
| `complaint_count` | 0.3080 | 0.3800 | 23.38% | False |
| `intervention_exposed` | 0.3040 | 0.2360 | -22.37% | False |
| `conversion_flag` | 0.2400 | 0.1960 | -18.33% | False |
| `high_value_transaction_flag` | 0.2440 | 0.2800 | 14.75% | False |
| `treatment_flag` | 0.5360 | 0.4800 | -10.45% | False |
| `experiment_group_encoded` | 0.5360 | 0.4800 | -10.45% | False |
| `average_resolution_time_hours` | 11.2546 | 10.1864 | -9.49% | False |
| `pre_post_period_encoded` | 0.5720 | 0.5200 | -9.09% | False |
| `transaction_count` | 3.8840 | 4.1920 | 7.93% | False |
| `max_transaction_amount` | 183.4628 | 170.0282 | -7.32% | False |

## Prediction Monitoring Summary

### Fraud

- Rows monitored: 100
- High-risk count: 1
- Risk band distribution: {'High': 1, 'Low': 25, 'Medium': 74}

### Churn

- Rows monitored: 100
- High-risk count: 2
- Risk band distribution: {'High': 2, 'Low': 62, 'Medium': 36}

### Anomaly

- Rows monitored: 500
- High-risk count: 21
- Risk band distribution: {'High': 21, 'Low': 333, 'Medium': 146}

## Overall Prediction Health

- Total high-risk count: 24
- High-risk volume threshold: 50
- Status: PASS
