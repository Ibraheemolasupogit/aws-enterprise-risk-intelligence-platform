"""Lightweight root-cause helpers for anomaly explanations."""

from __future__ import annotations

from typing import Any

import pandas as pd


def calculate_population_baselines(
    feature_dataset: pd.DataFrame,
    feature_columns: list[str],
    anomaly_label_column: str = "anomaly_label",
) -> pd.Series:
    """Calculate normal-population feature averages."""
    normal_population = feature_dataset[feature_dataset[anomaly_label_column] == 0]
    if normal_population.empty:
        normal_population = feature_dataset
    return normal_population[feature_columns].mean()


def identify_top_anomaly_drivers(
    record: pd.Series,
    baselines: pd.Series,
    feature_columns: list[str],
    top_n: int = 3,
) -> list[dict[str, Any]]:
    """Identify the largest standardized feature deviations for one record."""
    drivers: list[dict[str, Any]] = []

    for feature in feature_columns:
        baseline_value = float(baselines[feature])
        record_value = float(record[feature])
        scale = abs(baseline_value) if abs(baseline_value) > 1 else 1.0
        deviation = (record_value - baseline_value) / scale
        direction = "high" if deviation >= 0 else "low"
        drivers.append(
            {
                "feature": feature,
                "record_value": round(record_value, 4),
                "baseline_value": round(baseline_value, 4),
                "deviation": round(float(deviation), 4),
                "direction": direction,
            }
        )

    return sorted(drivers, key=lambda item: abs(item["deviation"]), reverse=True)[:top_n]


def build_driver_explanation(customer_id: str, drivers: list[dict[str, Any]]) -> str:
    """Create a simple human-readable anomaly explanation."""
    driver_text = "; ".join(
        f"{driver['feature']} is unusually {driver['direction']} "
        f"({driver['record_value']} vs baseline {driver['baseline_value']})"
        for driver in drivers
    )
    return f"{customer_id}: {driver_text}."


def build_root_cause_table(
    feature_dataset: pd.DataFrame,
    anomaly_scores: pd.DataFrame,
    feature_columns: list[str],
    top_n: int = 3,
) -> pd.DataFrame:
    """Build root-cause rows for anomalous records."""
    feature_dataset_without_existing_label = feature_dataset.drop(columns=["anomaly_label"], errors="ignore")
    scored_dataset = feature_dataset_without_existing_label.merge(
        anomaly_scores[["customer_id", "anomaly_score", "anomaly_label", "anomaly_risk_band"]],
        on="customer_id",
        how="inner",
    )
    anomalous_records = scored_dataset[scored_dataset["anomaly_label"] == 1].copy()
    baselines = calculate_population_baselines(scored_dataset, feature_columns)

    rows: list[dict[str, Any]] = []
    for record in anomalous_records.itertuples(index=False):
        record_series = pd.Series(record._asdict())
        drivers = identify_top_anomaly_drivers(record_series, baselines, feature_columns, top_n=top_n)
        row: dict[str, Any] = {
            "customer_id": record_series["customer_id"],
            "anomaly_score": record_series["anomaly_score"],
            "anomaly_risk_band": record_series["anomaly_risk_band"],
            "root_cause_explanation": build_driver_explanation(record_series["customer_id"], drivers),
        }
        for idx, driver in enumerate(drivers, start=1):
            row[f"driver_{idx}_feature"] = driver["feature"]
            row[f"driver_{idx}_direction"] = driver["direction"]
            row[f"driver_{idx}_record_value"] = driver["record_value"]
            row[f"driver_{idx}_baseline_value"] = driver["baseline_value"]
            row[f"driver_{idx}_deviation"] = driver["deviation"]
        rows.append(row)

    return pd.DataFrame(rows)


def build_root_cause_report(root_cause_table: pd.DataFrame) -> str:
    """Build a Markdown report for root-cause analysis outputs."""
    lines = [
        "# Root-Cause Analysis Report",
        "",
        "This report summarizes simple root-cause style explanations for customers flagged as anomalous.",
        "",
        "## Summary",
        "",
        f"- Anomalous records explained: {len(root_cause_table)}",
        "- Explanation logic: compare anomalous feature values with normal-population averages and rank largest relative deviations.",
        "",
        "## Most Common Top Drivers",
        "",
    ]

    if root_cause_table.empty:
        lines.append("- No anomalous records were flagged.")
    else:
        top_driver_counts = root_cause_table["driver_1_feature"].value_counts().head(10)
        for feature, count in top_driver_counts.items():
            lines.append(f"- `{feature}`: {count}")

        lines.extend(["", "## Example Explanations", ""])
        for explanation in root_cause_table["root_cause_explanation"].head(10):
            lines.append(f"- {explanation}")

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- These explanations are heuristic and compare feature deviations against local synthetic baselines.",
            "- Driver rankings are not causal explanations.",
            "- The logic is intended for portfolio evidence and future investigation workflows, not production decisions.",
        ]
    )

    return "\n".join(lines) + "\n"
