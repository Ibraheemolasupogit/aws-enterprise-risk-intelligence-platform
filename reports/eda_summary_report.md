# EDA Summary Report

This lightweight exploratory report summarizes the generated customer-level risk training dataset before feature engineering.

## Dataset Overview

- Source dataset: `data/sample/risk_training_dataset.csv`
- Row count: 500
- Column count: 28
- Customer segments: consumer: 305 (61.0%), enterprise: 49 (9.8%), small_business: 146 (29.2%)
- Regions: asia_pacific: 93 (18.6%), europe: 140 (28.0%), latin_america: 35 (7.0%), north_america: 232 (46.4%)

## Label And Experiment Distributions

- Fraud label distribution: 0: 403 (80.6%), 1: 97 (19.4%)
- Churn label distribution: 0: 452 (90.4%), 1: 48 (9.6%)
- Anomaly label distribution: 0: 465 (93.0%), 1: 35 (7.0%)
- Treatment/control split: control: 246 (49.2%), treatment: 254 (50.8%)
- Pre/post split: post: 273 (54.6%), pre: 227 (45.4%)

## Key Numeric Summaries

| Column | Mean | Median | Min | Max |
| --- | ---: | ---: | ---: | ---: |
| `account_age_days` | 918.01 | 910.00 | 24.00 | 1821.00 |
| `transaction_count` | 4.04 | 4.00 | 1.00 | 11.00 |
| `total_transaction_amount` | 377.21 | 244.22 | 15.07 | 3504.55 |
| `average_transaction_amount` | 93.88 | 62.12 | 12.74 | 1578.54 |
| `failed_transaction_count` | 1.80 | 1.00 | 0.00 | 7.00 |
| `support_ticket_count` | 1.22 | 1.00 | 0.00 | 5.00 |
| `average_resolution_time_hours` | 10.72 | 8.01 | 0.00 | 63.85 |
| `complaint_count` | 0.34 | 0.00 | 0.00 | 3.00 |
| `satisfaction_score` | 4.17 | 4.24 | 2.36 | 5.00 |
| `login_count_30d` | 12.25 | 12.00 | 2.00 | 23.00 |
| `days_since_last_login` | 9.47 | 8.00 | 0.50 | 40.40 |
| `session_count_30d` | 17.34 | 17.00 | 6.00 | 31.00 |
| `activity_decline_score` | 0.19 | 0.18 | 0.00 | 0.75 |
| `risk_score_proxy` | 0.15 | 0.11 | 0.01 | 0.66 |

## Short Interpretation

- Fraud appears in 19.4% of customer-level records, giving future fraud workflows a positive class while preserving class imbalance.
- Churn appears in 9.6% of records and is linked to behavioral decline, complaints, and login recency in the generator design.
- Anomalies appear in 7.0% of records, which is suitable for lightweight anomaly review and later root-cause analysis.
- Treatment assignment is 50.8% treatment, supporting local A/B testing simulation.
- The post-intervention share is 54.6%, supporting pre/post intervention analysis.
- These findings are synthetic development evidence only and should not be interpreted as real enterprise risk behavior.
