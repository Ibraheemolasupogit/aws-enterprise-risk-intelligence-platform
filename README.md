# AWS Enterprise Risk Intelligence Platform

A local, synthetic-data enterprise risk intelligence platform demonstrating AWS-oriented data science delivery, machine learning workflows, experimentation, monitoring, inference, and MLOps-ready project structure.

## Project Purpose

This project simulates how an enterprise risk team could use data science and machine learning to detect risk signals, evaluate interventions, monitor model behavior, and produce scoring outputs for operational decision-making. It is intentionally built with synthetic data and local execution only, so the full workflow can be reviewed without cloud access, paid services, or sensitive data.

## Business Problem

Enterprise risk teams need reliable ways to identify fraud patterns, predict customer churn, detect unusual behavior, explain root causes, compare model candidates, monitor drift, and translate scores into recommended actions. This repository demonstrates those capabilities as a cohesive local platform rather than isolated notebooks.

## Local-Only Disclaimer

This repository does **not** connect to AWS, deploy infrastructure, call paid services, or use real customer data. AWS services are represented as architecture mappings for a future implementation.

## Architecture Overview

The project is organized as a modular Python package under `src/risk_platform`:

- `ingestion`: reproducible synthetic data generation.
- `validation`: schema, quality, label, and experiment-field checks.
- `features`: ML-ready customer-level feature engineering.
- `fraud`, `churn`, `anomaly`: baseline risk modeling workflows.
- `experimentation`: A/B testing, pre/post intervention analysis, and Champion vs Challenger comparison.
- `monitoring`: data drift, prediction distribution, and model health monitoring.
- `inference`: batch scoring and real-time response simulation.
- `reporting`: EDA and evidence reporting.

Supporting architecture documentation:

- [Evidence Index](docs/evidence_index.md)
- [AWS Architecture Summary](docs/aws_architecture_summary.md)
- [Final Project Report](reports/final_project_report.md)
- [Portfolio Readiness Checklist](docs/portfolio_readiness_checklist.md)

## Core Capabilities

- Synthetic customer, transaction, support, behavioral, experiment, and intervention data.
- Data validation and exploratory analysis evidence.
- Feature engineering for fraud, churn, anomaly, and experimentation use cases.
- Baseline fraud detection with precision, recall, F1, ROC-AUC, confusion matrix, and risk bands.
- Baseline churn prediction with lift at top decile and churn risk bands.
- Anomaly detection with root-cause style driver explanations.
- A/B testing simulation with two-proportion significance testing.
- Pre/post intervention analysis.
- Champion vs Challenger model comparison.
- Monitoring for data drift, prediction distributions, high-risk volumes, and model health.
- Batch inference and JSON-style real-time inference simulation.

## Milestone Summary

1. Repository foundation, package structure, configuration, and CI.
2. Benchmarking and evidence framework.
3. Synthetic data generation.
4. Data validation and EDA.
5. Feature engineering.
6. Fraud detection baseline model.
7. Churn prediction baseline model.
8. Anomaly detection and root-cause analysis.
9. Experimentation, A/B testing, pre/post analysis, and Champion vs Challenger evaluation.
10. Monitoring and drift detection.
11. Batch inference and real-time inference simulation.
12. Portfolio readiness, evidence index, and AWS architecture narrative.

## Generated Outputs And Reports

Key generated artifacts include:

- `data/sample/*.csv`: synthetic source datasets.
- `data/processed/ml_feature_dataset.csv`: ML-ready feature table.
- `outputs/fraud_model_metrics.json` and `outputs/fraud_predictions.csv`.
- `outputs/churn_model_metrics.json` and `outputs/churn_predictions.csv`.
- `outputs/anomaly_scores.csv` and `outputs/root_cause_analysis.csv`.
- `outputs/ab_test_results.json`, `outputs/pre_post_intervention_analysis.json`, and `outputs/champion_challenger_comparison.json`.
- `outputs/data_drift_report.csv`, `outputs/prediction_monitoring_summary.json`, and `outputs/model_health_summary.json`.
- `outputs/batch_risk_scores.csv` and `outputs/realtime_scoring_responses.json`.
- `reports/*.md`: portfolio-ready evidence reports.

Selected design documents:

- [Experimentation Design](docs/experimentation_design.md)
- [Monitoring Design](docs/monitoring_design.md)
- [Inference Design](docs/inference_design.md)

## How To Run Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the local pipeline steps:

```bash
PYTHONPATH=src python3 -m risk_platform.ingestion.synthetic_data_generator
PYTHONPATH=src python3 -m risk_platform.validation.validation_report
PYTHONPATH=src python3 -m risk_platform.reporting.eda_report
PYTHONPATH=src python3 -m risk_platform.features.feature_builder
PYTHONPATH=src python3 -m risk_platform.fraud.fraud_model
PYTHONPATH=src python3 -m risk_platform.churn.churn_model
PYTHONPATH=src python3 -m risk_platform.anomaly.anomaly_detector
PYTHONPATH=src python3 -m risk_platform.experimentation.experiment_runner
PYTHONPATH=src python3 -m risk_platform.monitoring.monitoring_runner
PYTHONPATH=src python3 -m risk_platform.inference.inference_runner
```

Run tests:

```bash
python3 -m pytest
```

## AWS Service Mapping

| Local Capability | Future AWS Mapping |
| --- | --- |
| Local data storage | Amazon S3 |
| Ingestion and validation | AWS Glue, AWS Lambda, Amazon Kinesis |
| Analytical storage | Amazon Redshift |
| Feature engineering | SageMaker Feature Store |
| Model training | Amazon SageMaker Training Jobs |
| Pipeline orchestration | SageMaker Pipelines |
| Experiment tracking | SageMaker Experiments |
| Champion vs Challenger governance | SageMaker Model Registry |
| Batch inference | SageMaker Batch Transform |
| Real-time inference | SageMaker Endpoints, AWS Lambda, Amazon API Gateway |
| Monitoring and alerts | Amazon CloudWatch, SageMaker Model Monitor |
| Containers and access control | Amazon ECR, AWS IAM |

## Skills Demonstrated

- AWS-oriented data science architecture.
- Enterprise risk intelligence workflow design.
- Fraud detection, churn prediction, and anomaly detection.
- Root-cause analysis and interpretable evidence generation.
- Experimentation, A/B testing simulation, and statistical significance testing.
- Champion vs Challenger model comparison.
- Model monitoring, drift detection, and model health reporting.
- Batch inference and real-time inference simulation.
- Modular Python package design, tests, CI, and local reproducibility.

## Portfolio Positioning

This project presents a complete, local enterprise risk intelligence workflow aligned to AWS production patterns. It demonstrates how data science, ML engineering, experimentation, monitoring, inference, reporting, and cloud architecture design can fit together in a practical platform. The repository is suitable for technical review because each milestone produces evidence artifacts, documented design decisions, and runnable code.

## Future Enhancements

- Persist trained model artifacts and add model cards.
- Add threshold optimization and cost-sensitive evaluation.
- Train real challenger models instead of using simulated challenger metrics.
- Add richer causal experimentation methods.
- Add dashboard-ready outputs.
- Add optional AWS implementation with S3, Glue, SageMaker, CloudWatch, ECR, and IAM.

## Final Definition Of Done

- [x] Synthetic/local data only.
- [x] Modular, tested Python package.
- [x] Validation, EDA, feature engineering, modeling, experimentation, monitoring, and inference workflows.
- [x] Fraud, churn, anomaly, A/B testing, pre/post, and Champion vs Challenger examples.
- [x] Evidence artifacts for each major milestone.
- [x] AWS service mapping and architecture narrative.
- [x] Final project report and readiness checklist.
