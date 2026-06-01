from pathlib import Path

from risk_platform.ingestion.synthetic_data_generator import generate_synthetic_data, write_synthetic_data


def test_generated_datasets_are_not_empty():
    datasets = generate_synthetic_data(n_customers=25, seed=7)

    assert set(datasets) == {
        "customers",
        "transactions",
        "support_activity",
        "behavioural_activity",
        "risk_training_dataset",
    }
    assert all(not dataset.empty for dataset in datasets.values())


def test_expected_columns_exist():
    datasets = generate_synthetic_data(n_customers=25, seed=7)

    assert {
        "customer_id",
        "signup_date",
        "customer_segment",
        "region",
        "account_age_days",
        "acquisition_channel",
    }.issubset(datasets["customers"].columns)

    assert {
        "transaction_id",
        "customer_id",
        "transaction_date",
        "transaction_amount",
        "transaction_type",
        "merchant_category",
        "failed_transaction_count",
        "fraud_label",
    }.issubset(datasets["transactions"].columns)

    assert {
        "customer_id",
        "support_ticket_count",
        "average_resolution_time_hours",
        "complaint_count",
        "satisfaction_score",
    }.issubset(datasets["support_activity"].columns)

    assert {
        "customer_id",
        "login_count_30d",
        "days_since_last_login",
        "session_count_30d",
        "activity_decline_score",
    }.issubset(datasets["behavioural_activity"].columns)


def test_risk_training_dataset_contains_required_labels_and_experiment_fields():
    dataset = generate_synthetic_data(n_customers=25, seed=7)["risk_training_dataset"]

    assert {
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
    }.issubset(dataset.columns)


def test_csv_files_can_be_written_successfully(tmp_path: Path):
    written_files = write_synthetic_data(output_dir=tmp_path, n_customers=25, seed=7)

    assert set(written_files) == {
        "customers",
        "transactions",
        "support_activity",
        "behavioural_activity",
        "risk_training_dataset",
    }
    assert all(file_path.exists() for file_path in written_files.values())
    assert all(file_path.stat().st_size > 0 for file_path in written_files.values())
