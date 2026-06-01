# AWS Architecture Summary

This project runs locally today and does not connect to AWS. The structure is intentionally designed so each local capability can map to a future AWS implementation without changing the core project narrative.

## Local-To-AWS Architecture Mapping

| Local Layer | Future AWS Services |
| --- | --- |
| Synthetic/local data files | Amazon S3 |
| Ingestion scripts | AWS Glue, AWS Lambda, Amazon Kinesis |
| Validation and processing | AWS Glue, SageMaker Processing |
| Feature engineering | SageMaker Feature Store |
| Fraud/churn/anomaly training | Amazon SageMaker Training Jobs |
| Workflow orchestration | SageMaker Pipelines |
| Experiment comparison | SageMaker Experiments |
| Champion vs Challenger | SageMaker Model Registry |
| Batch scoring | SageMaker Batch Transform |
| Real-time scoring | SageMaker Endpoints, AWS Lambda, Amazon API Gateway |
| Monitoring | Amazon CloudWatch, SageMaker Model Monitor |
| Container packaging | Amazon ECR |
| Access control | AWS IAM |
| Reporting | Amazon S3, Amazon Redshift, dashboards |

## Data Ingestion Layer

The local synthetic generator produces customer, transaction, support, behavior, risk label, experiment, and intervention fields. In AWS, scheduled or event-driven ingestion could use AWS Glue for batch sources, Lambda for lightweight transformations, and Kinesis for streaming transaction or event data.

## Data Storage Layer

Local `data/sample` and `data/processed` folders map to Amazon S3. Raw, processed, and curated zones would separate source records, validated datasets, and ML-ready features. Amazon Redshift could serve analytical reporting and business intelligence use cases.

## Data Processing And Validation Layer

The validation layer checks schema, missingness, duplicates, numeric ranges, label validity, experiment groups, and pre/post periods. In AWS, these checks could run as Glue jobs, Glue Data Quality rules, or SageMaker Processing jobs.

## Feature Engineering And Feature Store Layer

The local feature builder creates customer, transaction, support, behavioral, experimentation, and target groups. In AWS, stable feature definitions could be registered in SageMaker Feature Store with `customer_id` as a record identifier and S3 as the offline store.

## Model Training Layer

The fraud and churn baselines use local scikit-learn workflows. In AWS, these can map to SageMaker Training Jobs with source data in S3, containerized training code in ECR, and metrics emitted for review.

## Experimentation Layer

Local A/B testing, pre/post analysis, and statistical testing map to SageMaker Experiments for run tracking and Amazon S3 or Redshift for experiment result storage.

## Model Registry And Champion/Challenger Layer

The local Champion vs Challenger comparison simulates model promotion decisioning. In production, approved models and evaluation metadata would be stored in SageMaker Model Registry, with SageMaker Pipelines enforcing promotion gates.

## Batch Inference Layer

Local batch scoring outputs map to SageMaker Batch Transform. Batch outputs could be written to S3 and later loaded into Redshift or dashboards for risk operations review.

## Real-Time Inference Layer

The JSON-style real-time simulator maps to SageMaker Endpoints for model scoring, Lambda for decision orchestration, and API Gateway for controlled request/response access.

## Monitoring And Drift Detection Layer

Local drift, prediction, and model health reports map to SageMaker Model Monitor and CloudWatch. CloudWatch metrics and alarms could track drift flags, high-risk volumes, latency, error rates, and degraded model metrics.

## Reporting And Evidence Layer

Local Markdown reports and JSON/CSV artifacts map to S3-backed reporting. Redshift and dashboards could support stakeholder-facing summaries, audit views, and model governance reporting.

## Security And IAM Considerations

Future production work should apply least-privilege IAM roles for ingestion, processing, training, inference, monitoring, and reporting. S3 buckets should use encryption, access policies, and environment separation. Model registry approval permissions should be limited to authorized reviewers.

## Cost-Control Considerations

The project is local to avoid cost. A future AWS version should start with small datasets, scheduled jobs rather than always-on resources, right-sized training instances, Batch Transform for non-real-time scoring, endpoint autoscaling, lifecycle policies for S3, and CloudWatch budget alerts.

## Future Productionisation Roadmap

1. Move synthetic data and generated artifacts to S3.
2. Run validation and feature jobs with Glue or SageMaker Processing.
3. Register feature definitions in SageMaker Feature Store.
4. Package training code and run SageMaker Training Jobs.
5. Track experiments in SageMaker Experiments.
6. Register approved models in SageMaker Model Registry.
7. Add SageMaker Pipelines for orchestration and approval gates.
8. Add Batch Transform and endpoint-based scoring paths.
9. Add CloudWatch and SageMaker Model Monitor.
10. Add IAM policies, cost controls, and deployment automation.
