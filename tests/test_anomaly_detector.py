import json
from pathlib import Path

import pandas as pd

from risk_platform.anomaly.anomaly_detector import write_anomaly_artifacts


def test_anomaly_detection_creates_outputs(tmp_path: Path):
    anomaly_scores_path = tmp_path / "anomaly_scores.csv"
    anomaly_summary_path = tmp_path / "anomaly_detection_summary.json"
    anomaly_report_path = tmp_path / "anomaly_detection_report.md"
    root_cause_output_path = tmp_path / "root_cause_analysis.csv"
    root_cause_report_path = tmp_path / "root_cause_analysis_report.md"

    artifacts = write_anomaly_artifacts(
        anomaly_scores_path=anomaly_scores_path,
        anomaly_summary_path=anomaly_summary_path,
        anomaly_report_path=anomaly_report_path,
        root_cause_output_path=root_cause_output_path,
        root_cause_report_path=root_cause_report_path,
    )

    assert artifacts["anomaly_scores"].exists()
    assert artifacts["anomaly_summary"].exists()
    assert artifacts["anomaly_report"].exists()
    assert artifacts["root_cause_output"].exists()
    assert artifacts["root_cause_report"].exists()

    scores = pd.read_csv(anomaly_scores_path)
    assert {
        "customer_id",
        "anomaly_score",
        "anomaly_label",
        "anomaly_risk_band",
        "top_anomaly_driver_1",
        "top_anomaly_driver_2",
        "top_anomaly_driver_3",
    }.issubset(scores.columns)
    assert scores["anomaly_score"].between(0, 1).all()
    assert set(scores["anomaly_risk_band"]).issubset({"Low", "Medium", "High"})

    summary = json.loads(anomaly_summary_path.read_text(encoding="utf-8"))
    assert summary["model_name"] == "IsolationForest"
    assert "anomaly_rate" in summary

    root_cause = pd.read_csv(root_cause_output_path)
    assert {
        "customer_id",
        "root_cause_explanation",
        "driver_1_feature",
    }.issubset(root_cause.columns)

    assert "Anomaly Detection Report" in anomaly_report_path.read_text(encoding="utf-8")
    assert "Root-Cause Analysis Report" in root_cause_report_path.read_text(encoding="utf-8")
