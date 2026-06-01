"""Build reusable ML-ready features from local synthetic datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


SAMPLE_DATA_DIR = Path("data/sample")
PROCESSED_FEATURE_PATH = Path("data/processed/ml_feature_dataset.csv")
FEATURE_SUMMARY_PATH = Path("outputs/feature_summary.json")
FEATURE_REPORT_PATH = Path("reports/feature_engineering_report.md")

CUSTOMER_SEGMENT_MAP = {
    "consumer": 0,
    "small_business": 1,
    "enterprise": 2,
}
REGION_MAP = {
    "north_america": 0,
    "europe": 1,
    "asia_pacific": 2,
    "latin_america": 3,
}
ACQUISITION_CHANNEL_MAP = {
    "organic": 0,
    "paid_search": 1,
    "partner": 2,
    "referral": 3,
    "direct": 4,
}
EXPERIMENT_GROUP_MAP = {
    "control": 0,
    "treatment": 1,
}
PRE_POST_PERIOD_MAP = {
    "pre": 0,
    "post": 1,
}

CUSTOMER_FEATURES = [
    "account_age_days",
    "customer_segment_encoded",
    "region_encoded",
    "acquisition_channel_encoded",
]
TRANSACTION_FEATURES = [
    "transaction_count",
    "average_transaction_amount",
    "max_transaction_amount",
    "total_transaction_amount",
    "failed_transaction_count",
    "high_value_transaction_flag",
    "transaction_risk_score",
]
SUPPORT_FEATURES = [
    "support_ticket_count",
    "average_resolution_time_hours",
    "complaint_count",
    "satisfaction_score",
    "support_risk_score",
]
BEHAVIOURAL_FEATURES = [
    "login_count_30d",
    "days_since_last_login",
    "session_count_30d",
    "activity_decline_score",
    "engagement_risk_score",
]
EXPERIMENTATION_FEATURES = [
    "treatment_flag",
    "experiment_group_encoded",
    "pre_post_period_encoded",
    "intervention_exposed",
    "conversion_flag",
    "retention_flag",
]
TARGET_COLUMNS = [
    "fraud_label",
    "churn_label",
    "anomaly_label",
]


def load_feature_inputs(data_dir: str | Path = SAMPLE_DATA_DIR) -> dict[str, pd.DataFrame]:
    """Load source datasets for feature engineering."""
    base_path = Path(data_dir)
    return {
        "customers": pd.read_csv(base_path / "customers.csv"),
        "transactions": pd.read_csv(base_path / "transactions.csv"),
        "support_activity": pd.read_csv(base_path / "support_activity.csv"),
        "behavioural_activity": pd.read_csv(base_path / "behavioural_activity.csv"),
        "risk_training_dataset": pd.read_csv(base_path / "risk_training_dataset.csv"),
    }


def build_customer_features(customers: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic encoded customer profile features."""
    features = customers[["customer_id", "account_age_days"]].copy()
    features["customer_segment_encoded"] = customers["customer_segment"].map(CUSTOMER_SEGMENT_MAP).fillna(-1).astype(int)
    features["region_encoded"] = customers["region"].map(REGION_MAP).fillna(-1).astype(int)
    features["acquisition_channel_encoded"] = (
        customers["acquisition_channel"].map(ACQUISITION_CHANNEL_MAP).fillna(-1).astype(int)
    )
    return features


def build_transaction_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction-level records into customer-level features."""
    aggregated = (
        transactions.groupby("customer_id")
        .agg(
            transaction_count=("transaction_id", "count"),
            average_transaction_amount=("transaction_amount", "mean"),
            max_transaction_amount=("transaction_amount", "max"),
            total_transaction_amount=("transaction_amount", "sum"),
            failed_transaction_count=("failed_transaction_count", "sum"),
            fraud_label=("fraud_label", "max"),
        )
        .reset_index()
    )

    high_value_threshold = float(transactions["transaction_amount"].quantile(0.90))
    aggregated["high_value_transaction_flag"] = (aggregated["max_transaction_amount"] >= high_value_threshold).astype(int)
    aggregated["transaction_risk_score"] = (
        0.35 * aggregated["high_value_transaction_flag"]
        + 0.30 * (aggregated["failed_transaction_count"] / aggregated["failed_transaction_count"].max()).fillna(0)
        + 0.25 * (aggregated["max_transaction_amount"] / aggregated["max_transaction_amount"].max()).fillna(0)
        + 0.10 * aggregated["fraud_label"]
    ).clip(0, 1)

    numeric_columns = [
        "average_transaction_amount",
        "max_transaction_amount",
        "total_transaction_amount",
        "transaction_risk_score",
    ]
    aggregated[numeric_columns] = aggregated[numeric_columns].round(4)
    return aggregated.drop(columns=["fraud_label"])


def build_support_features(support_activity: pd.DataFrame) -> pd.DataFrame:
    """Create customer-level support risk features."""
    features = support_activity.copy()
    max_resolution_time = features["average_resolution_time_hours"].max()
    features["support_risk_score"] = (
        0.35 * (features["support_ticket_count"] / features["support_ticket_count"].max()).fillna(0)
        + 0.30 * (features["complaint_count"] / max(features["complaint_count"].max(), 1)).fillna(0)
        + 0.20 * (features["average_resolution_time_hours"] / max(max_resolution_time, 1)).fillna(0)
        + 0.15 * ((5 - features["satisfaction_score"]) / 4).fillna(0)
    ).clip(0, 1)
    features["support_risk_score"] = features["support_risk_score"].round(4)
    return features


def build_behavioural_features(behavioural_activity: pd.DataFrame) -> pd.DataFrame:
    """Create customer-level engagement risk features."""
    features = behavioural_activity.copy()
    features["engagement_risk_score"] = (
        0.45 * features["activity_decline_score"]
        + 0.35 * (features["days_since_last_login"] / max(features["days_since_last_login"].max(), 1)).fillna(0)
        + 0.20 * (1 - (features["login_count_30d"] / max(features["login_count_30d"].max(), 1))).fillna(0)
    ).clip(0, 1)
    features["engagement_risk_score"] = features["engagement_risk_score"].round(4)
    return features


def build_experimentation_features(risk_training_dataset: pd.DataFrame) -> pd.DataFrame:
    """Prepare local experimentation and intervention features."""
    columns = [
        "customer_id",
        "treatment_flag",
        "experiment_group",
        "pre_post_period",
        "intervention_exposed",
        "conversion_flag",
        "retention_flag",
    ]
    features = risk_training_dataset[columns].copy()
    features["experiment_group_encoded"] = features["experiment_group"].map(EXPERIMENT_GROUP_MAP).fillna(-1).astype(int)
    features["pre_post_period_encoded"] = features["pre_post_period"].map(PRE_POST_PERIOD_MAP).fillna(-1).astype(int)
    return features.drop(columns=["experiment_group", "pre_post_period"])


def build_target_columns(risk_training_dataset: pd.DataFrame) -> pd.DataFrame:
    """Select final target columns."""
    return risk_training_dataset[["customer_id", *TARGET_COLUMNS]].copy()


def build_ml_feature_dataset(data_dir: str | Path = SAMPLE_DATA_DIR) -> pd.DataFrame:
    """Build the final customer-level ML feature dataset."""
    inputs = load_feature_inputs(data_dir=data_dir)
    feature_dataset = (
        build_customer_features(inputs["customers"])
        .merge(build_transaction_features(inputs["transactions"]), on="customer_id", how="left")
        .merge(build_support_features(inputs["support_activity"]), on="customer_id", how="left")
        .merge(build_behavioural_features(inputs["behavioural_activity"]), on="customer_id", how="left")
        .merge(build_experimentation_features(inputs["risk_training_dataset"]), on="customer_id", how="left")
        .merge(build_target_columns(inputs["risk_training_dataset"]), on="customer_id", how="left")
    )

    feature_dataset = feature_dataset.fillna(0)
    return feature_dataset[
        [
            "customer_id",
            *CUSTOMER_FEATURES,
            *TRANSACTION_FEATURES,
            *SUPPORT_FEATURES,
            *BEHAVIOURAL_FEATURES,
            *EXPERIMENTATION_FEATURES,
            *TARGET_COLUMNS,
        ]
    ]


def build_feature_summary(feature_dataset: pd.DataFrame) -> dict[str, Any]:
    """Build a JSON-serializable feature summary."""
    feature_groups = {
        "customer_features": CUSTOMER_FEATURES,
        "transaction_features": TRANSACTION_FEATURES,
        "support_features": SUPPORT_FEATURES,
        "behavioural_features": BEHAVIOURAL_FEATURES,
        "experimentation_features": EXPERIMENTATION_FEATURES,
        "target_columns": TARGET_COLUMNS,
    }
    return {
        "row_count": int(len(feature_dataset)),
        "column_count": int(len(feature_dataset.columns)),
        "duplicate_customer_id_count": int(feature_dataset["customer_id"].duplicated().sum()),
        "missing_value_count": int(feature_dataset.isna().sum().sum()),
        "feature_groups": feature_groups,
        "target_distributions": {
            target: {str(label): int(count) for label, count in feature_dataset[target].value_counts().sort_index().items()}
            for target in TARGET_COLUMNS
        },
    }


def build_feature_report(feature_dataset: pd.DataFrame, summary: dict[str, Any]) -> str:
    """Build a Markdown feature engineering report."""
    lines = [
        "# Feature Engineering Report",
        "",
        "This report summarizes the local ML-ready feature dataset created from synthetic customer, transaction, support, behavioral, and experimentation data.",
        "",
        "## Dataset Summary",
        "",
        f"- Row count: {summary['row_count']}",
        f"- Column count: {summary['column_count']}",
        f"- Duplicate `customer_id` count: {summary['duplicate_customer_id_count']}",
        f"- Missing value count: {summary['missing_value_count']}",
        "",
        "## Feature Groups",
        "",
    ]

    for group_name, columns in summary["feature_groups"].items():
        lines.append(f"- `{group_name}`: {', '.join(f'`{column}`' for column in columns)}")

    lines.extend(
        [
            "",
            "## Target Distributions",
            "",
        ]
    )
    for target, distribution in summary["target_distributions"].items():
        formatted_distribution = ", ".join(f"{label}: {count}" for label, count in distribution.items())
        lines.append(f"- `{target}`: {formatted_distribution}")

    lines.extend(
        [
            "",
            "## Feature Quality Notes",
            "",
            "- Encoded categorical features use deterministic local mappings for reproducibility.",
            "- Risk score features are lightweight proxies for later modeling and interpretation.",
            "- Experimentation fields are retained so A/B testing and pre/post analysis can use the same feature table.",
            "- No ML models are trained in this milestone.",
        ]
    )

    numeric_preview_columns = [
        "transaction_risk_score",
        "support_risk_score",
        "engagement_risk_score",
        "risk_score_proxy",
    ]
    available_preview_columns = [column for column in numeric_preview_columns if column in feature_dataset.columns]
    if available_preview_columns:
        lines.extend(["", "## Risk Score Summary", "", "| Feature | Mean | Min | Max |", "| --- | ---: | ---: | ---: |"])
        for column in available_preview_columns:
            lines.append(
                f"| `{column}` | {feature_dataset[column].mean():.4f} | "
                f"{feature_dataset[column].min():.4f} | {feature_dataset[column].max():.4f} |"
            )

    return "\n".join(lines) + "\n"


def write_feature_artifacts(
    data_dir: str | Path = SAMPLE_DATA_DIR,
    output_dataset_path: str | Path = PROCESSED_FEATURE_PATH,
    summary_path: str | Path = FEATURE_SUMMARY_PATH,
    report_path: str | Path = FEATURE_REPORT_PATH,
) -> dict[str, Path]:
    """Build and write feature engineering artifacts."""
    feature_dataset = build_ml_feature_dataset(data_dir=data_dir)
    summary = build_feature_summary(feature_dataset)
    report = build_feature_report(feature_dataset, summary)

    output_dataset = Path(output_dataset_path)
    output_summary = Path(summary_path)
    output_report = Path(report_path)
    output_dataset.parent.mkdir(parents=True, exist_ok=True)
    output_summary.parent.mkdir(parents=True, exist_ok=True)
    output_report.parent.mkdir(parents=True, exist_ok=True)

    feature_dataset.to_csv(output_dataset, index=False)
    output_summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    output_report.write_text(report, encoding="utf-8")

    return {
        "feature_dataset": output_dataset,
        "feature_summary": output_summary,
        "feature_report": output_report,
    }


def main() -> None:
    """CLI entry point for feature engineering artifact generation."""
    artifacts = write_feature_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
