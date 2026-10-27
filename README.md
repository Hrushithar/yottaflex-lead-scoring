# YottaFlex AI — Lead Scoring & Sales Pipeline

## Overview

An end-to-end synthetic CRM data pipeline for lead scoring, sales routing, task generation, opportunity tracking, and anomaly testing.

The project generates reproducible CRM datasets, applies transparent rule-based lead scoring, routes leads according to consent, territory, and product requirements, and validates data relationships and business constraints.

**Repository:** https://github.com/Hrushithar/yottaflex-lead-scoring

## Key Features

- **Deterministic data generation:** Generates synthetic CRM datasets using a fixed random seed.
- **Rule-based lead scoring:** Evaluates company fit, buying intent, and engagement using transparent scoring rules.
- **Consent-aware lead routing:** Supports routing decisions based on consent, territory, product, and lead priority.
- **Task generation:** Associates eligible leads with follow-up tasks and sales representatives.
- **Opportunity tracking:** Generates sales opportunities and tracks stage history.
- **Anomaly testing:** Provides five labeled anomaly fixtures covering consent violations, post-conversion activity, territory mismatches, duplicate opportunities, and missing stage transitions.
- **Automated validation:** Includes structural and relationship checks alongside pytest tests.
- **Analysis-ready outputs:** Stores generated datasets and pipeline results as CSV files.

## Technology Stack

- Python
- pandas
- pytest
- CSV-based data storage

## Project Structure

```text
yottaflex-lead-scoring/
├── src/
│   ├── generator.py
│   ├── scoring.py
│   ├── routing.py
│   ├── opportunities.py
│   ├── validation.py
│   ├── anomalies.py
│   └── anomaly_detector.py
├── tests/
│   └── test_business_rules.py
├── data/
│   └── output/
├── docs/
│   ├── ai_usage_and_prompt_history.md
│   ├── data_dictionary.md
│   ├── design_decisions.md
│   ├── source_manifest.md
│   └── validation_summary.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10 or later
- pip

The project was tested in a Python 3.14 virtual environment. Compatibility with every Python version in the stated range has not necessarily been verified.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Hrushithar/yottaflex-lead-scoring.git
cd yottaflex-lead-scoring
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Generate the Data

Generate the synthetic CRM datasets using the fixed seed:

```bash
python -m src.generator --seed 20261022
```

The generator supports configurable company, contact, campaign, and lead counts. Run the following command to view the available options:

```bash
python -m src.generator --help
```

## Run the Pipeline

Run the pipeline stages in the following order:

```bash
python -m src.scoring
python -m src.routing
python -m src.opportunities
python -m src.anomalies
```

Generated datasets and pipeline outputs are written to `data/output/`.

**Important:** Generate the upstream data before running downstream stages. Run the stages in order so that scoring, routing, opportunity tracking, and anomaly fixtures correspond to the same dataset.

## Validation and Tests

### Run structural and relationship validation

```bash
python -m src.validation
```

### Run automated tests

```bash
python -m pytest -v
```

### Current development checkpoint

- **Structural validation:** 22 checks passed.
- **Automated tests:** 5 tests passed.
- **Reproducibility:** Six core CSV files were verified to be byte-for-byte identical across two runs using the same seed and unchanged code and configuration.

These results describe the current development checkpoint and should be reverified after project changes.

The existing tests cover fixture completeness, expected anomaly types, ground-truth labels, fixture-level detector behavior, and handling of unknown issue types. They do not establish that every production pipeline component detects or rejects real-world business-rule violations.

For additional information, see `docs/validation_summary.md`.

## Anomaly Fixtures and Ground Truth

The project includes five labeled anomaly fixture types:

1. `OPTED_OUT_LEAD_CONTACTED`
2. `POST_CONVERSION_EVENT_USED`
3. `LEAD_OUTSIDE_TERRITORY`
4. `DUPLICATE_OPPORTUNITY`
5. `STAGE_HISTORY_GAP`

The fixture details are stored in `anomaly_cases.csv`, while expected labels and detection descriptions are stored separately in `ground_truth.csv`.

**Current limitation:** These fixtures describe test scenarios and are not necessarily corrupted production records. The current anomaly detector evaluates the supplied fixture details rather than independently detecting every violation in the generated production datasets.

Further integration testing would be required to verify that production pipeline logic detects or rejects these violations.

## Reproducibility

The default random seed is `20261022`.

Using the same seed, code, configuration, and dependencies helps reproduce the generated data. At the current development checkpoint, six core generated CSV files were compared across two runs and found to be byte-for-byte identical.

This verification applies to those six files and those tested conditions; it should not be interpreted as a guarantee that every output file will always be identical across different environments or dependency versions.

## Limitations and Future Improvements

- Lead scoring uses explicit rule-based weights rather than a trained machine-learning model.
- All CRM data is synthetic and should not be interpreted as real customer information.
- Anomaly fixtures currently describe violations rather than injecting every violation into the production datasets.
- The current detector primarily evaluates fixture details.
- Additional integration tests are needed to verify production business-rule enforcement.
- Future improvements could include stronger end-to-end validation, more anomaly scenarios, and configurable scoring and routing rules.

## Responsible Use of AI

AI tools assisted with development, debugging, testing guidance, and documentation. ChatGPT was the primary AI tool used, accounting for approximately 90% of AI assistance. Gemini accounted for approximately 10% and was used to understand testing- and anomaly-related files.

The project author is responsible for reviewing and understanding the implementation, design decisions, dependencies, limitations, and reported test results.

The separate `docs/ai_usage_and_prompt_history.md` document describes AI usage and prompt history. Actual prompt records should be retained and included as required by the candidate submission instructions.

## License

No license has been selected for this repository yet. Reuse and redistribution permissions should not be assumed until an appropriate license is added.
