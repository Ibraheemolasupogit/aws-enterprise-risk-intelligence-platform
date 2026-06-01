# AWS Enterprise Risk Intelligence Platform

Local, synthetic-data Enterprise Risk Intelligence Platform demonstrating data science, ML engineering, experimentation, monitoring, inference, and AWS architecture thinking.

## Business Problem

Enterprise risk teams need to detect fraud signals, predict churn, identify anomalies, explain unusual behavior, evaluate interventions, compare model candidates, monitor model health, and turn scores into operational actions. This repo simulates that workflow locally with synthetic data only.

## Architecture Overview

The project is organized as a modular Python package under `src/risk_platform`:

- `ingestion`: synthetic data generation.
- `validation`: data quality checks and validation reports.
- `features`: ML-ready feature engineering.
- `fraud`, `churn`, `anomaly`: baseline risk modeling workflows.
- `experimentation`: A/B testing, pre/post analysis, and Champion vs Challenger comparison.
- `monitoring`: drift, prediction, and model health monitoring.
- `inference`: batch scoring and real-time response simulation.
- `reporting`: EDA and evidence reports.

No AWS services are called. The structure is designed for later mapping to S3, Glue, Redshift, SageMaker, Feature Store, Model Registry, Batch Transform, Endpoints, Lambda, API Gateway, Kinesis, CloudWatch, ECR, and IAM.

## Milestone Summary

1. Repo foundation, package structure, configs, CI.
2. Benchmarking and evidence framework.
3. Synthetic customer, transaction, support, behavior, label, and experiment data.
4. Data validation and EDA evidence.
5. ML-ready feature engineering.
6. Baseline fraud classifier.
7. Baseline churn classifier with lift analysis.
8. Anomaly detection and root-cause analysis.
9. A/B testing, pre/post analysis, and Champion vs Challenger evaluation.
10. Monitoring and drift detection.
11. Batch inference and real-time inference simulation.
12. Portfolio readiness documentation and AWS architecture narrative.

## Key Capabilities

- Synthetic data generation with documented schema and limitations.
- Data quality validation and EDA reports.
- Feature engineering for customer, transaction, support, behavioral, and experiment signals.
- Fraud and churn classification baselines using `RandomForestClassifier`.
- Anomaly detection with `IsolationForest` and root-cause style explanations.
- A/B testing simulation with two-proportion z-tests.
- Pre/post intervention analysis.
- Champion vs Challenger model comparison.
- Data drift, prediction monitoring, and model health reporting.
- Batch risk scoring and JSON-style real-time inference simulation.

## Generated Artifacts

Important artifacts include:

- `data/sample/*.csv`
- `data/processed/ml_feature_dataset.csv`
- `outputs/*metrics.json`
- `outputs/*predictions.csv`
- `outputs/anomaly_scores.csv`
- `outputs/batch_risk_scores.csv`
- `outputs/realtime_scoring_responses.json`
- `reports/*.md`
- `docs/evidence_index.md`
- `docs/aws_architecture_summary.md`
- `reports/final_project_report.md`

See `docs/evidence_index.md` for the full artifact map.

## How To Run Locally

```bash
python3 -m pip install -r requirements.txt
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
| Local data files | Amazon S3 |
| Ingestion and validation | AWS Glue, Lambda, Kinesis |
| Processed analytics layer | Amazon Redshift |
| Feature engineering | SageMaker Feature Store |
| Training workflows | Amazon SageMaker Training Jobs |
| Pipeline orchestration | SageMaker Pipelines |
| Experiment tracking | SageMaker Experiments |
| Champion vs Challenger | SageMaker Model Registry |
| Batch inference | SageMaker Batch Transform |
| Real-time inference | SageMaker Endpoints, Lambda, API Gateway |
| Monitoring | CloudWatch, SageMaker Model Monitor |
| Containers and access control | Amazon ECR, AWS IAM |

## Final Definition Of Done

- [x] Synthetic/local data only.
- [x] Modular, tested Python package.
- [x] Validation, EDA, feature engineering, modeling, experimentation, monitoring, and inference workflows.
- [x] Fraud, churn, anomaly, A/B testing, pre/post, and Champion vs Challenger examples.
- [x] Evidence artifacts for each major milestone.
- [x] AWS service mapping and architecture narrative.
- [x] Portfolio-ready final report and interview talking points.

## Portfolio Positioning

This repo is designed for Data Scientist, ML Engineer, and Applied Scientist conversations. It shows practical modeling, experimentation, monitoring, MLOps, and AWS architecture judgment without requiring real customer data or cloud spend.
