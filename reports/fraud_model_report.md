# Fraud Model Report

This report summarizes the baseline local fraud detection model trained on the processed synthetic feature dataset.

## Model Summary

- Model: `RandomForestClassifier`
- Rows used: 500
- Train rows: 400
- Test rows: 100
- Positive fraud class rate: 19.4%
- Feature count: 24

## Evaluation Metrics

- Precision: 0.2381
- Recall: 0.2632
- F1: 0.2500
- ROC-AUC: 0.6355

## Confusion Matrix

| Metric | Count |
| --- | ---: |
| True negatives | 65 |
| False positives | 16 |
| False negatives | 14 |
| True positives | 5 |

## Top Feature Importances

| Feature | Importance |
| --- | ---: |
| `failed_transaction_count` | 0.106428 |
| `total_transaction_amount` | 0.092553 |
| `activity_decline_score` | 0.079852 |
| `average_transaction_amount` | 0.078071 |
| `engagement_risk_score` | 0.069774 |
| `max_transaction_amount` | 0.067119 |
| `support_risk_score` | 0.065860 |
| `account_age_days` | 0.064472 |
| `transaction_count` | 0.059489 |
| `average_resolution_time_hours` | 0.058181 |

## Interpretation

- Recall matters because missed fraud cases can create direct financial, operational, and customer trust risk.
- Precision matters because too many false positives can create unnecessary review work and customer friction.
- This is a baseline model on synthetic data only, so metrics should be treated as workflow evidence rather than production performance.
- Target columns and obvious outcome/proxy leakage fields are excluded from training.
- No AWS services are used in this milestone.
