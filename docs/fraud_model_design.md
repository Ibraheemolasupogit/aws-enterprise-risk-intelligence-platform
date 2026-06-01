# Fraud Model Design

## Fraud Modelling Objective

The objective is to train a lightweight baseline classifier that estimates whether a synthetic customer is associated with fraud risk. This milestone demonstrates the local modeling workflow, evaluation discipline, prediction output format, and evidence reporting before any AWS implementation.

## Target Variable

The target variable is `fraud_label` from `data/processed/ml_feature_dataset.csv`. It is a synthetic binary indicator where `1` represents a customer with fraud signal and `0` represents no fraud signal.

## Feature Groups Used

The baseline model uses numeric, model-ready features from the processed feature dataset:

- Customer profile features.
- Transaction aggregation features.
- Support activity features.
- Behavioral engagement features.
- Experiment/intervention assignment features where they are numeric and available.

Target columns and obvious outcome/proxy leakage fields are excluded from training, including `fraud_label`, `churn_label`, `anomaly_label`, `conversion_flag`, `retention_flag`, and `transaction_risk_score`.

## Chosen Baseline Model

The baseline model is `RandomForestClassifier` with modest depth and balanced class weights. It is simple to run locally, handles non-linear relationships, requires minimal preprocessing for numeric features, and provides feature importance values for a portfolio-ready explanation.

## Evaluation Metrics

The model is evaluated with:

- Precision.
- Recall.
- F1.
- ROC-AUC.
- Confusion matrix.

The prediction output also includes fraud probabilities and simple Low, Medium, and High risk bands.

## Why Recall Matters For Fraud

Recall measures how many actual fraud cases the model catches. In fraud detection, missed fraud can lead to financial loss, operational risk, and customer trust issues. A low-recall model may look quiet, but it can leave important fraud signals undetected.

## Why Precision Also Matters

Precision measures how many predicted fraud cases are actually fraud. Precision matters because false positives can create unnecessary manual review, customer friction, and alert fatigue. A usable fraud workflow needs to balance detection coverage with operational efficiency.

## Limitations Of The Baseline Model

- The data is synthetic and should not be interpreted as real fraud behavior.
- The model is a baseline, not an optimized production model.
- No hyperparameter tuning is performed in this milestone.
- No model persistence or registry is implemented yet.
- No threshold optimization, cost-sensitive evaluation, or manual review simulation is included yet.
- Feature importance is directional evidence, not causal explanation.

## Future AWS SageMaker Training Job Mapping

This local workflow can later map to an Amazon SageMaker training job:

- `data/processed/ml_feature_dataset.csv` can be stored in Amazon S3.
- `src/risk_platform/fraud/fraud_model.py` can become the training entry point.
- Metrics can be emitted to SageMaker Experiments or CloudWatch.
- Model artifacts can be registered in SageMaker Model Registry.
- Batch predictions can later map to SageMaker Batch Transform.

This milestone does not connect to AWS or create SageMaker resources.
