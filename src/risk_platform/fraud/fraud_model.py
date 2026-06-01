"""Train and evaluate a baseline local fraud detection model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
FRAUD_METRICS_PATH = Path("outputs/fraud_model_metrics.json")
FRAUD_PREDICTIONS_PATH = Path("outputs/fraud_predictions.csv")
FRAUD_REPORT_PATH = Path("reports/fraud_model_report.md")

TARGET_COLUMN = "fraud_label"
ID_COLUMN = "customer_id"
EXCLUDED_FEATURE_COLUMNS = {
    ID_COLUMN,
    "fraud_label",
    "churn_label",
    "anomaly_label",
    "conversion_flag",
    "retention_flag",
    "transaction_risk_score",
}


def load_feature_dataset(dataset_path: str | Path = FEATURE_DATASET_PATH) -> pd.DataFrame:
    """Load the processed ML feature dataset."""
    return pd.read_csv(dataset_path)


def select_model_features(dataset: pd.DataFrame) -> list[str]:
    """Select numeric, model-ready fraud features while avoiding target leakage."""
    numeric_columns = dataset.select_dtypes(include=["number"]).columns.tolist()
    return [column for column in numeric_columns if column not in EXCLUDED_FEATURE_COLUMNS]


def assign_risk_band(probability: float) -> str:
    """Convert fraud probability into a simple risk band."""
    if probability >= 0.60:
        return "High"
    if probability >= 0.30:
        return "Medium"
    return "Low"


def train_fraud_model(
    dataset_path: str | Path = FEATURE_DATASET_PATH,
    random_state: int = 42,
    test_size: float = 0.2,
) -> dict[str, Any]:
    """Train and evaluate a baseline fraud classifier."""
    dataset = load_feature_dataset(dataset_path)
    feature_columns = select_model_features(dataset)

    x = dataset[feature_columns]
    y = dataset[TARGET_COLUMN]

    x_train, x_test, y_train, y_test, train_index, test_index = train_test_split(
        x,
        y,
        dataset.index,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=random_state,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    confusion = confusion_matrix(y_test, predictions, labels=[0, 1])

    metrics = {
        "model_name": "RandomForestClassifier",
        "row_count": int(len(dataset)),
        "train_row_count": int(len(x_train)),
        "test_row_count": int(len(x_test)),
        "positive_class_rate": round(float(y.mean()), 4),
        "feature_count": int(len(feature_columns)),
        "features_used": feature_columns,
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "confusion_matrix": {
            "true_negative": int(confusion[0, 0]),
            "false_positive": int(confusion[0, 1]),
            "false_negative": int(confusion[1, 0]),
            "true_positive": int(confusion[1, 1]),
        },
        "feature_importance": {
            feature: round(float(importance), 6)
            for feature, importance in sorted(
                zip(feature_columns, model.feature_importances_),
                key=lambda item: item[1],
                reverse=True,
            )
        },
    }

    prediction_output = dataset.loc[test_index, [ID_COLUMN, TARGET_COLUMN]].copy()
    prediction_output["fraud_prediction"] = predictions
    prediction_output["fraud_probability"] = probabilities.round(6)
    prediction_output["risk_band"] = prediction_output["fraud_probability"].apply(assign_risk_band)
    prediction_output = prediction_output.sort_values("fraud_probability", ascending=False)

    return {
        "model": model,
        "metrics": metrics,
        "predictions": prediction_output,
    }


def build_fraud_model_report(metrics: dict[str, Any]) -> str:
    """Build a Markdown report for the fraud model."""
    confusion = metrics["confusion_matrix"]
    top_features = list(metrics["feature_importance"].items())[:10]

    lines = [
        "# Fraud Model Report",
        "",
        "This report summarizes the baseline local fraud detection model trained on the processed synthetic feature dataset.",
        "",
        "## Model Summary",
        "",
        f"- Model: `{metrics['model_name']}`",
        f"- Rows used: {metrics['row_count']}",
        f"- Train rows: {metrics['train_row_count']}",
        f"- Test rows: {metrics['test_row_count']}",
        f"- Positive fraud class rate: {metrics['positive_class_rate']:.1%}",
        f"- Feature count: {metrics['feature_count']}",
        "",
        "## Evaluation Metrics",
        "",
        f"- Precision: {metrics['precision']:.4f}",
        f"- Recall: {metrics['recall']:.4f}",
        f"- F1: {metrics['f1']:.4f}",
        f"- ROC-AUC: {metrics['roc_auc']:.4f}",
        "",
        "## Confusion Matrix",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| True negatives | {confusion['true_negative']} |",
        f"| False positives | {confusion['false_positive']} |",
        f"| False negatives | {confusion['false_negative']} |",
        f"| True positives | {confusion['true_positive']} |",
        "",
        "## Top Feature Importances",
        "",
        "| Feature | Importance |",
        "| --- | ---: |",
    ]

    for feature, importance in top_features:
        lines.append(f"| `{feature}` | {importance:.6f} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Recall matters because missed fraud cases can create direct financial, operational, and customer trust risk.",
            "- Precision matters because too many false positives can create unnecessary review work and customer friction.",
            "- This is a baseline model on synthetic data only, so metrics should be treated as workflow evidence rather than production performance.",
            "- Target columns and obvious outcome/proxy leakage fields are excluded from training.",
            "- No AWS services are used in this milestone.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_fraud_model_artifacts(
    dataset_path: str | Path = FEATURE_DATASET_PATH,
    metrics_path: str | Path = FRAUD_METRICS_PATH,
    predictions_path: str | Path = FRAUD_PREDICTIONS_PATH,
    report_path: str | Path = FRAUD_REPORT_PATH,
) -> dict[str, Path]:
    """Train the fraud model and write local evidence artifacts."""
    result = train_fraud_model(dataset_path=dataset_path)
    metrics = result["metrics"]
    predictions = result["predictions"]
    report = build_fraud_model_report(metrics)

    output_metrics = Path(metrics_path)
    output_predictions = Path(predictions_path)
    output_report = Path(report_path)
    output_metrics.parent.mkdir(parents=True, exist_ok=True)
    output_predictions.parent.mkdir(parents=True, exist_ok=True)
    output_report.parent.mkdir(parents=True, exist_ok=True)

    output_metrics.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    predictions.to_csv(output_predictions, index=False)
    output_report.write_text(report, encoding="utf-8")

    return {
        "metrics": output_metrics,
        "predictions": output_predictions,
        "report": output_report,
    }


def main() -> None:
    """CLI entry point for local fraud model training."""
    artifacts = write_fraud_model_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote fraud {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
