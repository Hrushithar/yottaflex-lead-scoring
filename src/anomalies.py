import json
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/output")


def generate_anomaly_fixtures():
    """Create five isolated, labeled anomaly test cases."""

    leads = pd.read_csv(DATA_DIR / "leads.csv")
    consents = pd.read_csv(DATA_DIR / "consents.csv")
    routing = pd.read_csv(DATA_DIR / "lead_routing.csv")
    companies = pd.read_csv(DATA_DIR / "companies.csv")
    reps = pd.read_csv(DATA_DIR / "sales_reps.csv")
    opportunities = pd.read_csv(DATA_DIR / "opportunities.csv")
    history = pd.read_csv(DATA_DIR / "stage_history.csv")

    cases = []
    truth = []

    def add_case(case_id, issue_type, entity_id, details, expected):
        cases.append({
            "case_id": case_id,
            "issue_type": issue_type,
            "entity_id": entity_id,
            "details_json": json.dumps(details, sort_keys=True),
        })
        truth.append({
            "case_id": case_id,
            "issue_type": issue_type,
            "ground_truth": "ANOMALY",
            "expected_detection": expected,
        })

    # 1. An opted-out lead receives a prohibited contact attempt.
    opted_out = consents[
        (consents["channel"] == "SALES_EMAIL")
        & (consents["status"] == "OPTED_OUT")
    ]

    # Find opted-out contacts that actually have leads.
    opted_out_leads = leads.merge(
        opted_out[["contact_id"]],
        on="contact_id",
        how="inner",
        validate="many_to_one",
    )

    if opted_out_leads.empty:
        raise ValueError(
            "No opted-out contacts with leads found. "
            "Check consent and lead generation."
        )

    lead = opted_out_leads.sort_values("lead_id").iloc[0]
    contact_id = lead["contact_id"]

    add_case(
        "ANOM-001",
        "OPTED_OUT_LEAD_CONTACTED",
        lead["lead_id"],
        {
            "contact_id": contact_id,
            "channel": "SALES_EMAIL",
            "consent_status": "OPTED_OUT",
            "attempted_contact": True,
        },
        "Block prohibited contact",
    )

    # 2. An activity occurs after the opportunity was won.
    won = opportunities[opportunities["outcome"] == "WON"]

    if won.empty:
        raise ValueError("No won opportunity available for test.")

    won_opp = won.iloc[0]

    add_case(
        "ANOM-002",
        "POST_CONVERSION_EVENT_USED",
        won_opp["lead_id"],
        {
            "opportunity_id": won_opp["opportunity_id"],
            "conversion_date": "2026-10-01",
            "activity_date": "2026-10-02",
            "score_includes_event": True,
        },
        "Exclude post-conversion activity from historical score",
    )

    # 3. Lead assigned outside its company's territory
    assigned = routing[
        routing["routing_status"] == "ASSIGNED"
    ].merge(
        companies[["company_id", "territory"]],
        on="company_id",
        how="left",
        suffixes=("_routing", "_company"),
    )

    assigned = assigned.merge(
        reps[["sales_rep_id", "territory"]].rename(
            columns={"territory": "rep_territory"}
        ),
        on="sales_rep_id",
        how="left",
    )

    if assigned.empty:
        raise ValueError("No assigned lead available for test.")

    row = assigned.sort_values("lead_id").iloc[0]

    wrong_reps = reps[
        (reps["active"] == True)
        & (reps["territory"] != row["territory_company"])
        & (reps["product"] == row["product"])
    ]

    if wrong_reps.empty:
        raise ValueError(
            "No salesperson with incompatible territory found."
        )

    wrong_rep = wrong_reps.sort_values("sales_rep_id").iloc[0]

    add_case(
        "ANOM-003",
        "LEAD_OUTSIDE_TERRITORY",
        row["lead_id"],
        {
            "company_territory": row["territory_company"],
            "correct_rep_id": row["sales_rep_id"],
            "incorrect_rep_id": wrong_rep["sales_rep_id"],
            "incorrect_rep_territory": wrong_rep["territory"],
        },
        "Flag territory mismatch",
    )

    # 4. A duplicate opportunity is created for the same lead.
    original = opportunities.iloc[0]

    add_case(
        "ANOM-004",
        "DUPLICATE_OPPORTUNITY",
        original["lead_id"],
        {
            "original_opportunity_id": original["opportunity_id"],
            "duplicate_opportunity_id": "OPP-2026-999999",
            "same_lead_id": True,
        },
        "Flag duplicate deal association",
    )

    # 5. Stage history skips an expected sequence number.
    history_counts = history.groupby("opportunity_id").size()
    candidate_ids = history_counts[history_counts >= 3].index

    if len(candidate_ids) == 0:
        raise ValueError("No opportunity with sufficient history.")

    opp_id = sorted(candidate_ids)[0]
    stages = history[history["opportunity_id"] == opp_id].sort_values(
        "sequence"
    )

    add_case(
        "ANOM-005",
        "STAGE_HISTORY_GAP",
        opp_id,
        {
            "existing_sequences": stages["sequence"].tolist(),
            "test_sequences": [1, 3],
            "missing_sequence": 2,
        },
        "Flag missing stage transition",
    )

    pd.DataFrame(cases).to_csv(
        DATA_DIR / "anomaly_cases.csv",
        index=False,
    )

    pd.DataFrame(truth).to_csv(
        DATA_DIR / "ground_truth.csv",
        index=False,
    )

    print("Anomaly fixtures generated.")
    print(f"Test cases: {len(cases)}")
    print("Ground-truth labels saved separately.")


if __name__ == "__main__":
    generate_anomaly_fixtures()
