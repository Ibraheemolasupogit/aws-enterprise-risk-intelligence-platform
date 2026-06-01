"""Local prediction and risk distribution monitoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


FRAUD_PREDICTIONS_PATH = Path("outputs/fraud_predictions.csv")
CHURN_PREDICTIONS_PATH = Path("outputs/churn_predictions.csv")
ANOMALY_SCORES_PATH = Path("outputs/anomaly_scores.csv")
MONITORING_CONFIG_PATH = Path("config/monitoring_config.yaml")
PREDICTION_MONITORING_OUTPUT_PATH = Path("outputs/prediction_monitoring_summary.json")


def load_monitoring_config(config_path: str | Path = MONITORING_CONFIG_PATH) -> dict[str, Any]:
    """Load local monitoring configuration."""
    return yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))


def _band_distribution(series: pd.Series) -> dict[str, int]:
    return {str(label): int(count) for label, count in series.value_counts().sort_index().items()}


def _probability_summary(series: pd.Series) -> dict[str, float]:
    return {
        "mean": round(float(series.mean()), 6),
        "min": round(float(series.min()), 6),
        "max": round(float(series.max()), 6),
        "std": round(float(series.std(ddof=0)), 6),
    }


def summarize_prediction_outputs(
    fraud_predictions_path: str | Path = FRAUD_PREDICTIONS_PATH,
    churn_predictions_path: str | Path = CHURN_PREDICTIONS_PATH,
    anomaly_scores_path: str | Path = ANOMALY_SCORES_PATH,
    config_path: str | Path = MONITORING_CONFIG_PATH,
) -> dict[str, Any]:
    """Summarize prediction distributions, risk bands, and high-risk counts."""
    config = load_monitoring_config(config_path)
    high_risk_threshold = int(config["thresholds"]["high_risk_volume_warning_threshold"])

    fraud_predictions = pd.read_csv(fraud_predictions_path)
    churn_predictions = pd.read_csv(churn_predictions_path)
    anomaly_scores = pd.read_csv(anomaly_scores_path)

    summary = {
        "fraud": {
            "row_count": int(len(fraud_predictions)),
            "probability_summary": _probability_summary(fraud_predictions["fraud_probability"]),
            "risk_band_distribution": _band_distribution(fraud_predictions["risk_band"]),
            "high_risk_count": int((fraud_predictions["risk_band"] == "High").sum()),
        },
        "churn": {
            "row_count": int(len(churn_predictions)),
            "probability_summary": _probability_summary(churn_predictions["churn_probability"]),
            "risk_band_distribution": _band_distribution(churn_predictions["churn_risk_band"]),
            "high_risk_count": int((churn_predictions["churn_risk_band"] == "High").sum()),
        },
        "anomaly": {
            "row_count": int(len(anomaly_scores)),
            "score_summary": _probability_summary(anomaly_scores["anomaly_score"]),
            "risk_band_distribution": _band_distribution(anomaly_scores["anomaly_risk_band"]),
            "high_risk_count": int((anomaly_scores["anomaly_risk_band"] == "High").sum()),
        },
    }

    total_high_risk_count = sum(section["high_risk_count"] for section in summary.values())
    summary["overall"] = {
        "total_high_risk_count": int(total_high_risk_count),
        "high_risk_volume_warning_threshold": high_risk_threshold,
        "model_health_status": "WARN" if total_high_risk_count >= high_risk_threshold else "PASS",
    }
    return summary


def write_prediction_monitoring_summary(
    output_path: str | Path = PREDICTION_MONITORING_OUTPUT_PATH,
) -> Path:
    """Write prediction monitoring summary to JSON."""
    summary = summarize_prediction_outputs()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return output
