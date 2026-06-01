import json
from pathlib import Path

import pandas as pd

from risk_platform.churn.churn_model import write_churn_model_artifacts


def test_churn_model_training_creates_outputs(tmp_path: Path):
    metrics_path = tmp_path / "churn_model_metrics.json"
    predictions_path = tmp_path / "churn_predictions.csv"
    report_path = tmp_path / "churn_model_report.md"

    artifacts = write_churn_model_artifacts(
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        report_path=report_path,
    )

    assert artifacts["metrics"].exists()
    assert artifacts["predictions"].exists()
    assert artifacts["report"].exists()

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    for metric in ["precision", "recall", "f1", "roc_auc", "confusion_matrix", "lift_at_top_decile"]:
        assert metric in metrics

    predictions = pd.read_csv(predictions_path)
    assert {
        "customer_id",
        "churn_label",
        "churn_prediction",
        "churn_probability",
        "churn_risk_band",
    }.issubset(predictions.columns)
    assert predictions["churn_probability"].between(0, 1).all()
    assert set(predictions["churn_risk_band"]).issubset({"Low", "Medium", "High"})

    report = report_path.read_text(encoding="utf-8")
    assert "Churn Model Report" in report
    assert "Lift at top decile" in report
