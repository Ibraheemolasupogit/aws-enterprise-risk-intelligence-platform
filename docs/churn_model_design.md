# Churn Model Design

## Churn Modelling Objective

The objective is to train a lightweight baseline classifier that estimates customer churn risk from the processed synthetic feature dataset. This milestone demonstrates a local retention modeling workflow with metrics, ranked predictions, risk bands, lift analysis, and a portfolio-ready report.

## Target Variable

The target variable is `churn_label` from `data/processed/ml_feature_dataset.csv`. It is a synthetic binary indicator where `1` represents churn and `0` represents retained customer behavior.

## Feature Groups Used

The model uses numeric, model-ready features from the processed feature dataset:

- Customer profile features.
- Transaction aggregation features.
- Support activity features.
- Behavioral engagement features.
- Numeric intervention and experiment assignment features.

The workflow excludes target labels and obvious outcome proxy fields, including `fraud_label`, `churn_label`, `anomaly_label`, `conversion_flag`, and `retention_flag`.

## Chosen Baseline Model

The baseline model is `RandomForestClassifier` with balanced class weights and modest tree depth. This model is easy to run locally, works well with numeric tabular features, supports non-linear relationships, and provides feature importance values for interpretation.

## Evaluation Metrics

The model is evaluated with:

- Precision.
- Recall.
- F1.
- ROC-AUC.
- Confusion matrix.
- Lift at top decile.

The prediction output also includes churn probabilities and Low, Medium, and High churn risk bands.

## Why Recall Matters For Churn

Recall matters because missed churners are missed retention opportunities. A retention team often wants to identify as many high-risk customers as possible before they leave, especially when the cost of outreach is acceptable.

## Why Lift Matters For Retention Targeting

Lift at top decile measures whether the highest-scored customers churn at a higher rate than the overall population. This is useful for retention targeting because teams often have limited campaign capacity and need to prioritize the most at-risk customers.

## Limitations Of The Baseline Model

- The data and labels are synthetic.
- The model is not tuned or production-ready.
- The feature set is local and static.
- No campaign cost model or treatment optimization is included yet.
- Feature importance is directional and should not be interpreted causally.
- No model registry, drift monitoring, or deployment workflow is included in this milestone.

## Future AWS SageMaker Training Job Mapping

This local workflow can later map to Amazon SageMaker:

- `data/processed/ml_feature_dataset.csv` can be stored in Amazon S3.
- `src/risk_platform/churn/churn_model.py` can become a SageMaker training entry point.
- Metrics can be tracked in SageMaker Experiments.
- Approved model artifacts can be registered in SageMaker Model Registry.
- Churn scoring can later run through SageMaker Batch Transform or an endpoint.

This milestone does not connect to AWS or create SageMaker resources.
