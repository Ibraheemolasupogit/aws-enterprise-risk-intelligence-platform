# Inference Design

## Batch Inference Objective

Batch inference scores all customers in the processed feature dataset and produces local enterprise risk outputs. The output combines fraud, churn, anomaly, and overall risk scores with risk bands and recommended actions.

## Real-Time Inference Simulation Objective

The real-time simulation creates JSON-style single-customer scoring responses for a small sample of customers. It demonstrates what an endpoint response could look like without deploying anything.

## Risk Banding Logic

Scores are mapped to simple bands:

- Low: score below 0.35.
- Medium: score from 0.35 to below 0.70.
- High: score at or above 0.70.

## Overall Risk Score Logic

The overall enterprise risk score is a weighted blend:

- Fraud risk: 45%.
- Churn risk: 30%.
- Anomaly risk: 25%.

These weights are simple local defaults for portfolio evidence.

## Decisioning Logic

Recommended actions are generated from the dominant risk signals and overall score. Possible actions include no action, monitoring, transaction review, retention outreach, fraud review, and escalation for risk investigation.

## AWS Mapping

This local inference layer can later map to:

- SageMaker Batch Transform for batch scoring.
- SageMaker Endpoints for real-time model inference.
- Lambda for lightweight decision orchestration.
- API Gateway for request/response access.
- S3 for storing scoring outputs.

No AWS services are used in this milestone.

## Limitations Of Local Inference Simulation

- Scores are local proxies, not deployed model predictions.
- No model artifact is loaded from a registry.
- No latency, authentication, autoscaling, or endpoint monitoring exists.
- Request timestamps are generated locally.
- Decision rules are simple and should not be used for production decisions.
