# Design Decisions — YottaFlex AI Lead Scoring

## 1. Overview

This document explains the main design choices, assumptions, trade-offs, and limitations of the synthetic CRM lead-scoring and sales-pipeline project.

The project generates synthetic CRM data, calculates lead scores, routes leads, creates follow-up tasks, tracks opportunities, and produces anomaly test fixtures.

## 2. Synthetic Data Generation

### Decision

Use locally generated synthetic CRM data rather than real customer records or an external data service.

### Rationale

Synthetic data makes the project reproducible and avoids dependence on private customer information or paid services. It also allows record counts and relationships to be controlled during development.

### Trade-off

Synthetic data is useful for testing pipeline behavior, but it does not necessarily reflect the distributions, complexity, or behavior of a real sales organization.

### Reproducibility

The default random seed is `20261022`. The six core generated CSV files were compared across two runs and found to be byte-for-byte identical.

## 3. Rule-Based Lead Scoring

### Decision

Use a transparent rule-based score composed of company fit, buying intent, and engagement.

### Scoring Components

| Component | Maximum points |
|---|---:|
| Company fit | 30 |
| Buying intent | 40 |
| Engagement | 30 |
| **Total** | **100** |

The score is categorized into three priority levels:

- `LOW`: 0–39
- `MEDIUM`: 40–69
- `HIGH`: 70–100

### Rationale

Rule-based scoring is easy to explain, inspect, and reproduce. It provides a baseline for ranking leads without requiring a trained model or a historical labeled dataset.

### Trade-off

The weights are manually defined rather than learned from actual conversion outcomes. Consequently, the scores represent configured business rules and should not be interpreted as calibrated probabilities of conversion.

## 4. Consent-Aware Routing

### Decision

Include communication consent, territory, product, and lead status in the routing process.

### Rationale

Routing should account for whether a contact can be contacted and whether a salesperson is an appropriate match for the lead.

### Trade-off

A deterministic routing process is straightforward to audit, but the current implementation does not represent every possible real-world sales constraint, such as workload balancing, availability, or complex territory exceptions.

The routing logic should be reviewed against the implementation in `src/routing.py`.

## 5. Follow-Up Task Generation

### Decision

Generate follow-up tasks for qualifying assigned leads.

### Rationale

Separating task generation from lead scoring and routing makes the pipeline easier to understand and validate.

### Trade-off

Rule-based task generation is predictable, but it does not optimize scheduling or salesperson workload.

## 6. Opportunity Generation

### Decision

Generate opportunity records from eligible assigned leads and retain a link between each opportunity and its originating lead.

### Rationale

This supports relationship validation and enables the pipeline to track sales outcomes and stage progression.

### Trade-off

Generated opportunity outcomes are synthetic and rule-driven. They should not be interpreted as forecasts of real sales performance.

## 7. Stage History

### Decision

Represent opportunity progression with separate stage-history records and sequence numbers.

### Rationale

A sequence makes it possible to inspect the recorded progression and test for missing transitions.

### Trade-off

Sequence numbers alone do not establish that every transition is valid. Additional checks would be required to validate allowed transitions, timestamps, and lifecycle consistency.

## 8. Anomaly Fixtures and Ground Truth

### Decision

Store anomaly descriptions separately from their expected labels.

### Rationale

Keeping fixture details and ground-truth labels in separate files makes test cases easier to inspect and supports future evaluation workflows.

### Current Limitations

The current fixtures describe five scenarios:

1. An opted-out lead receives a prohibited contact attempt.
2. A post-conversion event is used in historical scoring.
3. A lead is assigned outside its company's territory.
4. A duplicate opportunity is associated with the same lead.
5. Stage history contains a sequence gap.

The current detector evaluates the supplied fixture details. It does not yet prove that the production pipeline detects every violation when introduced into altered datasets.

## 9. Validation Strategy

### Decision

Use automated structural checks and pytest tests.

### Rationale

Structural validation helps detect problems such as duplicate identifiers, invalid relationships, missing opportunity history, and invalid score ranges. Automated tests provide repeatable checks for the expected anomaly-fixture structure.

### Recorded Results

- Structural validation: 22 checks passed, 0 failed.
- Automated tests: 5 passed.

These are results from the recorded development run. They should be rerun after relevant code or data changes.

### Limitation

Passing the current tests does not prove the absence of every possible defect. Integration tests against intentionally modified records would provide stronger evidence that the production business rules detect actual violations.

## 10. Technology Choices

The project uses Python and pandas for data generation and transformation, CSV files for local data storage, and pytest for automated tests.

These choices keep the project relatively lightweight, locally runnable, and straightforward to inspect.

The trade-off is that CSV-based storage does not provide database constraints, transaction management, or concurrent update handling.

## 11. Responsible Use of AI

ChatGPT was the primary AI assistant used for implementation guidance, debugging, testing, and documentation. Google Gemini was used to understand the testing and anomaly-related files.

AI assistance was used to support development and troubleshooting. The submitted implementation, design decisions, validation results, and limitations must be understood and explainable by the project author.

## 12. Future Improvements

Potential next improvements include:

- Integration tests that introduce real violations into test datasets.
- Validation of allowed opportunity stage transitions.
- More comprehensive checks for territory and consent violations.
- Evaluation of scoring weights against representative historical conversion data.
- Stronger pipeline-wide reproducibility checks.
- More detailed validation of opportunity outcomes and task-generation rules.
