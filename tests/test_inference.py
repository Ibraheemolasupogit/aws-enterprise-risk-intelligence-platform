import json

import pandas as pd

from risk_platform.inference.inference_runner import run_inference_artifacts


def test_inference_runner_creates_outputs():
    artifacts = run_inference_artifacts()

    assert artifacts["batch_scores"].exists()
    assert artifacts["batch_report"].exists()
    assert artifacts["realtime_responses"].exists()
    assert artifacts["realtime_report"].exists()

    batch_scores = pd.read_csv(artifacts["batch_scores"])
    assert "overall_risk_score" in batch_scores.columns
    assert "overall_risk_band" in batch_scores.columns

    realtime_responses = json.loads(artifacts["realtime_responses"].read_text(encoding="utf-8"))
    assert realtime_responses
    first_response = realtime_responses[0]
    assert "request_timestamp" in first_response
    assert "decision_reason" in first_response
    assert "recommended_action" in first_response
