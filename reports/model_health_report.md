# Model Health Report

This report consolidates local model, anomaly, and experiment health checks.

- Overall status: WARN

## Component Status

- Fraud: WARN
- Churn: WARN
- Anomaly: PASS
- Experimentation: WARN

## Risks

- `fraud_auc_below_threshold`
- `churn_auc_below_threshold`
- `churn_recall_below_threshold`
- `experiment_conversion_not_statistically_significant`

## Recommended Next Actions

- Review fraud features, threshold strategy, and class imbalance handling.
- Review churn engagement/support features and retention targeting logic.
- Tune churn model or threshold to improve high-risk customer capture.
- Treat experiment lift as directional until more evidence is available.
