# AWS Service Benchmark Mapping

This document maps local project milestones to future AWS services. The current project remains local-only, synthetic-data-only, and free to run. These mappings are design references for future architecture conversations, not active cloud integrations.

| Local Milestone Or Component | Future AWS Service Mapping | Benchmark Evidence |
| --- | --- | --- |
| Local data storage | Amazon S3 | Local `data/` folders, sample files, and data dictionary |
| Local validation scripts | AWS Glue Data Quality | Validation reports and schema checks |
| Local preprocessing scripts | AWS Glue, SageMaker Processing | Reproducible preprocessing outputs |
| Local feature engineering | SageMaker Feature Store | Feature definitions and transformation tests |
| Local fraud training scripts | SageMaker Training Jobs | Fraud model metrics and training report |
| Local churn training scripts | SageMaker Training Jobs | Churn model metrics and lift analysis |
| Local anomaly detection scripts | SageMaker Training Jobs, SageMaker Processing | Anomaly report and driver summary |
| Local root-cause analysis | SageMaker Processing, Amazon Redshift analytics | Ranked driver report and investigation summary |
| Local experiment tracking | SageMaker Experiments | Experiment run logs, configs, and metric comparisons |
| Local hyperparameter tuning | SageMaker Automatic Model Tuning | Tuning results table and selected configuration |
| Local model registry placeholder | SageMaker Model Registry | Champion model record and approval rationale |
| Champion vs Challenger comparison | SageMaker Model Registry, SageMaker Pipelines | Comparison report and promotion decision |
| Local batch inference | SageMaker Batch Transform | Batch scoring output and row-count validation |
| Local real-time simulation | SageMaker Endpoint, AWS Lambda | Request/response examples and latency proxy |
| Local monitoring reports | CloudWatch, SageMaker Model Monitor | Drift report, health status, and alert thresholds |
| Local streaming simulation | Amazon Kinesis | Simulated event stream and processing summary |
| Local reporting outputs | Amazon S3, Amazon Redshift, BI dashboards | Reports, charts, and portfolio summaries |
| Local CI checks | GitHub Actions, future deployment gates | Passing tests and package import checks |
| Future container packaging | Amazon ECR | Docker image metadata and reproducible runtime |
| Future access control design | AWS IAM | Role and permission mapping documentation |

## Review Standard

Each AWS mapping should answer three questions:

- What local evidence proves the workflow works?
- Which AWS service would own this responsibility in a managed architecture?
- What would need to change before deploying it in a real cloud environment?
