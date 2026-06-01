"""Run local monitoring and drift detection workflows."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from risk_platform.monitoring.drift_monitor import DATA_DRIFT_OUTPUT_PATH, write_data_drift_report
from risk_platform.monitoring.model_health import MODEL_HEALTH_OUTPUT_PATH, write_model_health_summary
from risk_platform.monitoring.prediction_monitor import (
    PREDICTION_MONITORING_OUTPUT_PATH,
    write_prediction_monitoring_summary,
)


MONITORING_REPORT_PATH = Path("reports/monitoring_report.md")
MODEL_HEALTH_REPORT_PATH = Path("reports/model_health_report.md")


def build_monitoring_report(drift_report: pd.DataFrame, prediction_summary: dict) -> str:
    """Build a Markdown report for data and prediction monitoring."""
    drifted_features = drift_report[drift_report["drift_flag"] == True]  # noqa: E712
    lines = [
        "# Monitoring Report",
        "",
        "This report summarizes local monitoring evidence for data drift, prediction distributions, and risk bands.",
        "",
        "## Data Drift Summary",
        "",
        f"- Features checked: {len(drift_report)}",
        f"- Features flagged for drift: {len(drifted_features)}",
        "",
        "## Top Drift Indicators",
        "",
        "| Feature | Reference Mean | Current Mean | Mean Change | Drift Flag |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for _, row in drift_report.head(10).iterrows():
        lines.append(
            f"| `{row['feature']}` | {row['reference_mean']:.4f} | {row['current_mean']:.4f} | "
            f"{row['percentage_mean_change']:.2%} | {row['drift_flag']} |"
        )

    lines.extend(["", "## Prediction Monitoring Summary", ""])
    for model_name in ["fraud", "churn", "anomaly"]:
        section = prediction_summary[model_name]
        lines.extend(
            [
                f"### {model_name.title()}",
                "",
                f"- Rows monitored: {section['row_count']}",
                f"- High-risk count: {section['high_risk_count']}",
                f"- Risk band distribution: {section['risk_band_distribution']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Overall Prediction Health",
            "",
            f"- Total high-risk count: {prediction_summary['overall']['total_high_risk_count']}",
            f"- High-risk volume threshold: {prediction_summary['overall']['high_risk_volume_warning_threshold']}",
            f"- Status: {prediction_summary['overall']['model_health_status']}",
            "",
        ]
    )
    return "\n".join(lines)


def build_model_health_report(model_health_summary: dict) -> str:
    """Build a Markdown report for consolidated model health."""
    lines = [
        "# Model Health Report",
        "",
        "This report consolidates local model, anomaly, and experiment health checks.",
        "",
        f"- Overall status: {model_health_summary['overall_status']}",
        "",
        "## Component Status",
        "",
        f"- Fraud: {model_health_summary['fraud']['status']}",
        f"- Churn: {model_health_summary['churn']['status']}",
        f"- Anomaly: {model_health_summary['anomaly']['status']}",
        f"- Experimentation: {model_health_summary['experimentation']['status']}",
        "",
        "## Risks",
        "",
    ]
    if model_health_summary["risks"]:
        for risk in model_health_summary["risks"]:
            lines.append(f"- `{risk}`")
    else:
        lines.append("- No risks flagged.")

    lines.extend(["", "## Recommended Next Actions", ""])
    if model_health_summary["recommended_next_actions"]:
        for action in model_health_summary["recommended_next_actions"]:
            lines.append(f"- {action}")
    else:
        lines.append("- Continue monitoring with current thresholds.")

    return "\n".join(lines) + "\n"


def write_text_report(path: str | Path, content: str) -> Path:
    """Write a text report."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return output


def run_monitoring_artifacts() -> dict[str, Path]:
    """Run drift, prediction, and model health monitoring."""
    drift_path = write_data_drift_report()
    prediction_path = write_prediction_monitoring_summary()
    model_health_path = write_model_health_summary()

    drift_report = pd.read_csv(DATA_DRIFT_OUTPUT_PATH)
    prediction_summary = json.loads(PREDICTION_MONITORING_OUTPUT_PATH.read_text(encoding="utf-8"))
    model_health_summary = json.loads(MODEL_HEALTH_OUTPUT_PATH.read_text(encoding="utf-8"))

    monitoring_report = write_text_report(
        MONITORING_REPORT_PATH,
        build_monitoring_report(drift_report, prediction_summary),
    )
    model_health_report = write_text_report(
        MODEL_HEALTH_REPORT_PATH,
        build_model_health_report(model_health_summary),
    )

    return {
        "data_drift_report": drift_path,
        "prediction_monitoring_summary": prediction_path,
        "model_health_summary": model_health_path,
        "monitoring_report": monitoring_report,
        "model_health_report": model_health_report,
    }


def main() -> None:
    """CLI entry point for local monitoring."""
    artifacts = run_monitoring_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
