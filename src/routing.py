
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/output")

PRODUCTS = [
    "AI Analytics",
    "AI Automation",
    "Data Platform",
]

TERRITORIES = ["North", "South", "East", "West"]


def generate_sales_reps() -> pd.DataFrame:
    """Create sales representatives with explicit coverage."""
    records = []
    rep_number = 1

    for territory in TERRITORIES:
        for product in PRODUCTS:
            records.append(
                {
                    "sales_rep_id": f"REP-{rep_number:04d}",
                    "sales_rep_name": f"Sales Rep {rep_number:02d}",
                    "territory": territory,
                    "product": product,
                    "active": True,
                }
            )
            rep_number += 1

    return pd.DataFrame(records)


def route_leads(
    leads: pd.DataFrame,
    scores: pd.DataFrame,
    companies: pd.DataFrame,
    contacts: pd.DataFrame,
    consents: pd.DataFrame,
    sales_reps: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Assign eligible leads and create permitted follow-up tasks."""

    df = (
        leads.merge(
            scores[["lead_id", "lead_score", "priority"]],
            on="lead_id",
            validate="one_to_one",
        )
        .merge(
            companies[["company_id", "territory"]],
            on="company_id",
            validate="many_to_one",
        )
        .merge(
            contacts[["contact_id", "company_id"]],
            on=["contact_id", "company_id"],
            validate="many_to_one",
        )
    )

    # Consent must explicitly allow the intended channel.
    email_consent = consents[
        consents["channel"].eq("SALES_EMAIL")
    ]

    if email_consent["contact_id"].duplicated().any():
        raise ValueError(
            "Multiple email consent records per contact require "
            "effective-date resolution before routing."
        )

    consent_lookup = email_consent.set_index("contact_id")["status"]
    df["consent_status"] = df["contact_id"].map(consent_lookup)

    # Match both territory and product.
    coverage = sales_reps[
        sales_reps["active"].eq(True)
    ][["sales_rep_id", "territory", "product"]]

    df = df.merge(
        coverage,
        on=["territory", "product"],
        how="left",
        validate="many_to_one",
    )

    df["routing_status"] = "ASSIGNED"
    df["routing_reason"] = "ELIGIBLE"

    missing_consent = df["consent_status"].ne("OPTED_IN")
    df.loc[missing_consent, "routing_status"] = "BLOCKED"
    df.loc[missing_consent, "routing_reason"] = "CONSENT_NOT_GRANTED"

    stale = df["is_stale"].eq(True)
    df.loc[
        stale & ~missing_consent, "routing_status"
    ] = "NURTURE"
    df.loc[
        stale & ~missing_consent, "routing_reason"
    ] = "STALE_LEAD"

    missing_rep = df["sales_rep_id"].isna()
    df.loc[
        missing_rep & ~missing_consent, "routing_status"
    ] = "UNASSIGNED"
    df.loc[
        missing_rep & ~missing_consent, "routing_reason"
    ] = "NO_COVERAGE"

    # Only eligible, non-stale, high-priority leads get immediate tasks.
    task_mask = (
        df["routing_status"].eq("ASSIGNED")
        & df["priority"].eq("HIGH")
    )

    df["task_id"] = None
    df["task_status"] = "NOT_CREATED"

    df.loc[task_mask, "task_id"] = (
        "TASK-" + df.loc[task_mask, "lead_id"] + "-001"
    )
    df.loc[task_mask, "task_status"] = "OPEN"

    task_columns = [
        "task_id",
        "lead_id",
        "sales_rep_id",
        "task_status",
    ]

    tasks = df.loc[task_mask, task_columns].copy()

    routed_columns = [
        "lead_id",
        "company_id",
        "lead_score",
        "priority",
        "territory",
        "product",
        "consent_status",
        "sales_rep_id",
        "routing_status",
        "routing_reason",
        "task_id",
        "task_status",
    ]


    return df[routed_columns], tasks


def main():
    leads = pd.read_csv(DATA_DIR / "leads.csv")
    scores = pd.read_csv(DATA_DIR / "lead_scores.csv")
    companies = pd.read_csv(DATA_DIR / "companies.csv")
    contacts = pd.read_csv(DATA_DIR / "contacts.csv")
    consents = pd.read_csv(DATA_DIR / "consents.csv")

    reps = generate_sales_reps()

    routed, tasks = route_leads(
        leads, scores, companies, contacts, consents, reps
    )

    reps.to_csv(DATA_DIR / "sales_reps.csv", index=False)
    routed.to_csv(DATA_DIR / "lead_routing.csv", index=False)
    tasks.to_csv(DATA_DIR / "tasks.csv", index=False)

    print("Lead routing completed.")
    print("\nRouting status:")
    print(routed["routing_status"].value_counts().to_string())
    print(f"\nFollow-up tasks created: {len(tasks):,}")


if __name__ == "__main__":
    main()
