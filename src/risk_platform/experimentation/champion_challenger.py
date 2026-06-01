"""Champion vs Challenger comparison using existing local model metrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FRAUD_METRICS_PATH = Path("outputs/fraud_model_metrics.json")
CHURN_METRICS_PATH = Path("outputs/churn_model_metrics.json")
CHAMPION_CHALLENGER_RESULTS_PATH = Path("outputs/champion_challenger_comparison.json")

METRIC_COLUMNS = ["roc_auc", "precision", "recall", "f1"]


def load_model_metrics(path: str | Path) -> dict[str, Any]:
    """Load model metric JSON."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def simulate_challenger_metrics(champion_metrics: dict[str, Any], model_type: str) -> dict[str, float]:
    """Create deterministic simulated challenger metrics without retraining."""
    adjustments = {
        "fraud": {"roc_auc": 0.018, "precision": -0.01, "recall": 0.035, "f1": 0.012},
        "churn": {"roc_auc": 0.012, "precision": 0.008, "recall": 0.020, "f1": 0.010},
    }
    model_adjustments = adjustments[model_type]
    return {
        metric: round(max(0.0, min(1.0, float(champion_metrics[metric]) + model_adjustments[metric])), 4)
        for metric in METRIC_COLUMNS
    }


def select_winner(champion_metrics: dict[str, Any], challenger_metrics: dict[str, Any]) -> str:
    """Select winner using ROC-AUC first and recall second."""
    if challenger_metrics["roc_auc"] > champion_metrics["roc_auc"]:
        return "challenger"
    if challenger_metrics["roc_auc"] < champion_metrics["roc_auc"]:
        return "champion"
    if challenger_metrics["recall"] > champion_metrics["recall"]:
        return "challenger"
    return "champion"


def compare_model_type(model_type: str, champion_metrics: dict[str, Any]) -> dict[str, Any]:
    """Compare one champion model with a simulated challenger."""
    champion_selected = {metric: round(float(champion_metrics[metric]), 4) for metric in METRIC_COLUMNS}
    challenger_metrics = simulate_challenger_metrics(champion_selected, model_type)
    winner = select_winner(champion_selected, challenger_metrics)
    return {
        "model_type": model_type,
        "primary_metric": "roc_auc",
        "secondary_metric": "recall",
        "champion": champion_selected,
        "challenger": challenger_metrics,
        "selected_winner": winner,
        "decision_reason": (
            "Selected by higher ROC-AUC, with recall as tie-breaker."
            if winner == "challenger"
            else "Champion retained by ROC-AUC and recall decision rule."
        ),
    }


def run_champion_challenger_comparison(
    fraud_metrics_path: str | Path = FRAUD_METRICS_PATH,
    churn_metrics_path: str | Path = CHURN_METRICS_PATH,
) -> dict[str, Any]:
    """Run Champion vs Challenger comparison for fraud and churn metrics."""
    fraud_metrics = load_model_metrics(fraud_metrics_path)
    churn_metrics = load_model_metrics(churn_metrics_path)
    comparisons = {
        "fraud": compare_model_type("fraud", fraud_metrics),
        "churn": compare_model_type("churn", churn_metrics),
    }
    return {
        "comparison_type": "simulated_champion_vs_challenger",
        "note": "Challenger metrics are deterministic simulations; no models are retrained in this milestone.",
        "comparisons": comparisons,
    }


def write_champion_challenger_results(
    output_path: str | Path = CHAMPION_CHALLENGER_RESULTS_PATH,
    fraud_metrics_path: str | Path = FRAUD_METRICS_PATH,
    churn_metrics_path: str | Path = CHURN_METRICS_PATH,
) -> Path:
    """Write Champion vs Challenger comparison results."""
    results = run_champion_challenger_comparison(
        fraud_metrics_path=fraud_metrics_path,
        churn_metrics_path=churn_metrics_path,
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return output
