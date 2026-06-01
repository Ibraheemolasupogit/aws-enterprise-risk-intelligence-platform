# Milestone Benchmarking Framework

This framework defines how each project milestone will be evaluated. The goal is to make progress measurable through evidence artifacts, not just completed code. Each milestone should leave behind a clear result that can be reviewed in a portfolio, technical interview, or architecture walkthrough.

## Repo Foundation

- Goal: Establish a modular, testable, AWS-oriented local project structure.
- Evidence artifact: Repository tree, README, configs, package structure, CI workflow, and smoke tests.
- Success criteria: Project imports successfully, CI runs, folders map cleanly to future platform capabilities.
- Example metric or quality check: `pytest` passes and `import risk_platform` succeeds.
- Portfolio value: Shows engineering discipline before modeling work begins.

## Synthetic Data Generation

- Goal: Create realistic local synthetic datasets for fraud, churn, anomaly, and experimentation use cases.
- Evidence artifact: Data generation script, data dictionary, and small sample CSV files.
- Success criteria: Datasets are reproducible, documented, and contain meaningful target or outcome columns.
- Example metric or quality check: Row counts, target distribution checks, and random seed reproducibility.
- Portfolio value: Demonstrates safe data simulation without customer or proprietary data.

## Data Validation

- Goal: Validate schema, missingness, ranges, duplicates, and target integrity before downstream use.
- Evidence artifact: Validation module, validation report, EDA summary, and tests for expected failures.
- Expected evidence artifacts: `reports/data_validation_report.md`, `reports/eda_summary_report.md`.
- Success criteria: Invalid records are flagged clearly and validation results are reproducible.
- Example metric or quality check: Missing value rate, duplicate rate, schema pass/fail status.
- Portfolio value: Shows production-minded data quality thinking.

## Feature Engineering

- Goal: Build reusable feature transformations for risk, churn, anomaly, and experimentation workflows.
- Evidence artifact: Feature engineering module, feature list, and transformation tests.
- Expected evidence artifacts: `data/processed/ml_feature_dataset.csv`, `outputs/feature_summary.json`, `reports/feature_engineering_report.md`, `docs/feature_engineering_design.md`.
- Success criteria: Features are deterministic, documented, and reusable across notebooks and scripts.
- Example metric or quality check: No unexpected nulls after transformation and stable feature counts.
- Portfolio value: Demonstrates ML-ready data preparation and reusable design.

## Fraud Detection Model

- Goal: Train a baseline fraud classifier on synthetic data.
- Evidence artifact: Training script, evaluation report, confusion matrix, and model summary.
- Expected evidence artifacts: `outputs/fraud_model_metrics.json`, `outputs/fraud_predictions.csv`, `reports/fraud_model_report.md`, `docs/fraud_model_design.md`.
- Success criteria: Baseline model runs end to end and reports precision, recall, F1, and ROC-AUC.
- Example metric or quality check: Recall and precision are reported with class imbalance noted.
- Portfolio value: Shows applied classification skills for a common enterprise risk use case.

## Churn Prediction Model

- Goal: Train a baseline churn classifier on synthetic customer behavior data.
- Evidence artifact: Training script, lift analysis, evaluation report, and model summary.
- Expected evidence artifacts: `outputs/churn_model_metrics.json`, `outputs/churn_predictions.csv`, `reports/churn_model_report.md`, `docs/churn_model_design.md`.
- Success criteria: Baseline model reports precision, recall, F1, ROC-AUC, and lift.
- Example metric or quality check: Lift at top decile is calculated and explained.
- Portfolio value: Connects ML outputs to business retention decisions.

## Anomaly Detection

- Goal: Detect unusual records or periods in synthetic operational or transaction data.
- Evidence artifact: Anomaly detection script, anomaly score output, and summary report.
- Expected evidence artifacts: `outputs/anomaly_scores.csv`, `outputs/anomaly_detection_summary.json`, `outputs/root_cause_analysis.csv`, `reports/anomaly_detection_report.md`, `reports/root_cause_analysis_report.md`, `docs/anomaly_detection_design.md`.
- Success criteria: Anomaly rates and top suspicious records are explainable.
- Example metric or quality check: Anomaly rate remains within expected configured threshold.
- Portfolio value: Demonstrates unsupervised risk monitoring concepts.

## Root-Cause Analysis

- Goal: Explain potential drivers behind anomalies, metric shifts, or performance changes.
- Evidence artifact: Root-cause analysis report and ranked driver table.
- Success criteria: Top drivers are interpretable and linked to measurable changes.
- Example metric or quality check: Driver ranking includes feature shift magnitude or segment contribution.
- Portfolio value: Shows ability to move from detection to business explanation.

## Experiment Tracking

- Goal: Track local experiment runs, configurations, metrics, and outputs.
- Evidence artifact: Experiment log file, run summary table, and configuration snapshot.
- Success criteria: Runs are comparable and reproducible from recorded parameters.
- Example metric or quality check: Each run has a timestamp, config, metric set, and artifact reference.
- Portfolio value: Demonstrates MLOps and experimentation hygiene without paid tooling.

## Hyperparameter Tuning

- Goal: Compare simple model configurations without over-engineering.
- Evidence artifact: Tuning results table and selected baseline configuration.
- Success criteria: Search space is documented and results are reproducible.
- Example metric or quality check: Best configuration selected using validation ROC-AUC or F1.
- Portfolio value: Shows disciplined model improvement and tradeoff evaluation.

## A/B Testing Simulation

- Goal: Simulate treatment and control outcomes for a synthetic business intervention.
- Evidence artifact: A/B testing notebook or script, effect size summary, and significance test output.
- Success criteria: Treatment/control groups, outcome metrics, and assumptions are documented.
- Example metric or quality check: Difference in means or proportions with p-value and confidence interval.
- Portfolio value: Demonstrates experimentation skills relevant to product, risk, and operations decisions.

## Champion Vs Challenger Evaluation

- Goal: Compare current baseline models against challenger alternatives.
- Evidence artifact: Champion vs Challenger comparison report and model selection rationale.
- Success criteria: Selection is based on agreed metrics and business tradeoffs.
- Example metric or quality check: Challenger must improve target metric or reduce risk without unacceptable regression.
- Portfolio value: Shows model governance and lifecycle thinking.

## Batch Inference

- Goal: Run local batch scoring over a sample dataset.
- Evidence artifact: Batch inference script and prediction output file.
- Success criteria: Predictions are generated with required IDs, timestamps, scores, and labels.
- Example metric or quality check: Output row count matches input row count.
- Portfolio value: Demonstrates operational scoring patterns used in enterprise ML.

## Real-Time Inference Simulation

- Goal: Simulate a lightweight local request/response inference flow.
- Evidence artifact: Local inference interface, sample requests, and response examples.
- Success criteria: Single-record scoring returns predictable schema and error handling.
- Example metric or quality check: Response includes model version, score, decision, and latency proxy.
- Portfolio value: Prepares the project for future API, Lambda, or SageMaker endpoint mapping.

## Monitoring And Drift Detection

- Goal: Monitor synthetic data quality, prediction distributions, model performance, and business KPIs.
- Evidence artifact: Monitoring report, drift summary, and health status output.
- Success criteria: Drift or degradation is flagged with thresholds and suggested investigation paths.
- Example metric or quality check: Population stability index, distribution shift, or performance delta.
- Portfolio value: Shows mature post-deployment ML thinking.

## AWS Architecture Mapping

- Goal: Map each local workflow to a future AWS service without connecting to AWS.
- Evidence artifact: AWS mapping config, architecture notes, and milestone-to-service benchmark mapping.
- Success criteria: Each local capability has a reasonable future AWS counterpart.
- Example metric or quality check: Mapping covers storage, ingestion, training, inference, monitoring, registry, and security.
- Portfolio value: Demonstrates cloud architecture awareness while preserving local reproducibility.

## Final Portfolio Readiness

- Goal: Package the project as a clear, reviewable portfolio artifact.
- Evidence artifact: README, docs, reports, notebooks, tests, and milestone evidence index.
- Success criteria: A reviewer can understand the business problem, technical design, results, and AWS mapping.
- Example metric or quality check: All major milestones have evidence artifacts and passing tests.
- Portfolio value: Converts the repo from code samples into a coherent enterprise ML case study.
