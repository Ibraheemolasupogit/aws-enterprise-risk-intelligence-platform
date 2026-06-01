# Churn Model Report

This report summarizes the baseline local churn prediction model trained on the processed synthetic feature dataset.

## Model Summary

- Model: `RandomForestClassifier`
- Rows used: 500
- Train rows: 400
- Test rows: 100
- Positive churn class rate: 9.6%
- Feature count: 25

## Evaluation Metrics

- Precision: 0.1667
- Recall: 0.1000
- F1: 0.1250
- ROC-AUC: 0.6333
- Lift at top decile: 2.0000

## Confusion Matrix

| Metric | Count |
| --- | ---: |
| True negatives | 85 |
| False positives | 5 |
| False negatives | 9 |
| True positives | 1 |

## Top Feature Importances

| Feature | Importance |
| --- | ---: |
| `activity_decline_score` | 0.124315 |
| `support_risk_score` | 0.086967 |
| `satisfaction_score` | 0.082669 |
| `average_resolution_time_hours` | 0.076019 |
| `days_since_last_login` | 0.075032 |
| `engagement_risk_score` | 0.069553 |
| `total_transaction_amount` | 0.064351 |
| `transaction_risk_score` | 0.055752 |
| `max_transaction_amount` | 0.044479 |
| `session_count_30d` | 0.044366 |

## Interpretation

- Recall matters because missed churners represent missed retention opportunities.
- Lift at top decile shows whether the model ranks high-risk customers better than random targeting.
- Precision matters because retention outreach has cost and can create customer fatigue if poorly targeted.
- This is a baseline model on synthetic data only, so metrics should be treated as workflow evidence rather than production performance.
- Target labels and obvious outcome proxy fields are excluded from training.
- No AWS services are used in this milestone.
