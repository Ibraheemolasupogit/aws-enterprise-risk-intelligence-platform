"""Local real-time inference simulation for single-customer scoring."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from risk_platform.inference.batch_inference import build_batch_risk_scores
from risk_platform.inference.risk_decisioning import (
    generate_decision_reason,
    generate_recommended_action,
)


REALTIME_RESPONSES_PATH = Path("outputs/realtime_scoring_responses.json")
REALTIME_REPORT_PATH = Path("reports/realtime_inference_simulation_report.md")


def simulate_realtime_scoring(sample_size: int = 5) -> list[dict[str, object]]:
    """Simulate JSON-style single-customer scoring responses."""
    batch_scores = build_batch_risk_scores().head(sample_size)
    responses: list[dict[str, object]] = []
    request_timestamp = datetime.now(timezone.utc).isoformat()

    for _, row in batch_scores.iterrows():
        decision_reason = generate_decision_reason(
            row["fraud_risk_score"],
            row["churn_risk_score"],
            row["anomaly_score"],
            row["overall_risk_score"],
        )
        recommended_action = generate_recommended_action(
            row["fraud_risk_score"],
            row["churn_risk_score"],
            row["anomaly_score"],
            row["overall_risk_score"],
        )
        responses.append(
            {
                "customer_id": row["customer_id"],
                "request_timestamp": request_timestamp,
                "fraud_risk_score": round(float(row["fraud_risk_score"]), 6),
                "churn_risk_score": round(float(row["churn_risk_score"]), 6),
                "anomaly_risk_score": round(float(row["anomaly_score"]), 6),
                "overall_risk_score": round(float(row["overall_risk_score"]), 6),
                "overall_risk_band": row["overall_risk_band"],
                "decision_reason": decision_reason,
                "recommended_action": recommended_action,
            }
        )

    return responses


def build_realtime_simulation_report(responses: list[dict[str, object]]) -> str:
    """Build a Markdown report for real-time inference simulation."""
    lines = [
        "# Real-Time Inference Simulation Report",
        "",
        "This report summarizes local JSON-style single-customer scoring responses.",
        "",
        f"- Simulated requests: {len(responses)}",
        "",
        "## Response Examples",
        "",
    ]
    for response in responses:
        lines.append(
            f"- `{response['customer_id']}`: {response['overall_risk_band']} risk, "
            f"{response['recommended_action']}."
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Responses simulate endpoint-style scoring payloads locally.",
            "- No API, Lambda function, SageMaker endpoint, or deployment is created.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_realtime_simulation_artifacts(
    output_path: str | Path = REALTIME_RESPONSES_PATH,
    report_path: str | Path = REALTIME_REPORT_PATH,
    sample_size: int = 5,
) -> dict[str, Path]:
    """Write simulated real-time scoring responses and report."""
    responses = simulate_realtime_scoring(sample_size=sample_size)
    output = Path(output_path)
    report = Path(report_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(responses, indent=2), encoding="utf-8")
    report.write_text(build_realtime_simulation_report(responses), encoding="utf-8")
    return {"realtime_responses": output, "realtime_report": report}
