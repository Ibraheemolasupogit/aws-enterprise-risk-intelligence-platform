# Champion Vs Challenger Report

This report compares existing champion model metrics with deterministic simulated challengers. No models are retrained.

## Fraud

- Selected winner: `challenger`
- Decision rule: primary `roc_auc`, secondary `recall`
- Decision reason: Selected by higher ROC-AUC, with recall as tie-breaker.

| Metric | Champion | Challenger |
| --- | ---: | ---: |
| `roc_auc` | 0.6355 | 0.6535 |
| `precision` | 0.2381 | 0.2281 |
| `recall` | 0.2632 | 0.2982 |
| `f1` | 0.2500 | 0.2620 |

## Churn

- Selected winner: `challenger`
- Decision rule: primary `roc_auc`, secondary `recall`
- Decision reason: Selected by higher ROC-AUC, with recall as tie-breaker.

| Metric | Champion | Challenger |
| --- | ---: | ---: |
| `roc_auc` | 0.6333 | 0.6453 |
| `precision` | 0.1667 | 0.1747 |
| `recall` | 0.1000 | 0.1200 |
| `f1` | 0.1250 | 0.1350 |

## Interpretation

- Champion vs Challenger comparison is a governance pattern for deciding whether a new model should replace the current model.
- This milestone simulates the decisioning layer only; challenger metrics are deterministic examples.
- Future milestones can replace simulated challengers with real trained model variants.
