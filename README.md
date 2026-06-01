# AWS Enterprise Risk Intelligence Platform

## Project Overview

This repository is the foundation for an AWS-oriented Enterprise Risk Intelligence Platform built with synthetic and local sample data only. The project is designed to demonstrate practical Data Science, Machine Learning Engineering, experimentation, monitoring, and MLOps concepts without connecting to AWS or using paid services during the initial phases.

The platform will evolve into a modular portfolio project covering risk analytics use cases such as fraud risk, churn risk, anomaly detection, root-cause analysis, experiment evaluation, and model monitoring.

## Business Problem

Enterprise risk teams need reliable ways to detect emerging risk signals, evaluate business interventions, monitor model performance, and explain changes in customer, transaction, or operational behavior. In production, these workflows often span data ingestion, feature engineering, model training, batch or real-time inference, experimentation, reporting, and governance.

This project simulates that environment locally so the architecture, analytics thinking, and engineering practices can be demonstrated safely before mapping the design to AWS services.

## Why This Project Matters

The project shows how risk intelligence capabilities can be built as testable, modular workflows rather than isolated notebooks. It is intended to demonstrate:

- Synthetic data generation and local data processing.
- Reusable feature engineering and validation patterns.
- Baseline machine learning workflows for fraud, churn, and anomaly detection.
- Experimentation workflows including A/B testing simulation and statistical analysis.
- Champion vs Challenger evaluation for model comparison.
- Monitoring concepts for data quality, model drift, and business KPIs.
- Clear mapping from local components to future AWS services.

## MVP Scope

The initial MVP should stay intentionally small and local:

- Generate or load synthetic sample datasets.
- Validate schemas and basic data quality rules.
- Build preprocessing and feature engineering utilities.
- Train baseline fraud, churn, and anomaly detection models.
- Evaluate models with simple metrics and reproducible reports.
- Simulate batch inference locally.
- Produce lightweight monitoring outputs and summary reports.
- Run unit tests and CI checks.

## Extended Scope

Future iterations may include:

- A/B testing simulation for synthetic interventions.
- Champion vs Challenger model comparison.
- Experiment impact analysis across risk, conversion, retention, or operational KPIs.
- Pre/post intervention analysis.
- Statistical significance testing for experiment and intervention results.
- Root-cause analysis for anomalies and metric shifts.
- Drift detection for features, predictions, and business metrics.
- Model cards, experiment tracking summaries, and governance reports.
- Local pipeline orchestration that can later map to SageMaker Pipelines or similar AWS-native workflows.
- Containerization and deployment simulation without paid infrastructure.

## Main Modules

- `ingestion`: Local synthetic data loading and future ingestion abstractions.
- `validation`: Schema checks, quality checks, and dataset validation utilities.
- `preprocessing`: Cleaning, encoding, scaling, splitting, and transformation helpers.
- `features`: Feature engineering logic shared across use cases.
- `fraud`: Fraud risk modeling workflows and domain-specific utilities.
- `churn`: Churn risk modeling workflows and domain-specific utilities.
- `anomaly`: Anomaly detection workflows and root-cause analysis helpers.
- `experimentation`: A/B testing simulation, experiment design, and intervention analysis.
- `evaluation`: Model metrics, Champion vs Challenger comparison, and statistical tests.
- `inference`: Local batch inference and prediction interface patterns.
- `monitoring`: Data quality, drift, model performance, and business KPI monitoring.
- `reporting`: Report generation and portfolio-ready output summaries.
- `utils`: Shared helpers for configuration, paths, logging, and reproducibility.

## Synthetic Data Layer

The repository uses realistic synthetic data to support local development before any future AWS deployment. The synthetic data layer generates customer, transaction, support, behavioral, risk label, experiment assignment, and pre/post intervention fields for fraud detection, churn prediction, anomaly detection, A/B testing simulation, and Champion vs Challenger evaluation.

Sample files can be regenerated locally with:

```bash
python -m risk_platform.ingestion.synthetic_data_generator
```

## Data Validation And EDA Layer

Milestone 3 adds lightweight data quality checks and exploratory evidence before model development begins. The validation layer checks required columns, missing values, duplicate identifiers, numeric ranges, label validity, experiment group validity, treatment/control balance, and pre/post period values. The reporting layer writes local Markdown evidence reports for validation and EDA.

```bash
python -m risk_platform.validation.validation_report
python -m risk_platform.reporting.eda_report
```

## Feature Engineering Layer

Milestone 4 creates ML-ready features from synthetic customer, transaction, support, behavioral, and experimentation data. The feature builder produces a reusable customer-level feature table, a JSON feature summary, and a Markdown evidence report before any model training begins.

```bash
python -m risk_platform.features.feature_builder
```

## Fraud Detection Model

Milestone 5 trains a baseline fraud classifier using the processed synthetic feature dataset. The workflow produces model metrics, fraud predictions, probability-based risk bands, and a portfolio-ready evaluation report while staying fully local.

```bash
python -m risk_platform.fraud.fraud_model
```

## Churn Prediction Model

Milestone 6 trains a baseline churn classifier using the processed synthetic feature dataset. The workflow produces model metrics, churn predictions, churn risk bands, lift analysis, and a portfolio-ready evaluation report while staying fully local.

```bash
python -m risk_platform.churn.churn_model
```

## Anomaly Detection And Root-Cause Analysis

Milestone 7 detects unusual customer risk patterns using the processed synthetic feature dataset and produces interpretable root-cause style evidence. The workflow generates anomaly scores, risk bands, likely top drivers, and investigation-ready reports while staying fully local.

```bash
python -m risk_platform.anomaly.anomaly_detector
```

## Experimentation, A/B Testing, And Champion Vs Challenger Evaluation

Milestone 8 simulates treatment/control analysis, pre/post intervention analysis, statistical significance testing, experiment impact reporting, and Champion vs Challenger model comparison evidence. It uses local synthetic outcomes and existing model metrics without retraining models or connecting to AWS.

```bash
python -m risk_platform.experimentation.experiment_runner
```

## Monitoring And Drift Detection

Milestone 9 creates local monitoring evidence for data drift, prediction drift, risk distribution, and model health before any future AWS deployment. The monitoring runner writes drift outputs, prediction summaries, consolidated health status, and portfolio-ready monitoring reports.

```bash
python -m risk_platform.monitoring.monitoring_runner
```

## Batch Inference And Real-Time Inference Simulation

Milestone 10 creates local scoring workflows before future AWS deployment. Batch inference scores all customers for fraud, churn, anomaly, and overall enterprise risk, while the real-time simulator creates JSON-style single-customer scoring responses.

```bash
python -m risk_platform.inference.inference_runner
```

## AWS Service Mapping

This project does not connect to AWS yet. The folder and module structure is designed so local components can later map to AWS services:

| Local Component | Future AWS Mapping |
| --- | --- |
| `data/raw`, `data/processed`, `data/sample` | Amazon S3 |
| `ingestion` | AWS Glue, AWS Lambda, Amazon Kinesis |
| `validation` | AWS Glue Data Quality, custom validation jobs |
| `features` | Amazon SageMaker Feature Store |
| `fraud`, `churn`, `anomaly` | Amazon SageMaker training jobs |
| `experimentation` | SageMaker Experiments, custom experiment analysis |
| `evaluation` | SageMaker Model Registry evaluation gates |
| `inference` | SageMaker endpoints, batch transform, AWS Lambda |
| `monitoring` | Amazon CloudWatch, SageMaker Model Monitor |
| `outputs`, `reports` | Amazon S3, Amazon Redshift, dashboards |
| CI workflow | GitHub Actions, future AWS deployment checks |
| Containerization later | Amazon ECR |
| Access control later | AWS IAM |

## Expected Outputs

- Synthetic datasets for risk intelligence workflows.
- Cleaned and processed local datasets.
- Exploratory notebooks.
- Baseline model artifacts or serialized outputs.
- Evaluation reports and metric summaries.
- Experiment analysis outputs.
- Monitoring summaries for drift, quality, and business KPIs.
- Documentation explaining architecture and results.

## Milestones

1. Create repository foundation, package structure, configuration files, and CI.
2. Add synthetic data generation and sample datasets.
3. Add validation and preprocessing utilities.
4. Build baseline fraud, churn, and anomaly models.
5. Add evaluation reports and Champion vs Challenger comparison.
6. Add A/B testing simulation and statistical significance testing.
7. Add pre/post intervention and experiment impact analysis.
8. Add monitoring summaries for drift and business metrics.
9. Document AWS architecture mapping and future deployment design.

## Milestone Benchmarking And Evidence

Each milestone will produce measurable evidence artifacts, not just code. Evidence may include validation reports, metric tables, model comparison summaries, experiment analysis outputs, monitoring reports, configuration snapshots, or architecture mapping documents.

The benchmark documents in `docs/benchmarks/` define how milestone quality will be assessed across local development, model evaluation, experimentation, monitoring, and future AWS service mapping. This keeps the project portfolio-ready and helps reviewers understand what was built, how it was evaluated, and why the result matters.

## Definition Of Done

The project is considered complete when it includes:

- Fully synthetic/local data workflows with no AWS dependency.
- Modular, tested Python package structure.
- Reproducible data generation, preprocessing, training, evaluation, and inference flows.
- Fraud, churn, and anomaly detection examples.
- A/B testing simulation.
- Champion vs Challenger model comparison.
- Experiment impact analysis.
- Pre/post intervention analysis.
- Statistical significance testing.
- Monitoring examples for data quality, drift, and business KPIs.
- Milestone benchmarking framework.
- Model benchmarking plan.
- AWS service benchmark mapping.
- Evidence artifacts for each major milestone.
- Clear reports and documentation suitable for a portfolio review.
- Explicit AWS service mapping for later implementation.
