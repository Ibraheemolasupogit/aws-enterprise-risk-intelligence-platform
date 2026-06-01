# Evidence Index

This index lists the major artifacts created across the AWS Enterprise Risk Intelligence Platform. Each artifact is local, synthetic-data-based, and designed for portfolio or interview discussion.

## Milestone 1: Repo Foundation

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `README.md` | Project goal, scope, architecture, and run instructions are documented. | Gives reviewers a fast, professional entry point. |
| `pyproject.toml` | The project is structured as a testable Python package. | Demonstrates engineering discipline and reproducibility. |
| `requirements.txt` | Core local dependencies are explicit. | Shows a lightweight, runnable stack. |
| `.github/workflows/ci.yml` | CI runs package import checks and tests. | Shows readiness for collaborative development. |
| `src/risk_platform/` | Modular source layout by platform capability. | Makes the project easier to explain as a real system. |

## Milestone 1A: Benchmarking / Evidence Framework

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `docs/benchmarks/milestone_benchmarking_framework.md` | Each milestone has evidence expectations and success criteria. | Shows outcome-oriented delivery, not just code completion. |
| `docs/benchmarks/model_benchmarking_plan.md` | Planned metrics for fraud, churn, anomaly, experimentation, and monitoring. | Shows understanding of model evaluation by use case. |
| `docs/benchmarks/aws_service_benchmark_mapping.md` | Local milestones are mapped to future AWS services. | Connects local work to cloud architecture thinking. |

## Milestone 2: Synthetic Data Generation

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/ingestion/synthetic_data_generator.py` | Synthetic customer, transaction, support, behavior, label, and experiment data can be generated reproducibly. | Avoids private data while creating realistic ML workflows. |
| `data/sample/*.csv` | Local sample datasets exist for development and review. | Lets reviewers inspect tangible inputs. |
| `docs/data_dictionary.md` | Generated columns are documented. | Shows data communication skills. |
| `docs/synthetic_data_design.md` | Design rationale and limitations are explicit. | Shows responsible use of synthetic data. |

## Milestone 3: Data Validation And EDA

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/validation/data_validator.py` | Required columns, missing values, duplicates, ranges, labels, and experiment fields are checked. | Demonstrates data quality discipline. |
| `reports/data_validation_report.md` | All generated datasets pass validation checks. | Provides milestone evidence before modeling. |
| `reports/eda_summary_report.md` | Label rates, treatment split, pre/post split, and numeric summaries are documented. | Shows exploratory analysis and dataset understanding. |

## Milestone 4: Feature Engineering

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/features/feature_builder.py` | Customer-level ML-ready features are built reproducibly. | Shows reusable feature engineering. |
| `data/processed/ml_feature_dataset.csv` | A final feature table exists for downstream workflows. | Provides a clear modeling input. |
| `outputs/feature_summary.json` | Feature groups, targets, row count, and quality checks are summarized. | Supports quick technical review. |
| `reports/feature_engineering_report.md` | Feature groups and quality notes are documented. | Makes feature design explainable. |
| `docs/feature_engineering_design.md` | Feature logic and future Feature Store mapping are explained. | Shows AWS-aware feature architecture. |

## Milestone 5: Fraud Detection Model

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/fraud/fraud_model.py` | A baseline fraud classifier can be trained and evaluated locally. | Shows supervised risk modeling capability. |
| `outputs/fraud_model_metrics.json` | Precision, recall, F1, ROC-AUC, confusion matrix, and feature importance are captured. | Gives interview-ready model evidence. |
| `outputs/fraud_predictions.csv` | Fraud probabilities and risk bands are produced. | Connects modeling to risk operations. |
| `reports/fraud_model_report.md` | Metrics and interpretation are documented. | Shows communication of model trade-offs. |
| `docs/fraud_model_design.md` | Objective, target, metrics, limitations, and SageMaker mapping are explained. | Demonstrates responsible model framing. |

## Milestone 6: Churn Prediction Model

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/churn/churn_model.py` | A baseline churn classifier can be trained and evaluated locally. | Shows retention modeling capability. |
| `outputs/churn_model_metrics.json` | Churn metrics and lift at top decile are captured. | Shows targeting-oriented evaluation. |
| `outputs/churn_predictions.csv` | Churn probabilities and risk bands are produced. | Connects ML to retention actions. |
| `reports/churn_model_report.md` | Model results and lift interpretation are documented. | Shows business framing of model outputs. |
| `docs/churn_model_design.md` | Churn objective, metrics, limitations, and SageMaker mapping are explained. | Demonstrates end-to-end model design thinking. |

## Milestone 7: Anomaly Detection And Root-Cause Analysis

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/anomaly/anomaly_detector.py` | IsolationForest anomaly scoring runs locally. | Shows unsupervised risk detection. |
| `src/risk_platform/anomaly/root_cause_analysis.py` | Anomaly drivers are explained with feature deviation logic. | Shows interpretability and investigation thinking. |
| `outputs/anomaly_scores.csv` | Customer anomaly scores, labels, risk bands, and drivers are produced. | Gives tangible anomaly review evidence. |
| `outputs/root_cause_analysis.csv` | Root-cause explanations are structured for review. | Shows movement from detection to explanation. |
| `reports/anomaly_detection_report.md` | Anomaly rate and driver distribution are documented. | Makes unsupervised outputs reviewable. |
| `reports/root_cause_analysis_report.md` | Example explanations are documented. | Supports interview storytelling. |

## Milestone 8: Experimentation, A/B Testing, And Champion Vs Challenger

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/experimentation/ab_testing.py` | Treatment/control comparisons and p-values are computed. | Shows experimentation fundamentals. |
| `src/risk_platform/experimentation/pre_post_analysis.py` | Pre/post outcome changes are measured. | Shows intervention analysis thinking. |
| `src/risk_platform/experimentation/champion_challenger.py` | Model comparison and winner decisioning are implemented. | Shows model governance awareness. |
| `outputs/ab_test_results.json` | A/B lift and significance evidence are recorded. | Supports data scientist interview discussion. |
| `outputs/pre_post_intervention_analysis.json` | Pre/post impact metrics are recorded. | Shows practical business analysis. |
| `outputs/champion_challenger_comparison.json` | Champion vs Challenger decisions are documented. | Shows model lifecycle thinking. |
| `reports/experiment_impact_report.md` | Experiment results are summarized for stakeholders. | Shows communication of statistical evidence. |
| `reports/champion_challenger_report.md` | Model comparison decisions are explained. | Shows governance and decision criteria. |

## Milestone 9: Monitoring And Drift Detection

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/monitoring/drift_monitor.py` | Feature drift indicators are calculated. | Shows post-model monitoring thinking. |
| `src/risk_platform/monitoring/prediction_monitor.py` | Prediction and risk-band distributions are summarized. | Shows operational model monitoring. |
| `src/risk_platform/monitoring/model_health.py` | Metrics are consolidated into model health status. | Shows production-minded ML governance. |
| `outputs/data_drift_report.csv` | Drift evidence is available by feature. | Supports Model Monitor mapping. |
| `outputs/prediction_monitoring_summary.json` | Prediction risk volumes are summarized. | Shows health checks on scoring outputs. |
| `outputs/model_health_summary.json` | Overall health status and actions are recorded. | Demonstrates risk-based next actions. |
| `reports/monitoring_report.md` | Drift and prediction monitoring are explained. | Shows portfolio-ready observability evidence. |
| `reports/model_health_report.md` | Model health risks and recommendations are documented. | Shows executive-friendly model governance. |

## Milestone 10: Batch Inference And Real-Time Inference Simulation

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `src/risk_platform/inference/batch_inference.py` | All customers can be scored locally for enterprise risk. | Shows batch scoring workflow design. |
| `src/risk_platform/inference/realtime_simulator.py` | JSON-style single-customer responses can be simulated. | Shows endpoint-oriented thinking. |
| `src/risk_platform/inference/risk_decisioning.py` | Risk bands, overall scores, reasons, and actions are reusable. | Connects scores to operational decisions. |
| `outputs/batch_risk_scores.csv` | Batch scores, bands, and recommended actions are produced. | Demonstrates scoring artifact readiness. |
| `outputs/realtime_scoring_responses.json` | Endpoint-style response examples are generated. | Supports deployment architecture discussion. |
| `reports/batch_inference_report.md` | Batch scoring summary is documented. | Shows workflow evidence for batch operations. |
| `reports/realtime_inference_simulation_report.md` | Real-time response simulation is documented. | Shows future endpoint readiness. |

## Milestone 11: Portfolio Readiness

| Artifact | What It Proves | Portfolio / Interview Value |
| --- | --- | --- |
| `docs/evidence_index.md` | All portfolio artifacts are indexed with purpose and value. | Helps reviewers navigate the repo quickly. |
| `docs/aws_architecture_summary.md` | Local implementation maps to a future AWS architecture. | Shows cloud architecture judgment. |
| `docs/interview_talking_points.md` | The project can be explained concisely in interviews. | Improves recruiter and interviewer readability. |
| `reports/final_project_report.md` | The full project narrative is consolidated. | Provides a final portfolio artifact. |
| `docs/portfolio_readiness_checklist.md` | Readiness is assessed across structure, artifacts, tests, and docs. | Confirms the repo is review-ready. |
