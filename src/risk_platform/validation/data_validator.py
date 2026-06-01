"""Lightweight validation checks for local synthetic datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


SAMPLE_DATA_DIR = Path("data/sample")

DATASET_FILES = {
    "customers": SAMPLE_DATA_DIR / "customers.csv",
    "transactions": SAMPLE_DATA_DIR / "transactions.csv",
    "support_activity": SAMPLE_DATA_DIR / "support_activity.csv",
    "behavioural_activity": SAMPLE_DATA_DIR / "behavioural_activity.csv",
    "risk_training_dataset": SAMPLE_DATA_DIR / "risk_training_dataset.csv",
}

REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "signup_date",
        "customer_segment",
        "region",
        "account_age_days",
        "acquisition_channel",
    ],
    "transactions": [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "transaction_amount",
        "transaction_type",
        "merchant_category",
        "failed_transaction_count",
        "fraud_label",
    ],
    "support_activity": [
        "customer_id",
        "support_ticket_count",
        "average_resolution_time_hours",
        "complaint_count",
        "satisfaction_score",
    ],
    "behavioural_activity": [
        "customer_id",
        "login_count_30d",
        "days_since_last_login",
        "session_count_30d",
        "activity_decline_score",
    ],
    "risk_training_dataset": [
        "customer_id",
        "fraud_label",
        "churn_label",
        "anomaly_label",
        "experiment_group",
        "treatment_flag",
        "pre_post_period",
        "intervention_exposed",
        "conversion_flag",
        "retention_flag",
        "risk_score_proxy",
    ],
}

ID_COLUMNS = {
    "customers": "customer_id",
    "transactions": "transaction_id",
    "support_activity": "customer_id",
    "behavioural_activity": "customer_id",
    "risk_training_dataset": "customer_id",
}

NUMERIC_RANGES = {
    "customers": {
        "account_age_days": (0, 2_000),
    },
    "transactions": {
        "transaction_amount": (0, None),
        "failed_transaction_count": (0, None),
        "fraud_label": (0, 1),
    },
    "support_activity": {
        "support_ticket_count": (0, None),
        "average_resolution_time_hours": (0, None),
        "complaint_count": (0, None),
        "satisfaction_score": (1, 5),
    },
    "behavioural_activity": {
        "login_count_30d": (0, None),
        "days_since_last_login": (0, 60),
        "session_count_30d": (0, None),
        "activity_decline_score": (0, 1),
    },
    "risk_training_dataset": {
        "transaction_count": (0, None),
        "total_transaction_amount": (0, None),
        "average_transaction_amount": (0, None),
        "failed_transaction_count": (0, None),
        "support_ticket_count": (0, None),
        "average_resolution_time_hours": (0, None),
        "complaint_count": (0, None),
        "satisfaction_score": (1, 5),
        "login_count_30d": (0, None),
        "days_since_last_login": (0, 60),
        "session_count_30d": (0, None),
        "activity_decline_score": (0, 1),
        "risk_score_proxy": (0, 1),
    },
}

LABEL_COLUMNS = [
    "fraud_label",
    "churn_label",
    "anomaly_label",
    "treatment_flag",
    "intervention_exposed",
    "conversion_flag",
    "retention_flag",
]

VALID_EXPERIMENT_GROUPS = {"control", "treatment"}
VALID_PRE_POST_PERIODS = {"pre", "post"}


def load_sample_datasets(data_dir: str | Path = SAMPLE_DATA_DIR) -> dict[str, pd.DataFrame]:
    """Load all supported sample datasets from CSV files."""
    base_path = Path(data_dir)
    return {
        dataset_name: pd.read_csv(base_path / file_path.name)
        for dataset_name, file_path in DATASET_FILES.items()
    }


def check_required_columns(df: pd.DataFrame, required_columns: list[str]) -> dict[str, Any]:
    """Check whether required columns are present."""
    missing_columns = [column for column in required_columns if column not in df.columns]
    return {
        "passed": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "present_columns": [column for column in required_columns if column in df.columns],
    }


def check_missing_values(df: pd.DataFrame) -> dict[str, Any]:
    """Summarize missing values by column."""
    missing_counts = df.isna().sum()
    missing_columns = missing_counts[missing_counts > 0].to_dict()
    return {
        "passed": len(missing_columns) == 0,
        "total_missing_values": int(missing_counts.sum()),
        "missing_by_column": {column: int(count) for column, count in missing_columns.items()},
    }


def check_duplicate_ids(df: pd.DataFrame, id_column: str) -> dict[str, Any]:
    """Check duplicate values in an identifier column."""
    if id_column not in df.columns:
        return {
            "passed": False,
            "id_column": id_column,
            "duplicate_count": None,
            "message": "ID column is missing.",
        }

    duplicate_count = int(df[id_column].duplicated().sum())
    return {
        "passed": duplicate_count == 0,
        "id_column": id_column,
        "duplicate_count": duplicate_count,
        "message": "No duplicate IDs found." if duplicate_count == 0 else "Duplicate IDs found.",
    }


def check_numeric_ranges(df: pd.DataFrame, ranges: dict[str, tuple[float | None, float | None]]) -> dict[str, Any]:
    """Check configured numeric columns against inclusive min/max bounds."""
    failures: dict[str, dict[str, Any]] = {}

    for column, (minimum, maximum) in ranges.items():
        if column not in df.columns:
            failures[column] = {"issue": "missing_column"}
            continue

        numeric_values = pd.to_numeric(df[column], errors="coerce")
        invalid_mask = numeric_values.isna()
        if minimum is not None:
            invalid_mask = invalid_mask | (numeric_values < minimum)
        if maximum is not None:
            invalid_mask = invalid_mask | (numeric_values > maximum)

        invalid_count = int(invalid_mask.sum())
        if invalid_count > 0:
            failures[column] = {
                "invalid_count": invalid_count,
                "minimum": minimum,
                "maximum": maximum,
            }

    return {
        "passed": len(failures) == 0,
        "failures": failures,
    }


def check_label_validity(df: pd.DataFrame, label_columns: list[str] | None = None) -> dict[str, Any]:
    """Check binary label columns for valid 0/1 values."""
    columns_to_check = label_columns or LABEL_COLUMNS
    failures: dict[str, dict[str, Any]] = {}
    distributions: dict[str, dict[int, int]] = {}

    for column in columns_to_check:
        if column not in df.columns:
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        invalid_mask = ~values.isin([0, 1])
        invalid_count = int(invalid_mask.sum())
        distributions[column] = {
            int(label): int(count)
            for label, count in values.value_counts(dropna=False).sort_index().items()
            if pd.notna(label)
        }
        if invalid_count > 0:
            failures[column] = {"invalid_count": invalid_count}

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "distributions": distributions,
    }


def check_experiment_group_validity(
    df: pd.DataFrame,
    column: str = "experiment_group",
    valid_groups: set[str] = VALID_EXPERIMENT_GROUPS,
) -> dict[str, Any]:
    """Check experiment group values."""
    if column not in df.columns:
        return {"passed": False, "column": column, "invalid_values": ["missing_column"], "distribution": {}}

    distribution = df[column].value_counts(dropna=False).to_dict()
    invalid_values = sorted(str(value) for value in set(df[column].dropna()) - valid_groups)
    null_count = int(df[column].isna().sum())
    if null_count > 0:
        invalid_values.append("null")

    return {
        "passed": len(invalid_values) == 0,
        "column": column,
        "invalid_values": invalid_values,
        "distribution": {str(group): int(count) for group, count in distribution.items()},
    }


def check_treatment_control_balance(
    df: pd.DataFrame,
    group_column: str = "experiment_group",
    tolerance: float = 0.15,
) -> dict[str, Any]:
    """Check whether treatment/control assignment is reasonably balanced."""
    if group_column not in df.columns:
        return {"passed": False, "group_column": group_column, "control_share": None, "treatment_share": None}

    normalized_counts = df[group_column].value_counts(normalize=True)
    control_share = float(normalized_counts.get("control", 0.0))
    treatment_share = float(normalized_counts.get("treatment", 0.0))
    difference = abs(control_share - treatment_share)

    return {
        "passed": difference <= tolerance,
        "group_column": group_column,
        "control_share": round(control_share, 4),
        "treatment_share": round(treatment_share, 4),
        "absolute_difference": round(difference, 4),
        "tolerance": tolerance,
    }


def check_pre_post_period_validity(
    df: pd.DataFrame,
    column: str = "pre_post_period",
    valid_periods: set[str] = VALID_PRE_POST_PERIODS,
) -> dict[str, Any]:
    """Check pre/post intervention period values."""
    if column not in df.columns:
        return {"passed": False, "column": column, "invalid_values": ["missing_column"], "distribution": {}}

    distribution = df[column].value_counts(dropna=False).to_dict()
    invalid_values = sorted(str(value) for value in set(df[column].dropna()) - valid_periods)
    null_count = int(df[column].isna().sum())
    if null_count > 0:
        invalid_values.append("null")

    return {
        "passed": len(invalid_values) == 0,
        "column": column,
        "invalid_values": invalid_values,
        "distribution": {str(period): int(count) for period, count in distribution.items()},
    }


def validate_dataset(dataset_name: str, df: pd.DataFrame) -> dict[str, Any]:
    """Run supported validation checks for one dataset."""
    checks = {
        "required_columns": check_required_columns(df, REQUIRED_COLUMNS[dataset_name]),
        "missing_values": check_missing_values(df),
        "duplicate_ids": check_duplicate_ids(df, ID_COLUMNS[dataset_name]),
        "numeric_ranges": check_numeric_ranges(df, NUMERIC_RANGES.get(dataset_name, {})),
        "label_validity": check_label_validity(df),
    }

    if dataset_name == "risk_training_dataset":
        checks["experiment_group_validity"] = check_experiment_group_validity(df)
        checks["treatment_control_balance"] = check_treatment_control_balance(df)
        checks["pre_post_period_validity"] = check_pre_post_period_validity(df)

    return {
        "dataset_name": dataset_name,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "checks": checks,
        "passed": all(check["passed"] for check in checks.values()),
    }


def validate_all_sample_datasets(data_dir: str | Path = SAMPLE_DATA_DIR) -> dict[str, Any]:
    """Load and validate all supported sample datasets."""
    datasets = load_sample_datasets(data_dir=data_dir)
    return {
        dataset_name: validate_dataset(dataset_name, dataset)
        for dataset_name, dataset in datasets.items()
    }
