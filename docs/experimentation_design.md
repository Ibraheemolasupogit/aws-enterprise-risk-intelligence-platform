# Experimentation Design

## Why Experimentation Matters

Experimentation helps risk, product, and operations teams understand whether an intervention changed outcomes. In enterprise risk intelligence, this can include evaluating retention actions, fraud review strategies, customer support interventions, or model replacement decisions.

## A/B Testing Simulation Objective

The A/B testing workflow compares synthetic treatment and control groups using `conversion_flag` and `retention_flag`. It estimates group sizes, outcome rates, absolute lift, relative lift, and p-values for outcome differences.

## Treatment/Control Comparison Logic

Treatment records use `experiment_group_encoded = 1`; control records use `experiment_group_encoded = 0`. The workflow calculates treatment and control rates for conversion and retention, then compares the differences.

## Statistical Significance Testing Logic

The milestone uses a local two-proportion z-test for binary outcomes. The test compares whether treatment and control rates differ more than expected by random variation. P-values are evidence, not automatic business decisions.

## Pre/Post Intervention Analysis Logic

The pre/post workflow compares records with `pre_post_period_encoded = 0` against records with `pre_post_period_encoded = 1`. It calculates conversion and retention rates before and after the simulated intervention and reports lift plus p-values.

## Champion Vs Challenger Evaluation Logic

The Champion vs Challenger workflow reads existing fraud and churn model metrics, simulates deterministic challenger metrics, and selects a winner using:

1. Primary metric: ROC-AUC.
2. Secondary metric: recall.

No models are retrained in this milestone.

## Production ML Experimentation Mapping

In production, these workflows could map to:

- Experiment tracking in SageMaker Experiments.
- Model approval decisions in SageMaker Model Registry.
- Batch evaluation jobs in SageMaker Processing.
- Business impact reports in S3, Redshift, or dashboards.
- Operational review gates before model promotion.

## Amazon-Style Data Scientist Relevance

This milestone mirrors common Amazon-style data scientist work: measuring treatment effects, communicating practical and statistical significance, comparing model candidates, and making decision recommendations from imperfect data.

## Limitations Of Simulated Experiments

- The data is synthetic and does not prove real causal impact.
- Treatment assignment and outcomes are generated locally.
- P-values assume simple independent binary outcomes.
- Champion metrics are real local outputs, but challenger metrics are deterministic simulations.
- No production experiment platform or AWS service is used.
