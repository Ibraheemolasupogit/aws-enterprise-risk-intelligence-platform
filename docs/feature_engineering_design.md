# Feature Engineering Design

## Purpose

The feature engineering layer transforms validated synthetic datasets into a single customer-level feature table. The output is local, reproducible, and designed for later fraud detection, churn prediction, anomaly detection, experimentation analysis, Champion vs Challenger evaluation, and pre/post intervention analysis.

No models are trained in this milestone.

## Customer Features

Customer features describe profile and lifecycle context. `account_age_days` captures maturity, while encoded segment, region, and acquisition channel fields make categorical customer attributes usable for later ML workflows.

These features can help explain risk differences by customer type, geography, and acquisition source.

## Fraud Feature Logic

Fraud-oriented features are aggregated from transaction records:

- `transaction_count`
- `average_transaction_amount`
- `max_transaction_amount`
- `total_transaction_amount`
- `failed_transaction_count`
- `high_value_transaction_flag`
- `transaction_risk_score`

The `transaction_risk_score` is a lightweight proxy based on high-value activity, failed transaction behavior, large transaction amounts, and fraud signal history. It is intended for feature readiness and EDA, not production decisioning.

## Churn Feature Logic

Churn-oriented features come from support and behavioral activity:

- Support burden and complaint patterns.
- Average resolution time.
- Satisfaction score.
- Login and session behavior.
- Days since last login.
- Activity decline.

`support_risk_score` and `engagement_risk_score` summarize customer experience and engagement risk into interpretable local features.

## Anomaly Feature Logic

Anomaly-oriented features preserve unusual behavior indicators such as high transaction value, failed transaction volume, support escalation, and engagement decline. These features can later support unsupervised anomaly detection, anomaly review, and root-cause analysis.

The feature table also retains `anomaly_label` as a synthetic benchmark target for local evaluation.

## Experimentation Feature Logic

Experimentation features are retained in the final table:

- `treatment_flag`
- `experiment_group_encoded`
- `pre_post_period_encoded`
- `intervention_exposed`
- `conversion_flag`
- `retention_flag`

These fields support A/B testing simulation, treatment/control comparisons, pre/post intervention analysis, and future Champion vs Challenger evaluation.

## Future SageMaker Feature Store Mapping

The local feature table maps naturally to a future SageMaker Feature Store design:

- `customer_id` can act as the record identifier.
- Customer, transaction, support, behavioral, and experimentation groups can become feature groups.
- The generated CSV can be replaced by offline store outputs in S3.
- Feature definitions in `config/feature_config.yaml` can become a starting point for feature registry documentation.

This milestone does not create or connect to SageMaker Feature Store.

## Limitations Of Local Feature Engineering

- Encodings are deterministic local mappings, not managed production encoders.
- Risk score features are simple proxies for development and interpretation.
- Synthetic labels and relationships are not real-world causal evidence.
- No online/offline consistency checks exist yet.
- Feature freshness, lineage, access control, and production monitoring are future concerns.
