"""Detect anomalous customer risk patterns with a local baseline model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from risk_platform.anomaly.root_cause_analysis import (
    build_root_cause_report,
    build_root_cause_table,
    calculate_population_baselines,
    identify_top_anomaly_drivers,
)


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
ANOMALY_SCORES_PATH = Path("outputs/anomaly_scores.csv")
ANOMALY_SUMMARY_PATH = Path("outputs/anomaly_detection_summary.json")
ANOMALY_REPORT_PATH = Path("reports/anomaly_detection_report.md")
ROOT_CAUSE_OUTPUT_PATH = Path("outputs/root_cause_analysis.csv")
ROOT_CAUSE_REPORT_PATH = Path("reports/root_cause_analysis_report.md")

ID_COLUMN = "customer_id"
EXCLUDED_FEATURE_COLUMNS = {
    ID_COLUMN,
    "fraud_label",
    "churn_label",
    "anomaly_label",
    "conversion_flag",
    "retention_flag",
}


def load_feature_dataset(dataset_path: str | Path = FEATURE_DATASET_PATH) -> pd.DataFrame:
    """Load the processed ML feature dataset."""
    return pd.read_csv(dataset_path)


def select_anomaly_features(dataset: pd.DataFrame) -> list[str]:
    """Select numeric features for anomaly detection while avoiding leakage."""
    numeric_columns = dataset.select_dtypes(include=["number"]).columns.tolist()
    return [column for column in numeric_columns if column not in EXCLUDED_FEATURE_COLUMNS]


def assign_anomaly_risk_band(score: float) -> str:
    """Convert normalized anomaly score into a simple risk band."""
    if score >= 0.70:
        return "High"
    if score >= 0.40:
        return "Medium"
    return "Low"


def build_anomaly_scores(
    dataset: pd.DataFrame,
    feature_columns: list[str],
    contamination: float = 0.07,
    random_state: int = 42,
) -> tuple[pd.DataFrame, IsolationForest]:
    """Train IsolationForest and generate anomaly scores."""
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(dataset[feature_columns])

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(scaled_features)

    raw_scores = -model.decision_function(scaled_features)
    min_score = raw_scores.min()
    max_score = raw_scores.max()
    normalized_scores = (raw_scores - min_score) / (max_score - min_score) if max_score > min_score else raw_scores
    labels = (model.predict(scaled_features) == -1).astype(int)

    scored = pd.DataFrame(
        {
            "customer_id": dataset[ID_COLUMN],
            "anomaly_score": normalized_scores.round(6),
            "anomaly_label": labels,
        }
    )
    scored["anomaly_risk_band"] = scored["anomaly_score"].apply(assign_anomaly_risk_band)

    baselines = calculate_population_baselines(
        dataset.assign(anomaly_label=scored["anomaly_label"]),
        feature_columns,
    )
    driver_columns = ["top_anomaly_driver_1", "top_anomaly_driver_2", "top_anomaly_driver_3"]
    for column in driver_columns:
        scored[column] = None

    for index, record in dataset.iterrows():
        drivers = identify_top_anomaly_drivers(record, baselines, feature_columns, top_n=3)
        for driver_index, driver in enumerate(drivers, start=1):
            scored.loc[index, f"top_anomaly_driver_{driver_index}"] = driver["feature"]

    return scored.sort_values("anomaly_score", ascending=False), model


def build_anomaly_summary(
    anomaly_scores: pd.DataFrame,
    feature_columns: list[str],
    model_name: str = "IsolationForest",
) -> dict[str, Any]:
    """Build a JSON-serializable anomaly detection summary."""
    anomaly_count = int(anomaly_scores["anomaly_label"].sum())
    total_count = int(len(anomaly_scores))
    return {
        "model_name": model_name,
        "row_count": total_count,
        "feature_count": int(len(feature_columns)),
        "features_used": feature_columns,
        "anomaly_count": anomaly_count,
        "anomaly_rate": round(anomaly_count / total_count, 4),
        "risk_band_distribution": {
            str(label): int(count)
            for label, count in anomaly_scores["anomaly_risk_band"].value_counts().sort_index().items()
        },
        "top_driver_distribution": {
            str(label): int(count)
            for label, count in anomaly_scores.loc[
                anomaly_scores["anomaly_label"] == 1,
                "top_anomaly_driver_1",
            ].value_counts().head(10).items()
        },
    }


def build_anomaly_detection_report(summary: dict[str, Any]) -> str:
    """Build a Markdown anomaly detection report."""
    lines = [
        "# Anomaly Detection Report",
        "",
        "This report summarizes baseline local anomaly detection on the processed synthetic feature dataset.",
        "",
        "## Model Summary",
        "",
        f"- Model: `{summary['model_name']}`",
        f"- Rows scored: {summary['row_count']}",
        f"- Feature count: {summary['feature_count']}",
        f"- Anomaly count: {summary['anomaly_count']}",
        f"- Anomaly rate: {summary['anomaly_rate']:.1%}",
        "",
        "## Risk Band Distribution",
        "",
    ]
    for band, count in summary["risk_band_distribution"].items():
        lines.append(f"- `{band}`: {count}")

    lines.extend(["", "## Top First-Driver Distribution For Flagged Anomalies", ""])
    if summary["top_driver_distribution"]:
        for driver, count in summary["top_driver_distribution"].items():
            lines.append(f"- `{driver}`: {count}")
    else:
        lines.append("- No anomalies flagged.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The anomaly score is normalized so higher values indicate more unusual records.",
            "- Driver columns identify the largest feature deviations compared with the normal population.",
            "- This is a local baseline for investigation evidence, not a production alerting system.",
            "- No AWS services are used in this milestone.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_anomaly_detection(
    dataset_path: str | Path = FEATURE_DATASET_PATH,
    contamination: float = 0.07,
    random_state: int = 42,
) -> dict[str, Any]:
    """Run anomaly detection and root-cause analysis in memory."""
    dataset = load_feature_dataset(dataset_path)
    feature_columns = select_anomaly_features(dataset)
    anomaly_scores, model = build_anomaly_scores(
        dataset=dataset,
        feature_columns=feature_columns,
        contamination=contamination,
        random_state=random_state,
    )
    summary = build_anomaly_summary(anomaly_scores, feature_columns)
    root_cause_table = build_root_cause_table(dataset, anomaly_scores, feature_columns)

    return {
        "model": model,
        "anomaly_scores": anomaly_scores,
        "summary": summary,
        "anomaly_report": build_anomaly_detection_report(summary),
        "root_cause_table": root_cause_table,
        "root_cause_report": build_root_cause_report(root_cause_table),
    }


def write_anomaly_artifacts(
    dataset_path: str | Path = FEATURE_DATASET_PATH,
    anomaly_scores_path: str | Path = ANOMALY_SCORES_PATH,
    anomaly_summary_path: str | Path = ANOMALY_SUMMARY_PATH,
    anomaly_report_path: str | Path = ANOMALY_REPORT_PATH,
    root_cause_output_path: str | Path = ROOT_CAUSE_OUTPUT_PATH,
    root_cause_report_path: str | Path = ROOT_CAUSE_REPORT_PATH,
) -> dict[str, Path]:
    """Run anomaly detection and write local evidence artifacts."""
    result = run_anomaly_detection(dataset_path=dataset_path)

    output_scores = Path(anomaly_scores_path)
    output_summary = Path(anomaly_summary_path)
    output_anomaly_report = Path(anomaly_report_path)
    output_root_cause = Path(root_cause_output_path)
    output_root_cause_report = Path(root_cause_report_path)

    for output_path in [
        output_scores,
        output_summary,
        output_anomaly_report,
        output_root_cause,
        output_root_cause_report,
    ]:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    result["anomaly_scores"].to_csv(output_scores, index=False)
    output_summary.write_text(json.dumps(result["summary"], indent=2), encoding="utf-8")
    output_anomaly_report.write_text(result["anomaly_report"], encoding="utf-8")
    result["root_cause_table"].to_csv(output_root_cause, index=False)
    output_root_cause_report.write_text(result["root_cause_report"], encoding="utf-8")

    return {
        "anomaly_scores": output_scores,
        "anomaly_summary": output_summary,
        "anomaly_report": output_anomaly_report,
        "root_cause_output": output_root_cause,
        "root_cause_report": output_root_cause_report,
    }


def main() -> None:
    """CLI entry point for local anomaly detection."""
    artifacts = write_anomaly_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
