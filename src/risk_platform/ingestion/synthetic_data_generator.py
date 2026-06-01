"""Generate local synthetic datasets for the risk intelligence platform."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_SEED = 42
DEFAULT_CUSTOMER_COUNT = 500
DEFAULT_OUTPUT_DIR = Path("data/sample")


def _clip_probability(values: np.ndarray) -> np.ndarray:
    return np.clip(values, 0.01, 0.95)


def generate_customers(n_customers: int, rng: np.random.Generator) -> pd.DataFrame:
    """Generate synthetic customer profile data."""
    customer_ids = [f"CUST-{idx:06d}" for idx in range(1, n_customers + 1)]
    account_age_days = rng.integers(15, 1_825, size=n_customers)
    signup_dates = pd.Timestamp("2026-01-01") - pd.to_timedelta(account_age_days, unit="D")

    return pd.DataFrame(
        {
            "customer_id": customer_ids,
            "signup_date": signup_dates.date.astype(str),
            "customer_segment": rng.choice(
                ["consumer", "small_business", "enterprise"],
                size=n_customers,
                p=[0.62, 0.28, 0.10],
            ),
            "region": rng.choice(
                ["north_america", "europe", "asia_pacific", "latin_america"],
                size=n_customers,
                p=[0.45, 0.30, 0.18, 0.07],
            ),
            "account_age_days": account_age_days,
            "acquisition_channel": rng.choice(
                ["organic", "paid_search", "partner", "referral", "direct"],
                size=n_customers,
                p=[0.32, 0.24, 0.18, 0.16, 0.10],
            ),
        }
    )


def generate_transactions(customers: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Generate synthetic transaction records with transaction-level fraud labels."""
    rows: list[dict[str, object]] = []
    transaction_id = 1

    segment_amount_multiplier = {
        "consumer": 1.0,
        "small_business": 2.4,
        "enterprise": 5.5,
    }
    merchant_risk = {
        "grocery": 0.0,
        "travel": 0.02,
        "electronics": 0.04,
        "digital_goods": 0.06,
        "cash_transfer": 0.09,
        "subscription": 0.01,
    }

    for customer in customers.itertuples(index=False):
        transaction_count = max(1, int(rng.poisson(4)))
        for _ in range(transaction_count):
            merchant_category = rng.choice(
                list(merchant_risk.keys()),
                p=[0.24, 0.14, 0.16, 0.15, 0.08, 0.23],
            )
            failed_transaction_count = int(rng.poisson(0.35 + merchant_risk[merchant_category] * 4))
            base_amount = rng.lognormal(mean=3.6, sigma=0.8)
            transaction_amount = round(
                base_amount * segment_amount_multiplier[customer.customer_segment],
                2,
            )
            fraud_probability = (
                0.01
                + merchant_risk[merchant_category]
                + 0.015 * failed_transaction_count
                + (0.035 if transaction_amount > 350 else 0.0)
                + (0.02 if customer.account_age_days < 90 else 0.0)
            )

            rows.append(
                {
                    "transaction_id": f"TXN-{transaction_id:08d}",
                    "customer_id": customer.customer_id,
                    "transaction_date": (
                        pd.Timestamp("2026-01-01")
                        - pd.to_timedelta(int(rng.integers(0, 180)), unit="D")
                    ).date().isoformat(),
                    "transaction_amount": transaction_amount,
                    "transaction_type": rng.choice(
                        ["purchase", "refund", "transfer", "subscription"],
                        p=[0.72, 0.07, 0.11, 0.10],
                    ),
                    "merchant_category": merchant_category,
                    "failed_transaction_count": failed_transaction_count,
                    "fraud_label": int(rng.random() < fraud_probability),
                }
            )
            transaction_id += 1

    return pd.DataFrame(rows)


def generate_support_activity(customers: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Generate customer support activity data."""
    n_customers = len(customers)
    support_ticket_count = rng.poisson(1.2, size=n_customers)
    complaint_count = rng.binomial(support_ticket_count, 0.28)
    average_resolution_time_hours = np.where(
        support_ticket_count > 0,
        rng.gamma(shape=2.0, scale=7.5, size=n_customers),
        0,
    )
    satisfaction_score = np.clip(
        4.6 - complaint_count * 0.45 - average_resolution_time_hours * 0.025 + rng.normal(0, 0.35, n_customers),
        1,
        5,
    )

    return pd.DataFrame(
        {
            "customer_id": customers["customer_id"],
            "support_ticket_count": support_ticket_count,
            "average_resolution_time_hours": np.round(average_resolution_time_hours, 2),
            "complaint_count": complaint_count,
            "satisfaction_score": np.round(satisfaction_score, 2),
        }
    )


def generate_behavioural_activity(customers: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Generate customer behavioural activity data."""
    n_customers = len(customers)
    login_count_30d = rng.poisson(12, size=n_customers)
    session_count_30d = login_count_30d + rng.poisson(5, size=n_customers)
    days_since_last_login = np.clip(rng.gamma(shape=2.2, scale=4.2, size=n_customers), 0, 60)
    activity_decline_score = np.clip(
        (days_since_last_login / 60) + np.maximum(0, 10 - login_count_30d) / 20 + rng.normal(0, 0.08, n_customers),
        0,
        1,
    )

    return pd.DataFrame(
        {
            "customer_id": customers["customer_id"],
            "login_count_30d": login_count_30d,
            "days_since_last_login": np.round(days_since_last_login, 1),
            "session_count_30d": session_count_30d,
            "activity_decline_score": np.round(activity_decline_score, 3),
        }
    )


def generate_risk_training_dataset(
    customers: pd.DataFrame,
    transactions: pd.DataFrame,
    support_activity: pd.DataFrame,
    behavioural_activity: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Create a customer-level training table with labels and experiment fields."""
    transaction_features = (
        transactions.groupby("customer_id")
        .agg(
            transaction_count=("transaction_id", "count"),
            total_transaction_amount=("transaction_amount", "sum"),
            average_transaction_amount=("transaction_amount", "mean"),
            failed_transaction_count=("failed_transaction_count", "sum"),
            fraud_label=("fraud_label", "max"),
        )
        .reset_index()
    )

    dataset = (
        customers.merge(transaction_features, on="customer_id", how="left")
        .merge(support_activity, on="customer_id", how="left")
        .merge(behavioural_activity, on="customer_id", how="left")
    )

    experiment_group = rng.choice(["control", "treatment"], size=len(dataset), p=[0.5, 0.5])
    pre_post_period = rng.choice(["pre", "post"], size=len(dataset), p=[0.45, 0.55])
    treatment_flag = (experiment_group == "treatment").astype(int)
    intervention_exposed = ((experiment_group == "treatment") & (pre_post_period == "post")).astype(int)

    churn_probability = _clip_probability(
        0.08
        + dataset["activity_decline_score"].to_numpy() * 0.36
        + (dataset["days_since_last_login"].to_numpy() > 20) * 0.12
        + (dataset["complaint_count"].to_numpy() >= 2) * 0.10
        - intervention_exposed * 0.06
        - (dataset["account_age_days"].to_numpy() > 365) * 0.04
    )
    churn_label = (rng.random(len(dataset)) < churn_probability).astype(int)

    conversion_probability = _clip_probability(
        0.18
        + intervention_exposed * 0.08
        + (dataset["satisfaction_score"].to_numpy() - 3.0) * 0.04
        - dataset["activity_decline_score"].to_numpy() * 0.07
    )
    retention_probability = _clip_probability(1 - churn_probability + intervention_exposed * 0.04)

    amount_z_score = (
        dataset["total_transaction_amount"] - dataset["total_transaction_amount"].mean()
    ) / dataset["total_transaction_amount"].std(ddof=0)
    failure_z_score = (
        dataset["failed_transaction_count"] - dataset["failed_transaction_count"].mean()
    ) / dataset["failed_transaction_count"].std(ddof=0)
    support_z_score = (
        dataset["average_resolution_time_hours"] - dataset["average_resolution_time_hours"].mean()
    ) / dataset["average_resolution_time_hours"].std(ddof=0)
    anomaly_signal = amount_z_score.fillna(0) * 0.45 + failure_z_score.fillna(0) * 0.35 + support_z_score.fillna(0) * 0.20
    anomaly_threshold = float(np.quantile(anomaly_signal, 0.93))
    anomaly_label = (anomaly_signal > anomaly_threshold).astype(int)

    risk_score_proxy = np.clip(
        0.20 * dataset["fraud_label"].to_numpy()
        + 0.28 * churn_probability
        + 0.18 * anomaly_label.to_numpy()
        + 0.16 * dataset["activity_decline_score"].to_numpy()
        + 0.10 * np.clip(dataset["failed_transaction_count"].to_numpy() / 6, 0, 1)
        + 0.08 * np.clip(dataset["complaint_count"].to_numpy() / 4, 0, 1),
        0,
        1,
    )

    dataset["experiment_group"] = experiment_group
    dataset["treatment_flag"] = treatment_flag
    dataset["pre_post_period"] = pre_post_period
    dataset["intervention_exposed"] = intervention_exposed
    dataset["conversion_flag"] = (rng.random(len(dataset)) < conversion_probability).astype(int)
    dataset["retention_flag"] = (rng.random(len(dataset)) < retention_probability).astype(int)
    dataset["churn_label"] = churn_label
    dataset["anomaly_label"] = anomaly_label
    dataset["risk_score_proxy"] = np.round(risk_score_proxy, 4)

    numeric_columns = [
        "total_transaction_amount",
        "average_transaction_amount",
        "average_resolution_time_hours",
    ]
    dataset[numeric_columns] = dataset[numeric_columns].round(2)

    return dataset


def generate_synthetic_data(
    n_customers: int = DEFAULT_CUSTOMER_COUNT,
    seed: int = DEFAULT_SEED,
) -> dict[str, pd.DataFrame]:
    """Generate all synthetic datasets used by the project."""
    rng = np.random.default_rng(seed)
    customers = generate_customers(n_customers=n_customers, rng=rng)
    transactions = generate_transactions(customers=customers, rng=rng)
    support_activity = generate_support_activity(customers=customers, rng=rng)
    behavioural_activity = generate_behavioural_activity(customers=customers, rng=rng)
    risk_training_dataset = generate_risk_training_dataset(
        customers=customers,
        transactions=transactions,
        support_activity=support_activity,
        behavioural_activity=behavioural_activity,
        rng=rng,
    )

    return {
        "customers": customers,
        "transactions": transactions,
        "support_activity": support_activity,
        "behavioural_activity": behavioural_activity,
        "risk_training_dataset": risk_training_dataset,
    }


def write_synthetic_data(
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    n_customers: int = DEFAULT_CUSTOMER_COUNT,
    seed: int = DEFAULT_SEED,
) -> dict[str, Path]:
    """Generate synthetic datasets and write them as CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    datasets = generate_synthetic_data(n_customers=n_customers, seed=seed)
    written_files: dict[str, Path] = {}
    for dataset_name, dataset in datasets.items():
        file_path = output_path / f"{dataset_name}.csv"
        dataset.to_csv(file_path, index=False)
        written_files[dataset_name] = file_path

    return written_files


def main() -> None:
    """CLI entry point for local synthetic data generation."""
    parser = argparse.ArgumentParser(description="Generate local synthetic risk platform sample data.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for generated CSV files.")
    parser.add_argument("--n-customers", type=int, default=DEFAULT_CUSTOMER_COUNT, help="Number of customers.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed for reproducible data.")
    args = parser.parse_args()

    written_files = write_synthetic_data(
        output_dir=args.output_dir,
        n_customers=args.n_customers,
        seed=args.seed,
    )
    for dataset_name, file_path in written_files.items():
        print(f"Wrote {dataset_name}: {file_path}")


if __name__ == "__main__":
    main()
