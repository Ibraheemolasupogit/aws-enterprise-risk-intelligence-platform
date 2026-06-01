import pandas as pd

from risk_platform.validation.data_validator import (
    check_duplicate_ids,
    check_experiment_group_validity,
    check_label_validity,
    check_missing_values,
    check_required_columns,
    check_treatment_control_balance,
)


def test_required_columns_validation_works():
    df = pd.DataFrame({"customer_id": ["CUST-001"], "region": ["europe"]})

    result = check_required_columns(df, ["customer_id", "region", "account_age_days"])

    assert result["passed"] is False
    assert result["missing_columns"] == ["account_age_days"]


def test_missing_value_check_returns_expected_structure():
    df = pd.DataFrame({"customer_id": ["CUST-001", "CUST-002"], "region": ["europe", None]})

    result = check_missing_values(df)

    assert result["passed"] is False
    assert result["total_missing_values"] == 1
    assert result["missing_by_column"] == {"region": 1}


def test_duplicate_check_works():
    df = pd.DataFrame({"customer_id": ["CUST-001", "CUST-001", "CUST-002"]})

    result = check_duplicate_ids(df, "customer_id")

    assert result["passed"] is False
    assert result["duplicate_count"] == 1


def test_label_validity_check_works():
    df = pd.DataFrame({"fraud_label": [0, 1, 2], "churn_label": [0, 1, 1]})

    result = check_label_validity(df, ["fraud_label", "churn_label"])

    assert result["passed"] is False
    assert result["failures"] == {"fraud_label": {"invalid_count": 1}}
    assert result["distributions"]["churn_label"] == {0: 1, 1: 2}


def test_experiment_group_validation_works():
    df = pd.DataFrame({"experiment_group": ["control", "treatment", "holdout"]})

    result = check_experiment_group_validity(df)

    assert result["passed"] is False
    assert result["invalid_values"] == ["holdout"]


def test_treatment_control_balance_check_works():
    balanced_df = pd.DataFrame({"experiment_group": ["control", "treatment", "control", "treatment"]})
    imbalanced_df = pd.DataFrame({"experiment_group": ["control", "control", "control", "treatment"]})

    balanced_result = check_treatment_control_balance(balanced_df, tolerance=0.15)
    imbalanced_result = check_treatment_control_balance(imbalanced_df, tolerance=0.15)

    assert balanced_result["passed"] is True
    assert imbalanced_result["passed"] is False
