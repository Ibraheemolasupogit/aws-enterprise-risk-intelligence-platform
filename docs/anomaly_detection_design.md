# Anomaly Detection Design

## Anomaly Detection Objective

The objective is to detect unusual customer risk patterns in the processed synthetic feature dataset and produce lightweight root-cause style explanations for investigation. This milestone focuses on local anomaly evidence, not production monitoring or alerting.

## Why Anomaly Detection Matters For Enterprise Risk Intelligence

Enterprise risk teams often need to find unusual behavior before a supervised label is available. Anomaly detection can help surface unexpected transaction patterns, support escalations, engagement drops, or combined risk signals that deserve review.

## Selected Baseline Method

The baseline method is `IsolationForest`. It is a simple unsupervised model that isolates unusual records based on feature patterns. It works well as a local baseline because it is fast, available in scikit-learn, and does not require labeled anomaly outcomes.

## Anomaly Score Interpretation

The workflow normalizes model scores so higher `anomaly_score` values indicate more unusual customer records. The score is also mapped into simple risk bands:

- Low.
- Medium.
- High.

These bands are review aids only and are not production thresholds.

## Root-Cause Analysis Logic

Root-cause analysis is implemented with simple feature deviation logic:

1. Compare anomalous records against normal-population feature averages.
2. Calculate relative deviations for model-ready numeric features.
3. Rank the largest high or low deviations.
4. Return the top drivers and a short human-readable explanation.

This gives reviewers a practical starting point for investigating why a record was flagged.

## Limitations Of The Local Baseline Approach

- The data is synthetic and does not represent real customer behavior.
- IsolationForest does not provide causal explanations.
- Driver rankings are heuristic comparisons against local averages.
- Thresholds and risk bands are simple defaults.
- No streaming detection, alert routing, or monitoring workflow is included yet.
- No AWS services are used in this milestone.

## Future AWS/SageMaker Mapping

This local workflow can later map to AWS services:

- Store feature inputs and anomaly outputs in Amazon S3.
- Run anomaly scoring as a SageMaker Processing job or SageMaker Batch Transform job.
- Track anomaly job metrics in CloudWatch.
- Use SageMaker Model Registry if the anomaly detector becomes a managed model artifact.
- Route future real-time anomaly events through Kinesis, Lambda, or a SageMaker endpoint.

This milestone intentionally remains local-only.
