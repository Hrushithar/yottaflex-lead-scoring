# Validation Summary

## Current Verified Results

The project was validated after regenerating the core data and downstream pipeline outputs.

| Check | Result |
|---|---:|
| Structural validation checks passed | 22 |
| Structural validation checks failed | 0 |
| Pytest tests passed | 5 |
| Pytest tests failed | 0 |
| Core generated CSVs reproducible with the same seed | Yes |

## Structural Validation

The validation script checks:

- Expected row counts for companies, contacts, leads, and opportunities.
- Uniqueness of company, contact, lead, activity, and opportunity identifiers.
- Foreign-key integrity for contact, lead, activity, and opportunity relationships.
- Lead score uniqueness and valid score range.
- Unique routing records.
- No open tasks for blocked leads.
- Unique lead associations in the opportunity dataset.
- Company identifiers present in opportunities.
- Stage-history records present for opportunities.

**Latest recorded result:** 22 checks passed and 0 failed.

## Automated Tests

The current pytest suite contains five tests covering:

1. Anomaly fixtures have matching ground-truth records.
2. All five required anomaly types exist.
3. Ground-truth labels are marked as anomalies.
4. All five fixture descriptions are detected by the fixture-level detector.
5. Unknown issue types are not flagged.

**Latest recorded result:** 5 tests passed.

## Reproducibility

The following six core CSV files were compared using SHA-256 checksums before and after regeneration with seed `20261022`:

- `companies.csv`
- `contacts.csv`
- `campaigns.csv`
- `consents.csv`
- `leads.csv`
- `activities.csv`

The checksum comparison produced no differences.

## Limitations

The current anomaly detector evaluates the supplied fixture details. The tests do not yet establish that the production scoring, routing, opportunity, or stage-history logic detects every real violation in altered datasets.

The validation results reflect the project state at the time of the recorded run. Rerun the validation and test commands after making code or data changes.
