"""Run local experimentation and model comparison workflows."""

from __future__ import annotations

import json
from pathlib import Path

from risk_platform.experimentation.ab_testing import AB_TEST_RESULTS_PATH, run_ab_test_analysis, write_ab_test_results
from risk_platform.experimentation.champion_challenger import (
    CHAMPION_CHALLENGER_RESULTS_PATH,
    run_champion_challenger_comparison,
    write_champion_challenger_results,
)
from risk_platform.experimentation.pre_post_analysis import (
    PRE_POST_RESULTS_PATH,
    run_pre_post_analysis,
    write_pre_post_results,
)


EXPERIMENT_IMPACT_REPORT_PATH = Path("reports/experiment_impact_report.md")
CHAMPION_CHALLENGER_REPORT_PATH = Path("reports/champion_challenger_report.md")


def build_experiment_impact_report(ab_results: dict, pre_post_results: dict) -> str:
    """Build a Markdown report for A/B and pre/post experiment impact."""
    return "\n".join(
        [
            "# Experiment Impact Report",
            "",
            "This report summarizes local synthetic experiment analysis for treatment/control and pre/post intervention comparisons.",
            "",
            "## A/B Test Summary",
            "",
            f"- Treatment group size: {ab_results['treatment_group_size']}",
            f"- Control group size: {ab_results['control_group_size']}",
            f"- Treatment conversion rate: {ab_results['treatment_conversion_rate']:.2%}",
            f"- Control conversion rate: {ab_results['control_conversion_rate']:.2%}",
            f"- Absolute conversion lift: {ab_results['absolute_lift']:.2%}",
            f"- Relative conversion lift: {ab_results['relative_lift']:.2%}",
            f"- Conversion p-value: {ab_results['p_value_conversion_difference']:.6f}",
            f"- Retention rate difference: {ab_results['retention_rate_difference']:.2%}",
            f"- Retention p-value: {ab_results['p_value_retention_difference']:.6f}",
            "",
            "## Pre/Post Summary",
            "",
            f"- Pre conversion rate: {pre_post_results['pre_conversion_rate']:.2%}",
            f"- Post conversion rate: {pre_post_results['post_conversion_rate']:.2%}",
            f"- Conversion lift: {pre_post_results['conversion_lift']:.2%}",
            f"- Conversion p-value: {pre_post_results['p_value_conversion_difference']:.6f}",
            f"- Pre retention rate: {pre_post_results['pre_retention_rate']:.2%}",
            f"- Post retention rate: {pre_post_results['post_retention_rate']:.2%}",
            f"- Retention lift: {pre_post_results['retention_lift']:.2%}",
            f"- Retention p-value: {pre_post_results['p_value_retention_difference']:.6f}",
            "",
            "## Interpretation",
            "",
            "- These results demonstrate local experiment analysis mechanics on synthetic data.",
            "- P-values are included as statistical evidence, but practical significance should also be considered.",
            "- No production causal claim is made from this simulated dataset.",
            "",
        ]
    )


def build_champion_challenger_report(comparison_results: dict) -> str:
    """Build a Markdown report for Champion vs Challenger decisions."""
    lines = [
        "# Champion Vs Challenger Report",
        "",
        "This report compares existing champion model metrics with deterministic simulated challengers. No models are retrained.",
        "",
    ]
    for model_type, comparison in comparison_results["comparisons"].items():
        lines.extend(
            [
                f"## {model_type.title()}",
                "",
                f"- Selected winner: `{comparison['selected_winner']}`",
                f"- Decision rule: primary `{comparison['primary_metric']}`, secondary `{comparison['secondary_metric']}`",
                f"- Decision reason: {comparison['decision_reason']}",
                "",
                "| Metric | Champion | Challenger |",
                "| --- | ---: | ---: |",
            ]
        )
        for metric in ["roc_auc", "precision", "recall", "f1"]:
            lines.append(f"| `{metric}` | {comparison['champion'][metric]:.4f} | {comparison['challenger'][metric]:.4f} |")
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "- Champion vs Challenger comparison is a governance pattern for deciding whether a new model should replace the current model.",
            "- This milestone simulates the decisioning layer only; challenger metrics are deterministic examples.",
            "- Future milestones can replace simulated challengers with real trained model variants.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text_report(path: str | Path, content: str) -> Path:
    """Write a text report and return its path."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return output


def run_all_experimentation_artifacts() -> dict[str, Path]:
    """Run A/B testing, pre/post analysis, and Champion vs Challenger comparison."""
    write_ab_test_results()
    write_pre_post_results()
    write_champion_challenger_results()

    ab_results = json.loads(AB_TEST_RESULTS_PATH.read_text(encoding="utf-8"))
    pre_post_results = json.loads(PRE_POST_RESULTS_PATH.read_text(encoding="utf-8"))
    comparison_results = json.loads(CHAMPION_CHALLENGER_RESULTS_PATH.read_text(encoding="utf-8"))

    experiment_report = write_text_report(
        EXPERIMENT_IMPACT_REPORT_PATH,
        build_experiment_impact_report(ab_results, pre_post_results),
    )
    champion_report = write_text_report(
        CHAMPION_CHALLENGER_REPORT_PATH,
        build_champion_challenger_report(comparison_results),
    )

    return {
        "ab_test_results": AB_TEST_RESULTS_PATH,
        "pre_post_results": PRE_POST_RESULTS_PATH,
        "champion_challenger_results": CHAMPION_CHALLENGER_RESULTS_PATH,
        "experiment_impact_report": experiment_report,
        "champion_challenger_report": champion_report,
    }


def main() -> None:
    """CLI entry point for local experimentation workflows."""
    artifacts = run_all_experimentation_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
