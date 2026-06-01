import json
from pathlib import Path

import pandas as pd

from risk_platform.monitoring.monitoring_runner import run_monitoring_artifacts


def test_monitoring_runner_creates_outputs():
    artifacts = run_monitoring_artifacts()

    assert artifacts["data_drift_report"].exists()
    assert artifacts["prediction_monitoring_summary"].exists()
    assert artifacts["model_health_summary"].exists()
    assert artifacts["monitoring_report"].exists()
    assert artifacts["model_health_report"].exists()

    drift_report = pd.read_csv(artifacts["data_drift_report"])
    assert "drift_flag" in drift_report.columns

    model_health = json.loads(artifacts["model_health_summary"].read_text(encoding="utf-8"))
    assert "overall_status" in model_health
    assert model_health["overall_status"] in {"PASS", "WARN"}
