"""Local pre/post intervention analysis for synthetic outcomes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from risk_platform.experimentation.ab_testing import two_proportion_z_test


FEATURE_DATASET_PATH = Path("data/processed/ml_feature_dataset.csv")
PRE_POST_RESULTS_PATH = Path("outputs/pre_post_intervention_analysis.json")


def _relative_lift(post_rate: float, pre_rate: float) -> float:
    if pre_rate == 0:
        return 0.0
    return post_rate / pre_rate - 1


def run_pre_post_analysis(dataset_path: str | Path = FEATURE_DATASET_PATH) -> dict[str, Any]:
    """Compare pre and post intervention periods for conversion and retention."""
    dataset = pd.read_csv(dataset_path)
    pre = dataset[dataset["pre_post_period_encoded"] == 0]
    post = dataset[dataset["pre_post_period_encoded"] == 1]

    pre_size = int(len(pre))
    post_size = int(len(post))
    pre_conversion_rate = float(pre["conversion_flag"].mean())
    post_conversion_rate = float(post["conversion_flag"].mean())
    pre_retention_rate = float(pre["retention_flag"].mean())
    post_retention_rate = float(post["retention_flag"].mean())

    return {
        "pre_period_size": pre_size,
        "post_period_size": post_size,
        "pre_conversion_rate": round(pre_conversion_rate, 4),
        "post_conversion_rate": round(post_conversion_rate, 4),
        "conversion_lift": round(post_conversion_rate - pre_conversion_rate, 4),
        "conversion_relative_lift": round(_relative_lift(post_conversion_rate, pre_conversion_rate), 4),
        "p_value_conversion_difference": two_proportion_z_test(
            int(post["conversion_flag"].sum()),
            post_size,
            int(pre["conversion_flag"].sum()),
            pre_size,
        ),
        "pre_retention_rate": round(pre_retention_rate, 4),
        "post_retention_rate": round(post_retention_rate, 4),
        "retention_lift": round(post_retention_rate - pre_retention_rate, 4),
        "retention_relative_lift": round(_relative_lift(post_retention_rate, pre_retention_rate), 4),
        "p_value_retention_difference": two_proportion_z_test(
            int(post["retention_flag"].sum()),
            post_size,
            int(pre["retention_flag"].sum()),
            pre_size,
        ),
    }


def write_pre_post_results(
    output_path: str | Path = PRE_POST_RESULTS_PATH,
    dataset_path: str | Path = FEATURE_DATASET_PATH,
) -> Path:
    """Write pre/post analysis results to JSON."""
    results = run_pre_post_analysis(dataset_path=dataset_path)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return output
