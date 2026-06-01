import json
from pathlib import Path

import pandas as pd

from risk_platform.features.feature_builder import (
    CUSTOMER_FEATURES,
    EXPERIMENTATION_FEATURES,
    SUPPORT_FEATURES,
    TARGET_COLUMNS,
    TRANSACTION_FEATURES,
    BEHAVIOURAL_FEATURES,
    write_feature_artifacts,
)


def test_feature_builder_creates_expected_artifacts(tmp_path: Path):
    dataset_path = tmp_path / "ml_feature_dataset.csv"
    summary_path = tmp_path / "feature_summary.json"
    report_path = tmp_path / "feature_engineering_report.md"

    artifacts = write_feature_artifacts(
        output_dataset_path=dataset_path,
        summary_path=summary_path,
        report_path=report_path,
    )

    assert artifacts["feature_dataset"].exists()
    assert artifacts["feature_summary"].exists()
    assert artifacts["feature_report"].exists()

    feature_dataset = pd.read_csv(dataset_path)
    expected_columns = {
        "customer_id",
        *CUSTOMER_FEATURES,
        *TRANSACTION_FEATURES,
        *SUPPORT_FEATURES,
        *BEHAVIOURAL_FEATURES,
        *EXPERIMENTATION_FEATURES,
        *TARGET_COLUMNS,
    }

    assert expected_columns.issubset(feature_dataset.columns)
    assert set(TARGET_COLUMNS).issubset(feature_dataset.columns)
    assert feature_dataset["customer_id"].duplicated().sum() == 0

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["row_count"] == len(feature_dataset)
    assert summary["duplicate_customer_id_count"] == 0
    assert "feature_groups" in summary

    report = report_path.read_text(encoding="utf-8")
    assert "Feature Engineering Report" in report
    assert "No ML models are trained" in report
