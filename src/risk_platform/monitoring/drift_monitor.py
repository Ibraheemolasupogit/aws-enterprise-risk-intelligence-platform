"""Local data drift monitoring for processed feature datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
MONITORING_CONFIG_PATH = Path("config/monitoring_config.yaml")
DATA_DRIFT_OUTPUT_PATH = Path("outputs/data_drift_report.csv")

EXCLUDED_COLUMNS = {
    "customer_id",
    "fraud_label",
    "churn_label",
    "anomaly_label",
}


def load_monitoring_config(config_path: str | Path = MONITORING_CONFIG_PATH) -> dict[str, Any]:
    """Load local monitoring configuration."""
    return yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))


def load_feature_dataset(dataset_path: str | Path = FEATURE_DATASET_PATH) -> pd.DataFrame:
    """Load the processed ML feature dataset."""
    return pd.read_csv(dataset_path)


def select_drift_features(dataset: pd.DataFrame) -> list[str]:
    """Select numeric columns suitable for drift comparison."""
    numeric_columns = dataset.select_dtypes(include=["number"]).columns.tolist()
    return [column for column in numeric_columns if column not in EXCLUDED_COLUMNS]


def split_reference_current(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create deterministic reference and current samples."""
    midpoint = len(dataset) // 2
    return dataset.iloc[:midpoint].copy(), dataset.iloc[midpoint:].copy()


def calculate_drift_report(
    dataset: pd.DataFrame,
    drift_mean_change_threshold: float = 0.25,
) -> pd.DataFrame:
    """Calculate simple drift indicators for numeric features."""
    reference, current = split_reference_current(dataset)
    rows: list[dict[str, Any]] = []

    for feature in select_drift_features(dataset):
        reference_mean = float(reference[feature].mean())
        current_mean = float(current[feature].mean())
        reference_std = float(reference[feature].std(ddof=0))
        current_std = float(current[feature].std(ddof=0))
        mean_difference = current_mean - reference_mean
        percentage_mean_change = 0.0 if reference_mean == 0 else mean_difference / abs(reference_mean)
        standard_deviation_change = current_std - reference_std

        rows.append(
            {
                "feature": feature,
                "reference_mean": round(reference_mean, 6),
                "current_mean": round(current_mean, 6),
                "mean_difference": round(mean_difference, 6),
                "percentage_mean_change": round(percentage_mean_change, 6),
                "reference_std": round(reference_std, 6),
                "current_std": round(current_std, 6),
                "standard_deviation_change": round(standard_deviation_change, 6),
                "drift_threshold": drift_mean_change_threshold,
                "drift_flag": abs(percentage_mean_change) >= drift_mean_change_threshold,
            }
        )

    return pd.DataFrame(rows).sort_values("percentage_mean_change", key=lambda series: series.abs(), ascending=False)


def write_data_drift_report(
    output_path: str | Path = DATA_DRIFT_OUTPUT_PATH,
    dataset_path: str | Path = FEATURE_DATASET_PATH,
    config_path: str | Path = MONITORING_CONFIG_PATH,
) -> Path:
    """Write data drift report to CSV."""
    config = load_monitoring_config(config_path)
    threshold = float(config["thresholds"]["drift_mean_change_threshold"])
    dataset = load_feature_dataset(dataset_path)
    drift_report = calculate_drift_report(dataset, drift_mean_change_threshold=threshold)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    drift_report.to_csv(output, index=False)
    return output
