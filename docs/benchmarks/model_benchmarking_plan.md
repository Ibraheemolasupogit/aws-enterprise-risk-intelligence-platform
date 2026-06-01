# Model Benchmarking Plan

This plan defines the benchmark metrics that will be used once modeling and experimentation milestones begin. The project will remain local and synthetic during these phases, but the metrics are selected to mirror production-style decision making.

## Fraud Model

- Precision: Measures how many predicted fraud cases are actually fraudulent.
- Recall: Measures how many actual fraud cases are detected.
- F1: Balances precision and recall for imbalanced fraud data.
- ROC-AUC: Evaluates ranking quality across classification thresholds.
- Confusion matrix: Shows true positives, false positives, true negatives, and false negatives.

Planned evidence artifact: Fraud model evaluation report with metric table, confusion matrix, threshold notes, and business interpretation.

## Churn Model

- Precision: Measures how many predicted churners actually churn.
- Recall: Measures how many actual churners are identified.
- F1: Balances precision and recall.
- ROC-AUC: Evaluates ranking quality across thresholds.
- Lift: Measures how much better the model is at identifying churners than random selection.

Planned evidence artifact: Churn evaluation report with metric table, lift chart or lift table, and retention-use interpretation.

## Anomaly Detection

- Anomaly rate: Percentage of records flagged as anomalous.
- Top anomaly drivers: Features or segments most associated with flagged anomalies.
- False positive review proxy: Lightweight review estimate using synthetic labels, rules, or manual inspection categories.
- Root-cause explanation quality: Qualitative score for whether explanations are interpretable, ranked, and tied to measurable feature shifts.

Planned evidence artifact: Anomaly report with score distribution, anomaly examples, driver ranking, and root-cause notes.

## Experimentation

- Treatment vs control comparison: Compares outcome rates, means, or risk metrics across groups.
- A/B testing simulation: Uses synthetic assignment and outcomes to estimate intervention impact.
- Statistical significance testing: Reports p-values, confidence intervals, and practical significance.
- Pre/post intervention analysis: Compares metrics before and after a simulated intervention.
- Champion vs Challenger comparison: Compares model or strategy variants using agreed decision metrics.

Planned evidence artifact: Experiment analysis report with assumptions, group summaries, statistical test results, effect size, and recommendation.

## Monitoring

- Data drift: Detects changes in feature distributions between baseline and current data.
- Prediction drift: Detects changes in model score or label distributions.
- Performance degradation: Tracks metric changes when synthetic ground truth is available.
- Model health status: Summarizes data, prediction, performance, and business KPI checks.

Planned evidence artifact: Monitoring report with drift metrics, threshold flags, health status, and recommended follow-up actions.
