"""Local A/B testing analysis for synthetic experiment outcomes."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import NormalDist
from typing import Any

import pandas as pd


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
AB_TEST_RESULTS_PATH = Path("outputs/ab_test_results.json")


def two_proportion_z_test(success_a: int, size_a: int, success_b: int, size_b: int) -> float:
    """Return a two-sided p-value for a two-proportion z-test."""
    if size_a == 0 or size_b == 0:
        return 1.0

    rate_a = success_a / size_a
    rate_b = success_b / size_b
    pooled_rate = (success_a + success_b) / (size_a + size_b)
    standard_error = (pooled_rate * (1 - pooled_rate) * ((1 / size_a) + (1 / size_b))) ** 0.5
    if standard_error == 0:
        return 1.0

    z_score = (rate_a - rate_b) / standard_error
    p_value = 2 * (1 - NormalDist().cdf(abs(z_score)))
    return round(float(p_value), 6)


def _relative_lift(treatment_rate: float, control_rate: float) -> float:
    if control_rate == 0:
        return 0.0
    return treatment_rate / control_rate - 1


def run_ab_test_analysis(dataset_path: str | Path = FEATURE_DATASET_PATH) -> dict[str, Any]:
    """Compare treatment and control groups for conversion and retention outcomes."""
    dataset = pd.read_csv(dataset_path)
    treatment = dataset[dataset["experiment_group_encoded"] == 1]
    control = dataset[dataset["experiment_group_encoded"] == 0]

    treatment_size = int(len(treatment))
    control_size = int(len(control))
    treatment_conversion_rate = float(treatment["conversion_flag"].mean())
    control_conversion_rate = float(control["conversion_flag"].mean())
    treatment_retention_rate = float(treatment["retention_flag"].mean())
    control_retention_rate = float(control["retention_flag"].mean())

    return {
        "treatment_group_size": treatment_size,
        "control_group_size": control_size,
        "treatment_conversion_rate": round(treatment_conversion_rate, 4),
        "control_conversion_rate": round(control_conversion_rate, 4),
        "absolute_lift": round(treatment_conversion_rate - control_conversion_rate, 4),
        "relative_lift": round(_relative_lift(treatment_conversion_rate, control_conversion_rate), 4),
        "p_value_conversion_difference": two_proportion_z_test(
            int(treatment["conversion_flag"].sum()),
            treatment_size,
            int(control["conversion_flag"].sum()),
            control_size,
        ),
        "treatment_retention_rate": round(treatment_retention_rate, 4),
        "control_retention_rate": round(control_retention_rate, 4),
        "retention_rate_difference": round(treatment_retention_rate - control_retention_rate, 4),
        "p_value_retention_difference": two_proportion_z_test(
            int(treatment["retention_flag"].sum()),
            treatment_size,
            int(control["retention_flag"].sum()),
            control_size,
        ),
    }


def write_ab_test_results(
    output_path: str | Path = AB_TEST_RESULTS_PATH,
    dataset_path: str | Path = FEATURE_DATASET_PATH,
) -> Path:
    """Write A/B test results to JSON."""
    results = run_ab_test_analysis(dataset_path=dataset_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return output
