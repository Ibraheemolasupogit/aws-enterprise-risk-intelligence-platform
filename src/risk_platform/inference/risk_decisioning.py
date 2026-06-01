"""Reusable risk scoring and decisioning helpers."""

from __future__ import annotations


def score_to_risk_band(score: float) -> str:
    """Convert a 0-1 risk score into a simple risk band."""
    if score >= 0.70:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"


def calculate_overall_risk_score(
    fraud_risk_score: float,
    churn_risk_score: float,
    anomaly_risk_score: float,
) -> float:
    """Calculate a weighted enterprise risk score."""
    return round(
        min(
            max(
                0.45 * fraud_risk_score
                + 0.30 * churn_risk_score
                + 0.25 * anomaly_risk_score,
                0,
            ),
            1,
        ),
        6,
    )


def generate_recommended_action(
    fraud_risk_score: float,
    churn_risk_score: float,
    anomaly_risk_score: float,
    overall_risk_score: float,
) -> str:
    """Generate a simple action recommendation from risk scores."""
    if overall_risk_score >= 0.75:
        return "Escalate for risk investigation"
    if fraud_risk_score >= 0.70:
        return "Fraud review"
    if anomaly_risk_score >= 0.70:
        return "Review transaction behaviour"
    if churn_risk_score >= 0.60:
        return "Retention outreach"
    if overall_risk_score >= 0.35:
        return "Monitor customer"
    return "No action required"


def generate_decision_reason(
    fraud_risk_score: float,
    churn_risk_score: float,
    anomaly_risk_score: float,
    overall_risk_score: float,
) -> str:
    """Generate a human-readable decision reason."""
    dominant_signal = max(
        [
            ("fraud", fraud_risk_score),
            ("churn", churn_risk_score),
            ("anomaly", anomaly_risk_score),
        ],
        key=lambda item: item[1],
    )
    overall_band = score_to_risk_band(overall_risk_score)
    return (
        f"Overall risk is {overall_band}; strongest signal is "
        f"{dominant_signal[0]} risk at {dominant_signal[1]:.3f}."
    )
