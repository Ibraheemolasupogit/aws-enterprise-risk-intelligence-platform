"""Local batch inference workflow for enterprise risk scoring."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from risk_platform.inference.risk_decisioning import (
    calculate_overall_risk_score,
    generate_recommended_action,
    score_to_risk_band,
)


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
BATCH_SCORES_PATH = Path("outputs/batch_risk_scores.csv")
BATCH_REPORT_PATH = Path("reports/batch_inference_report.md")


def _min_max_scale(series: pd.Series) -> pd.Series:
    min_value = series.min()
    max_value = series.max()
    if max_value == min_value:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - min_value) / (max_value - min_value)


def build_batch_risk_scores(dataset_path: str | Path = FEATURE_DATASET_PATH) -> pd.DataFrame:
    """Build local batch risk scores for fraud, churn, anomaly, and overall risk."""
    dataset = pd.read_csv(dataset_path)

    fraud_risk_score = (
        0.40 * _min_max_scale(dataset["failed_transaction_count"])
        + 0.25 * dataset["high_value_transaction_flag"]
        + 0.20 * _min_max_scale(dataset["max_transaction_amount"])
        + 0.15 * dataset["transaction_risk_score"]
    ).clip(0, 1)
    churn_risk_score = (
        0.45 * dataset["engagement_risk_score"]
        + 0.30 * dataset["support_risk_score"]
        + 0.15 * dataset["activity_decline_score"]
        + 0.10 * (1 - (dataset["satisfaction_score"] / 5))
    ).clip(0, 1)
    anomaly_risk_score = (
        0.40 * _min_max_scale(dataset["total_transaction_amount"])
        + 0.25 * _min_max_scale(dataset["average_resolution_time_hours"])
        + 0.20 * _min_max_scale(dataset["failed_transaction_count"])
        + 0.15 * dataset["engagement_risk_score"]
    ).clip(0, 1)

    output = pd.DataFrame(
        {
            "customer_id": dataset["customer_id"],
            "fraud_risk_score": fraud_risk_score.round(6),
            "churn_risk_score": churn_risk_score.round(6),
            "anomaly_score": anomaly_risk_score.round(6),
        }
    )
    output["fraud_risk_band"] = output["fraud_risk_score"].apply(score_to_risk_band)
    output["churn_risk_band"] = output["churn_risk_score"].apply(score_to_risk_band)
    output["anomaly_risk_band"] = output["anomaly_score"].apply(score_to_risk_band)
    output["overall_risk_score"] = output.apply(
        lambda row: calculate_overall_risk_score(
            row["fraud_risk_score"],
            row["churn_risk_score"],
            row["anomaly_score"],
        ),
        axis=1,
    )
    output["overall_risk_band"] = output["overall_risk_score"].apply(score_to_risk_band)
    output["recommended_action"] = output.apply(
        lambda row: generate_recommended_action(
            row["fraud_risk_score"],
            row["churn_risk_score"],
            row["anomaly_score"],
            row["overall_risk_score"],
        ),
        axis=1,
    )
    return output.sort_values("overall_risk_score", ascending=False)


def build_batch_inference_report(batch_scores: pd.DataFrame) -> str:
    """Build a Markdown report for batch inference outputs."""
    lines = [
        "# Batch Inference Report",
        "",
        "This report summarizes local batch enterprise risk scoring outputs.",
        "",
        "## Summary",
        "",
        f"- Customers scored: {len(batch_scores)}",
        f"- Average overall risk score: {batch_scores['overall_risk_score'].mean():.4f}",
        f"- High overall risk customers: {(batch_scores['overall_risk_band'] == 'High').sum()}",
        f"- Medium overall risk customers: {(batch_scores['overall_risk_band'] == 'Medium').sum()}",
        f"- Low overall risk customers: {(batch_scores['overall_risk_band'] == 'Low').sum()}",
        "",
        "## Recommended Action Distribution",
        "",
    ]
    for action, count in batch_scores["recommended_action"].value_counts().items():
        lines.append(f"- {action}: {count}")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Scores are local scoring proxies built from processed synthetic features.",
            "- No deployed model, endpoint, or AWS service is used in this milestone.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_batch_inference_artifacts(
    output_path: str | Path = BATCH_SCORES_PATH,
    report_path: str | Path = BATCH_REPORT_PATH,
    dataset_path: str | Path = FEATURE_DATASET_PATH,
) -> dict[str, Path]:
    """Write batch inference CSV and report artifacts."""
    batch_scores = build_batch_risk_scores(dataset_path=dataset_path)
    output = Path(output_path)
    report = Path(report_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    batch_scores.to_csv(output, index=False)
    report.write_text(build_batch_inference_report(batch_scores), encoding="utf-8")
    return {"batch_scores": output, "batch_report": report}
