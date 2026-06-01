"""Generate a lightweight EDA summary report for synthetic risk data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_RISK_DATASET_PATH = Path("data/sample/risk_training_dataset.csv")
DEFAULT_REPORT_PATH = Path("reports/eda_summary_report.md")


def _format_distribution(series: pd.Series) -> str:
    counts = series.value_counts(dropna=False).sort_index()
    total = len(series)
    return ", ".join(f"{label}: {count} ({count / total:.1%})" for label, count in counts.items())


def _format_numeric_summary(df: pd.DataFrame, columns: list[str]) -> list[str]:
    lines = [
        "| Column | Mean | Median | Min | Max |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for column in columns:
        if column not in df.columns:
            continue
        lines.append(
            f"| `{column}` | {df[column].mean():.2f} | {df[column].median():.2f} | "
            f"{df[column].min():.2f} | {df[column].max():.2f} |"
        )
    return lines


def build_eda_report(dataset_path: str | Path = DEFAULT_RISK_DATASET_PATH) -> str:
    """Build Markdown content for the EDA summary report."""
    dataset = pd.read_csv(dataset_path)
    numeric_columns = [
        "account_age_days",
        "transaction_count",
        "total_transaction_amount",
        "average_transaction_amount",
        "failed_transaction_count",
        "support_ticket_count",
        "average_resolution_time_hours",
        "complaint_count",
        "satisfaction_score",
        "login_count_30d",
        "days_since_last_login",
        "session_count_30d",
        "activity_decline_score",
        "risk_score_proxy",
    ]

    fraud_rate = dataset["fraud_label"].mean()
    churn_rate = dataset["churn_label"].mean()
    anomaly_rate = dataset["anomaly_label"].mean()
    treatment_share = (dataset["experiment_group"] == "treatment").mean()
    post_share = (dataset["pre_post_period"] == "post").mean()

    lines = [
        "# EDA Summary Report",
        "",
        "This lightweight exploratory report summarizes the generated customer-level risk training dataset before feature engineering.",
        "",
        "## Dataset Overview",
        "",
        f"- Source dataset: `{dataset_path}`",
        f"- Row count: {len(dataset)}",
        f"- Column count: {len(dataset.columns)}",
        f"- Customer segments: {_format_distribution(dataset['customer_segment'])}",
        f"- Regions: {_format_distribution(dataset['region'])}",
        "",
        "## Label And Experiment Distributions",
        "",
        f"- Fraud label distribution: {_format_distribution(dataset['fraud_label'])}",
        f"- Churn label distribution: {_format_distribution(dataset['churn_label'])}",
        f"- Anomaly label distribution: {_format_distribution(dataset['anomaly_label'])}",
        f"- Treatment/control split: {_format_distribution(dataset['experiment_group'])}",
        f"- Pre/post split: {_format_distribution(dataset['pre_post_period'])}",
        "",
        "## Key Numeric Summaries",
        "",
    ]
    lines.extend(_format_numeric_summary(dataset, numeric_columns))
    lines.extend(
        [
            "",
            "## Short Interpretation",
            "",
            f"- Fraud appears in {fraud_rate:.1%} of customer-level records, giving future fraud workflows a positive class while preserving class imbalance.",
            f"- Churn appears in {churn_rate:.1%} of records and is linked to behavioral decline, complaints, and login recency in the generator design.",
            f"- Anomalies appear in {anomaly_rate:.1%} of records, which is suitable for lightweight anomaly review and later root-cause analysis.",
            f"- Treatment assignment is {treatment_share:.1%} treatment, supporting local A/B testing simulation.",
            f"- The post-intervention share is {post_share:.1%}, supporting pre/post intervention analysis.",
            "- These findings are synthetic development evidence only and should not be interpreted as real enterprise risk behavior.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_eda_report(
    report_path: str | Path = DEFAULT_REPORT_PATH,
    dataset_path: str | Path = DEFAULT_RISK_DATASET_PATH,
) -> Path:
    """Write the EDA report to disk."""
    output_path = Path(report_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_eda_report(dataset_path=dataset_path), encoding="utf-8")
    return output_path


def main() -> None:
    """CLI entry point for EDA report generation."""
    report_path = write_eda_report()
    print(f"Wrote EDA report: {report_path}")


if __name__ == "__main__":
    main()
