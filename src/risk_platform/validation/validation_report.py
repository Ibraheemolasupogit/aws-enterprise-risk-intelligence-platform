"""Generate a Markdown validation report for local sample datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from risk_platform.validation.data_validator import load_sample_datasets, validate_all_sample_datasets


DEFAULT_REPORT_PATH = Path("reports/data_validation_report.md")


def _format_mapping(mapping: dict[Any, Any]) -> str:
    if not mapping:
        return "None"
    return ", ".join(f"{key}: {value}" for key, value in mapping.items())


def build_validation_report(data_dir: str | Path = "data/sample") -> str:
    """Build the validation report Markdown content."""
    datasets = load_sample_datasets(data_dir=data_dir)
    validation_results = validate_all_sample_datasets(data_dir=data_dir)

    lines = [
        "# Data Validation Report",
        "",
        "This report validates the local synthetic sample datasets before feature engineering and model development.",
        "",
        "## Summary",
        "",
        "| Dataset | Rows | Columns | Status |",
        "| --- | ---: | ---: | --- |",
    ]

    for dataset_name, result in validation_results.items():
        status = "PASS" if result["passed"] else "FAIL"
        lines.append(f"| `{dataset_name}` | {result['row_count']} | {result['column_count']} | {status} |")

    for dataset_name, result in validation_results.items():
        dataset = datasets[dataset_name]
        checks = result["checks"]
        label_distributions = checks["label_validity"]["distributions"]

        lines.extend(
            [
                "",
                f"## {dataset_name}",
                "",
                f"- Dataset name: `{dataset_name}`",
                f"- Row count: {result['row_count']}",
                f"- Column count: {result['column_count']}",
                f"- Pass/fail status: {'PASS' if result['passed'] else 'FAIL'}",
                f"- Missing value summary: {_format_mapping(checks['missing_values']['missing_by_column'])}",
                f"- Duplicate check result: {checks['duplicate_ids']['message']} "
                f"({checks['duplicate_ids']['duplicate_count']} duplicates in `{checks['duplicate_ids']['id_column']}`)",
                f"- Required column result: {'PASS' if checks['required_columns']['passed'] else 'FAIL'}",
            ]
        )

        missing_required = checks["required_columns"]["missing_columns"]
        if missing_required:
            lines.append(f"- Missing required columns: {', '.join(missing_required)}")

        if label_distributions:
            lines.append("- Label distribution summary:")
            for column, distribution in label_distributions.items():
                lines.append(f"  - `{column}`: {_format_mapping(distribution)}")
        else:
            lines.append("- Label distribution summary: No label columns present.")

        if "experiment_group" in dataset.columns:
            experiment_distribution = dataset["experiment_group"].value_counts().to_dict()
            lines.append(f"- Experiment group distribution: {_format_mapping(experiment_distribution)}")
        else:
            lines.append("- Experiment group distribution: Not applicable.")

        if "pre_post_period" in dataset.columns:
            period_distribution = dataset["pre_post_period"].value_counts().to_dict()
            lines.append(f"- Pre/post distribution: {_format_mapping(period_distribution)}")

    return "\n".join(lines) + "\n"


def write_validation_report(
    report_path: str | Path = DEFAULT_REPORT_PATH,
    data_dir: str | Path = "data/sample",
) -> Path:
    """Write the validation report to disk."""
    output_path = Path(report_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_validation_report(data_dir=data_dir), encoding="utf-8")
    return output_path


def main() -> None:
    """CLI entry point for validation report generation."""
    report_path = write_validation_report()
    print(f"Wrote validation report: {report_path}")


if __name__ == "__main__":
    main()
