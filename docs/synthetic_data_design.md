# Synthetic Data Design

## Why Synthetic Data Is Used

This project uses synthetic data so the repository can demonstrate enterprise risk workflows without exposing private customer data, connecting to AWS, or relying on paid services. Synthetic data keeps development local, reproducible, and safe for portfolio review.

The generated data is not intended to represent a real company. It is designed to provide realistic shapes, relationships, and labels that support future validation, feature engineering, modeling, experimentation, and monitoring milestones.

## Fraud Detection Support

Fraud detection is supported through transaction-level records with merchant categories, transaction amounts, failed transaction counts, and a synthetic `fraud_label`. Fraud probability is influenced by higher-risk merchant categories, large transaction amounts, repeated failures, and younger accounts.

This creates a usable supervised classification target while keeping the logic simple enough to explain.

## Churn Prediction Support

Churn prediction is supported through customer support and behavioral activity signals. The synthetic `churn_label` is influenced by activity decline, days since last login, complaint counts, support experience, account age, and intervention exposure.

This gives future churn modeling workflows a customer-level target and business-relevant explanatory variables.

## Anomaly Detection Support

Anomaly detection is supported by transaction volume, failed transaction behavior, and support resolution patterns. The `anomaly_label` flags customers with unusually high combined risk signals.

The label is a benchmark aid for local evaluation and review. Future anomaly workflows can also ignore the label and treat the problem as unsupervised.

## A/B Testing Simulation Support

Experimentation is supported with `experiment_group`, `treatment_flag`, `conversion_flag`, and `retention_flag`. Treatment assignment is randomized, and treatment exposure is only active for customers in the treatment group during the post-intervention period.

These fields allow future notebooks or scripts to compare treatment and control groups, estimate lift, and run statistical significance tests.

## Pre/Post Intervention Analysis Support

Pre/post intervention analysis is supported with `pre_post_period` and `intervention_exposed`. These fields make it possible to compare outcomes before and after a simulated intervention, including treatment-specific post-period effects.

Future analysis can use these columns for difference-in-differences style exploration, simple pre/post comparisons, or intervention impact summaries.

## Limitations Of Synthetic Data

- Synthetic relationships are simplified and should not be interpreted as real-world causal claims.
- Generated labels are useful for development but do not represent actual fraud, churn, or anomaly outcomes.
- Distribution choices are intentionally lightweight and may not match real enterprise data.
- Synthetic experiment effects are simulated and should be used only to demonstrate analysis workflow mechanics.
- Results from future models should be evaluated as portfolio evidence, not production performance.
