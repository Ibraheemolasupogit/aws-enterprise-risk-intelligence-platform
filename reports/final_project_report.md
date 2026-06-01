# Final Project Report

## Project Objective

The AWS Enterprise Risk Intelligence Platform demonstrates a full local ML lifecycle for enterprise risk analytics using synthetic data only. It is designed for portfolio review and future AWS mapping without connecting to paid services or deploying infrastructure.

## Business Problem

Enterprise risk teams need to detect fraud signals, predict churn, identify anomalies, explain likely drivers, evaluate interventions, compare model candidates, monitor health, and produce scoring outputs for operational decisions.

## Dataset Design

The project generates synthetic customer, transaction, support activity, behavioral activity, labels, experiment assignment, treatment/control fields, and pre/post intervention periods. The generated datasets are documented in `docs/data_dictionary.md` and `docs/synthetic_data_design.md`.

## Validation And EDA

Validation checks required columns, missing values, duplicate identifiers, numeric ranges, label values, experiment group validity, treatment/control balance, and pre/post period validity. EDA documents segment distributions, label rates, treatment split, pre/post split, and numeric summaries.

## Feature Engineering

The feature layer creates a customer-level ML-ready dataset with customer, transaction, support, behavioral, experimentation, and target columns. The final feature table has 500 rows, 31 columns, no duplicate customer IDs, and no missing values.

## Fraud Model

The fraud model uses a baseline `RandomForestClassifier`. It reports precision `0.2381`, recall `0.2632`, F1 `0.2500`, ROC-AUC `0.6355`, confusion matrix values, feature importance, fraud probabilities, and risk bands.

## Churn Model

The churn model uses a baseline `RandomForestClassifier`. It reports precision `0.1667`, recall `0.1000`, F1 `0.1250`, ROC-AUC `0.6333`, and lift at top decile `2.0`.

## Anomaly Detection

The anomaly workflow uses `IsolationForest` to flag unusual customer risk patterns. It flagged 35 customers, a `7.0%` anomaly rate.

## Root-Cause Analysis

Root-cause analysis compares anomalous records against normal-population averages and ranks the largest feature deviations. Common drivers include total transaction amount, average transaction amount, average resolution time, days since last login, and complaint count.

## A/B Testing Simulation

The A/B workflow compares treatment and control groups for conversion and retention. Treatment conversion was `22.44%`, control conversion was `21.14%`, absolute lift was `1.30%`, and the conversion p-value was `0.724302`.

## Pre/Post Intervention Analysis

The pre/post workflow compares pre and post periods for conversion and retention. Post conversion was `24.54%` versus pre conversion `18.50%`, a `6.04%` lift with p-value `0.103402`.

## Champion Vs Challenger Evaluation

The Champion vs Challenger workflow reads existing fraud and churn metrics, simulates deterministic challenger results, and selects winners using ROC-AUC first and recall second. Simulated challengers won for both fraud and churn.

## Monitoring And Drift Detection

Monitoring checks data drift, prediction distribution, high-risk volumes, and model health. No drift flags were triggered across 27 checked features. Prediction monitoring found 24 total high-risk records, below the configured warning threshold. Model health is `WARN` due to baseline metric weakness and non-significant experiment results.

## Batch Inference

Batch inference scores all customers for fraud, churn, anomaly, and overall enterprise risk. The batch output includes risk bands and recommended actions.

## Real-Time Inference Simulation

The real-time simulator creates JSON-style single-customer scoring responses with timestamp, risk scores, overall risk band, decision reason, and recommended action.

## AWS Architecture Mapping

The local architecture maps to S3, Glue, Redshift, SageMaker, SageMaker Pipelines, Feature Store, Experiments, Model Registry, Batch Transform, Endpoints, Lambda, API Gateway, Kinesis, CloudWatch, ECR, and IAM. Details are documented in `docs/aws_architecture_summary.md`.

## Final Definition Of Done Status

The project includes synthetic data workflows, validation, EDA, feature engineering, fraud and churn models, anomaly detection, root-cause analysis, A/B testing, pre/post analysis, Champion vs Challenger comparison, monitoring, inference simulation, tests, evidence artifacts, and AWS architecture mapping.

## Limitations

All data is synthetic. Model metrics are baseline workflow evidence, not production performance claims. Challenger metrics are simulated. Monitoring is local and static. No AWS resources are deployed.

## Next Steps

Potential next steps include adding persisted model artifacts, real challenger training, richer threshold tuning, model cards, pipeline orchestration, dashboard outputs, and optional AWS implementation using the documented architecture.
