"""Consolidated local model health checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


FRAUD_METRICS_PATH = Path("outputs/fraud_model_metrics.json")
CHURN_METRICS_PATH = Path("outputs/churn_model_metrics.json")
ANOMALY_SUMMARY_PATH = Path("outputs/anomaly_detection_summary.json")
AB_TEST_RESULTS_PATH = Path("outputs/ab_test_results.json")
MONITORING_CONFIG_PATH = Path("config/monitoring_config.yaml")
MODEL_HEALTH_OUTPUT_PATH = Path("outputs/model_health_summary.json")


def load_json(path: str | Path) -> dict[str, Any]:
    """Load JSON from disk."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_monitoring_config(config_path: str | Path = MONITORING_CONFIG_PATH) -> dict[str, Any]:
    """Load local monitoring configuration."""
    return yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))


def build_model_health_summary(
    fraud_metrics_path: str | Path = FRAUD_METRICS_PATH,
    churn_metrics_path: str | Path = CHURN_METRICS_PATH,
    anomaly_summary_path: str | Path = ANOMALY_SUMMARY_PATH,
    ab_test_results_path: str | Path = AB_TEST_RESULTS_PATH,
    config_path: str | Path = MONITORING_CONFIG_PATH,
) -> dict[str, Any]:
    """Build consolidated model health status from local evidence artifacts."""
    config = load_monitoring_config(config_path)
    thresholds = config["thresholds"]
    fraud_metrics = load_json(fraud_metrics_path)
    churn_metrics = load_json(churn_metrics_path)
    anomaly_summary = load_json(anomaly_summary_path)
    ab_test_results = load_json(ab_test_results_path)

    risks: list[str] = []
    recommended_actions: list[str] = []

    if fraud_metrics["roc_auc"] < thresholds["fraud_auc_warning_threshold"]:
        risks.append("fraud_auc_below_threshold")
        recommended_actions.append("Review fraud features, threshold strategy, and class imbalance handling.")
    if churn_metrics["roc_auc"] < thresholds["churn_auc_warning_threshold"]:
        risks.append("churn_auc_below_threshold")
        recommended_actions.append("Review churn engagement/support features and retention targeting logic.")
    if fraud_metrics["recall"] < thresholds["minimum_recall_threshold"]:
        risks.append("fraud_recall_below_threshold")
        recommended_actions.append("Tune fraud model or threshold to improve fraud capture.")
    if churn_metrics["recall"] < thresholds["minimum_recall_threshold"]:
        risks.append("churn_recall_below_threshold")
        recommended_actions.append("Tune churn model or threshold to improve high-risk customer capture.")
    if anomaly_summary["anomaly_rate"] > thresholds["anomaly_rate_warning_threshold"]:
        risks.append("anomaly_rate_above_threshold")
        recommended_actions.append("Review anomaly score threshold and high-risk segment concentration.")
    if ab_test_results["p_value_conversion_difference"] > thresholds["experiment_p_value_warning_threshold"]:
        risks.append("experiment_conversion_not_statistically_significant")
        recommended_actions.append("Treat experiment lift as directional until more evidence is available.")

    overall_status = "PASS" if not risks else "WARN"
    return {
        "overall_status": overall_status,
        "risks": risks,
        "recommended_next_actions": recommended_actions,
        "thresholds": thresholds,
        "fraud": {
            "roc_auc": fraud_metrics["roc_auc"],
            "precision": fraud_metrics["precision"],
            "recall": fraud_metrics["recall"],
            "f1": fraud_metrics["f1"],
            "status": "WARN"
            if fraud_metrics["roc_auc"] < thresholds["fraud_auc_warning_threshold"]
            or fraud_metrics["recall"] < thresholds["minimum_recall_threshold"]
            else "PASS",
        },
        "churn": {
            "roc_auc": churn_metrics["roc_auc"],
            "precision": churn_metrics["precision"],
            "recall": churn_metrics["recall"],
            "f1": churn_metrics["f1"],
            "lift_at_top_decile": churn_metrics["lift_at_top_decile"],
            "status": "WARN"
            if churn_metrics["roc_auc"] < thresholds["churn_auc_warning_threshold"]
            or churn_metrics["recall"] < thresholds["minimum_recall_threshold"]
            else "PASS",
        },
        "anomaly": {
            "anomaly_rate": anomaly_summary["anomaly_rate"],
            "anomaly_count": anomaly_summary["anomaly_count"],
            "status": "WARN"
            if anomaly_summary["anomaly_rate"] > thresholds["anomaly_rate_warning_threshold"]
            else "PASS",
        },
        "experimentation": {
            "conversion_absolute_lift": ab_test_results["absolute_lift"],
            "conversion_p_value": ab_test_results["p_value_conversion_difference"],
            "retention_rate_difference": ab_test_results["retention_rate_difference"],
            "retention_p_value": ab_test_results["p_value_retention_difference"],
            "status": "WARN"
            if ab_test_results["p_value_conversion_difference"] > thresholds["experiment_p_value_warning_threshold"]
            else "PASS",
        },
    }


def write_model_health_summary(
    output_path: str | Path = MODEL_HEALTH_OUTPUT_PATH,
) -> Path:
    """Write consolidated model health status to JSON."""
    summary = build_model_health_summary()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return output
