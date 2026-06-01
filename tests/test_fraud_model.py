import json
from pathlib import Path

import pandas as pd

from risk_platform.fraud.fraud_model import write_fraud_model_artifacts


def test_fraud_model_training_creates_outputs(tmp_path: Path):
    metrics_path = tmp_path / "fraud_model_metrics.json"
    predictions_path = tmp_path / "fraud_predictions.csv"
    report_path = tmp_path / "fraud_model_report.md"

    artifacts = write_fraud_model_artifacts(
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        report_path=report_path,
    )

    assert artifacts["metrics"].exists()
    assert artifacts["predictions"].exists()
    assert artifacts["report"].exists()

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    for metric in ["precision", "recall", "f1", "roc_auc", "confusion_matrix"]:
        assert metric in metrics

    predictions = pd.read_csv(predictions_path)
    assert {
        "customer_id",
        "fraud_label",
        "fraud_prediction",
        "fraud_probability",
        "risk_band",
    }.issubset(predictions.columns)
    assert predictions["fraud_probability"].between(0, 1).all()
    assert set(predictions["risk_band"]).issubset({"Low", "Medium", "High"})

    report = report_path.read_text(encoding="utf-8")
    assert "Fraud Model Report" in report
    assert "RandomForestClassifier" in report
