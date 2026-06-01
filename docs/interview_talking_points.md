# Interview Talking Points

## 30-Second Project Pitch

I built a local AWS-oriented Enterprise Risk Intelligence Platform using synthetic data. It covers the end-to-end ML lifecycle: data generation, validation, feature engineering, fraud and churn models, anomaly detection, root-cause analysis, experimentation, Champion vs Challenger evaluation, monitoring, and inference simulation. It is designed to map cleanly to AWS services like S3, Glue, SageMaker, Feature Store, Model Registry, Batch Transform, Endpoints, Lambda, CloudWatch, and IAM.

## 2-Minute Technical Walkthrough

The repo starts with synthetic customer, transaction, support, behavior, experiment, and intervention data. I validate schemas and data quality, then build a customer-level ML feature table. I train baseline fraud and churn classifiers, run IsolationForest anomaly detection, and add simple root-cause explanations based on feature deviations. I then simulate A/B testing, pre/post intervention analysis, and Champion vs Challenger decisions. Finally, I produce local monitoring, drift, batch inference, and real-time scoring artifacts, all backed by tests and evidence reports.

## Business Problem Solved

Enterprise risk teams need to identify risky customers, explain unusual behavior, evaluate interventions, compare model candidates, and monitor model health. This project demonstrates those workflows safely with synthetic data.

## Why AWS Services Were Selected

S3 fits raw and processed storage. Glue supports ingestion and validation. SageMaker supports training, processing, experiments, feature storage, model registry, batch scoring, and endpoints. Lambda and API Gateway support lightweight real-time decisioning. Kinesis supports future streaming events. CloudWatch supports metrics and alerts. ECR supports container packaging. IAM controls access.

## How The Capabilities Connect

Fraud, churn, and anomaly workflows share the same validated feature table. Experimentation evaluates treatment and intervention impact. Champion vs Challenger compares model candidates. Monitoring checks drift, prediction risk volumes, and model health. Inference turns risk scores into operational actions.

## Key Metrics To Mention

- Fraud baseline: ROC-AUC `0.6355`, recall `0.2632`, precision `0.2381`.
- Churn baseline: ROC-AUC `0.6333`, lift at top decile `2.0`, recall `0.1000`.
- Anomaly detection: 35 flagged anomalies, `7.0%` anomaly rate.
- A/B test: treatment conversion `22.44%`, control conversion `21.14%`, p-value `0.724302`.
- Pre/post conversion lift: `6.04%`, p-value `0.103402`.
- Monitoring: no drift flags across 27 checked features; model health status `WARN`.
- Tests: `18 passed`.

## Trade-Offs And Limitations

The data is synthetic, so model metrics are workflow evidence rather than production claims. Models are intentionally simple baselines. Challenger results are simulated. Monitoring uses a deterministic local split, not live traffic. No AWS resources are deployed.

## Future Improvements

Add real challenger model variants, model persistence, threshold optimization, cost-sensitive fraud evaluation, richer causal experiment design, pipeline orchestration, model registry metadata, and AWS deployment automation.

## Role Alignment

For Data Scientist roles, emphasize experimentation, metrics, business framing, and statistical testing. For ML Engineer roles, emphasize modular code, CI, feature pipelines, inference, monitoring, and AWS mapping. For Applied Scientist roles, emphasize modeling assumptions, evaluation trade-offs, anomaly explanations, and limitations.
