# Data Dictionary

This project uses local synthetic data only. The generated files are small sample datasets intended for development, documentation, and future model workflow testing.

## `data/sample/customers.csv`

Customer profile table with one row per synthetic customer.

| Column | Description |
| --- | --- |
| `customer_id` | Stable synthetic customer identifier. |
| `signup_date` | Simulated date when the customer account was created. |
| `customer_segment` | Customer type such as consumer, small business, or enterprise. |
| `region` | Simulated customer region. |
| `account_age_days` | Number of days since signup. |
| `acquisition_channel` | Simulated channel where the customer was acquired. |

## `data/sample/transactions.csv`

Transaction-level table with multiple records per customer.

| Column | Description |
| --- | --- |
| `transaction_id` | Stable synthetic transaction identifier. |
| `customer_id` | Customer linked to the transaction. |
| `transaction_date` | Simulated transaction date. |
| `transaction_amount` | Synthetic transaction amount. |
| `transaction_type` | Transaction category such as purchase, refund, transfer, or subscription. |
| `merchant_category` | Simulated merchant category. |
| `failed_transaction_count` | Number of failed attempts associated with the transaction context. |
| `fraud_label` | Synthetic binary fraud indicator for supervised fraud modeling later. |

## `data/sample/support_activity.csv`

Customer-level support activity table.

| Column | Description |
| --- | --- |
| `customer_id` | Customer linked to support activity. |
| `support_ticket_count` | Number of recent support tickets. |
| `average_resolution_time_hours` | Average time to resolve tickets. |
| `complaint_count` | Count of complaint-like support interactions. |
| `satisfaction_score` | Simulated satisfaction score from 1 to 5. |

## `data/sample/behavioural_activity.csv`

Customer-level behavioral engagement table.

| Column | Description |
| --- | --- |
| `customer_id` | Customer linked to behavioral activity. |
| `login_count_30d` | Number of logins in the last 30 days. |
| `days_since_last_login` | Days since the customer last logged in. |
| `session_count_30d` | Number of sessions in the last 30 days. |
| `activity_decline_score` | Synthetic score from 0 to 1 indicating declining engagement. |

## `data/sample/risk_training_dataset.csv`

Customer-level joined dataset for future fraud, churn, anomaly, experimentation, and intervention analysis workflows.

| Column | Description |
| --- | --- |
| `customer_id` | Customer identifier. |
| `customer_segment` | Customer type. |
| `region` | Customer region. |
| `account_age_days` | Account age in days. |
| `transaction_count` | Number of transactions for the customer. |
| `total_transaction_amount` | Total transaction amount across generated transactions. |
| `average_transaction_amount` | Average transaction amount. |
| `failed_transaction_count` | Total failed transaction count across generated transactions. |
| `fraud_label` | Customer-level fraud indicator based on any fraudulent transaction. |
| `support_ticket_count` | Recent support ticket count. |
| `average_resolution_time_hours` | Average support resolution time. |
| `complaint_count` | Complaint count. |
| `satisfaction_score` | Simulated satisfaction score. |
| `login_count_30d` | Recent login count. |
| `days_since_last_login` | Days since last login. |
| `session_count_30d` | Recent session count. |
| `activity_decline_score` | Engagement decline score. |
| `experiment_group` | A/B testing group: control or treatment. |
| `treatment_flag` | Binary treatment assignment flag. |
| `pre_post_period` | Simulated intervention period: pre or post. |
| `intervention_exposed` | Binary flag for customers exposed to the post-period treatment. |
| `conversion_flag` | Synthetic conversion outcome for experimentation analysis. |
| `retention_flag` | Synthetic retention outcome for experimentation analysis. |
| `churn_label` | Synthetic binary churn indicator. |
| `anomaly_label` | Synthetic binary anomaly indicator. |
| `risk_score_proxy` | Lightweight proxy score combining fraud, churn, anomaly, behavior, and complaint signals. |
