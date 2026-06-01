# Monitoring Design

## Why Monitoring Matters

Monitoring turns model outputs into operational evidence. For enterprise risk intelligence, teams need to understand whether data distributions are shifting, whether risk volumes are changing, and whether model health is strong enough for continued use.

## Data Drift Monitoring Logic

The local drift monitor splits `data/processed/ml_feature_dataset.csv` into deterministic reference and current samples. It compares numeric feature distributions using:

- Reference mean.
- Current mean.
- Mean difference.
- Percentage mean change.
- Standard deviation change.
- Drift flag based on a configurable mean-change threshold.

## Prediction Drift Monitoring Logic

Prediction monitoring loads local fraud, churn, and anomaly outputs. It summarizes probability or score distributions, risk band distributions, and high-risk customer counts.

## Model Health Monitoring Logic

Model health monitoring consolidates:

- Fraud model metrics.
- Churn model metrics.
- Anomaly detection summary.
- A/B test results.

The consolidated health output flags weak metrics and recommends follow-up actions.

## Threshold Logic

Thresholds are stored in `config/monitoring_config.yaml`. They include drift sensitivity, AUC warning levels, minimum recall, anomaly rate warning level, experiment p-value warning level, and high-risk volume warning level.

## CloudWatch And SageMaker Model Monitor Mapping

This local milestone can later map to AWS services:

- Data drift summaries can map to SageMaker Model Monitor baseline and constraint reports.
- Prediction and risk-band summaries can map to CloudWatch metrics.
- Model health status can map to CloudWatch alarms or operational dashboards.
- Reports can be stored in S3 and queried in Redshift or exposed through BI dashboards.

No AWS services are used in this milestone.

## Limitations Of Local Monitoring

- Reference and current splits are simulated from one synthetic dataset.
- Thresholds are simple defaults, not production-calibrated controls.
- Prediction monitoring uses static local outputs, not live traffic.
- Health status is a lightweight portfolio signal, not a deployment gate.
- No automated alerting or incident workflow exists yet.
