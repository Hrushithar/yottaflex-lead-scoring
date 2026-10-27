# Source Manifest

## Project Information

- **Project:** YottaFlex AI — Lead Scoring & Sales Pipeline
- **Data type:** Synthetic CRM data
- **Generator:** `src/generator.py`
- **Default random seed:** `20261022`
- **Output directory:** `data/output/`

## Core Data Generation

| Dataset | Purpose | Generation source |
|---|---|---|
| `companies.csv` | Company records | `src/generator.py` |
| `contacts.csv` | Contact records | `src/generator.py` |
| `campaigns.csv` | Campaign records | `src/generator.py` |
| `consents.csv` | Contact communication preferences | `src/generator.py` |
| `leads.csv` | Lead records | `src/generator.py` |
| `activities.csv` | Lead engagement events | `src/generator.py` |

## Derived Pipeline Outputs

| Dataset | Purpose | Generation source |
|---|---|---|
| `lead_scores.csv` | Component scores, total scores, priority, and rule version | `src/scoring.py` |
| `sales_reps.csv` | Sales representative records used for routing | `src/routing.py` |
| `lead_routing.csv` | Lead assignment and routing decisions | `src/routing.py` |
| `tasks.csv` | Follow-up task records | `src/routing.py` |
| `opportunities.csv` | Opportunity and outcome records | `src/opportunities.py` |
| `stage_history.csv` | Opportunity stage progression records | `src/opportunities.py` |

## Testing and Validation Artifacts

| Dataset | Purpose | Generation source |
|---|---|---|
| `anomaly_cases.csv` | Descriptions of anomaly test fixtures | `src/anomalies.py` |
| `ground_truth.csv` | Expected anomaly labels and detection descriptions | `src/anomalies.py` |
| `validation_summary.csv` | Results of structural validation checks | `src/validation.py` |

## Reproducibility

The default seed is `20261022`. The six core generator outputs were compared using SHA-256 checksums across two runs with the same seed and were found to be byte-for-byte identical.

## Data Provenance

The datasets are synthetic and generated locally by the project code. They are not real customer or prospect records.

The generated files are CSV outputs. Their schemas and generation logic should be reviewed alongside the corresponding Python modules.
