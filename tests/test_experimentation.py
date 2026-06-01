import json
from pathlib import Path

from risk_platform.experimentation.experiment_runner import run_all_experimentation_artifacts


def test_experimentation_artifacts_are_created(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(Path.cwd())

    artifacts = run_all_experimentation_artifacts()

    assert artifacts["ab_test_results"].exists()
    assert artifacts["pre_post_results"].exists()
    assert artifacts["champion_challenger_results"].exists()
    assert artifacts["experiment_impact_report"].exists()
    assert artifacts["champion_challenger_report"].exists()

    ab_results = json.loads(artifacts["ab_test_results"].read_text(encoding="utf-8"))
    assert "absolute_lift" in ab_results
    assert "relative_lift" in ab_results
    assert "p_value_conversion_difference" in ab_results
    assert "p_value_retention_difference" in ab_results

    pre_post_results = json.loads(artifacts["pre_post_results"].read_text(encoding="utf-8"))
    assert "conversion_lift" in pre_post_results
    assert "retention_lift" in pre_post_results

    comparison_results = json.loads(artifacts["champion_challenger_results"].read_text(encoding="utf-8"))
    assert comparison_results["comparisons"]["fraud"]["selected_winner"] in {"champion", "challenger"}
    assert comparison_results["comparisons"]["churn"]["selected_winner"] in {"champion", "challenger"}
