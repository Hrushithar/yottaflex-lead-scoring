
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/output")


def check_unique(df, column):
    return int(df[column].duplicated().sum())


def check_foreign_key(child, child_column, parent, parent_column):
    return int((~child[child_column].isin(parent[parent_column])).sum())


def run_validation():
    companies = pd.read_csv(DATA_DIR / "companies.csv")
    contacts = pd.read_csv(DATA_DIR / "contacts.csv")
    leads = pd.read_csv(DATA_DIR / "leads.csv")
    campaigns = pd.read_csv(DATA_DIR / "campaigns.csv")
    consents = pd.read_csv(DATA_DIR / "consents.csv")
    activities = pd.read_csv(DATA_DIR / "activities.csv")
    scores = pd.read_csv(DATA_DIR / "lead_scores.csv")
    routing = pd.read_csv(DATA_DIR / "lead_routing.csv")
    tasks = pd.read_csv(DATA_DIR / "tasks.csv")
    opportunities = pd.read_csv(DATA_DIR / "opportunities.csv")
    history = pd.read_csv(DATA_DIR / "stage_history.csv")

    results = {}

    # Required baseline row counts.
    results["companies_count"] = len(companies) == 5000
    results["contacts_count"] = len(contacts) == 10000
    results["leads_count"] = len(leads) == 20000
    results["opportunities_count"] = len(opportunities) == 3000

    # Primary-key uniqueness.
    results["company_ids_unique"] = (
        check_unique(companies, "company_id") == 0
    )
    results["contact_ids_unique"] = (
        check_unique(contacts, "contact_id") == 0
    )
    results["lead_ids_unique"] = (
        check_unique(leads, "lead_id") == 0
    )
    results["activity_ids_unique"] = (
        check_unique(activities, "activity_id") == 0
    )
    results["opportunity_ids_unique"] = (
        check_unique(opportunities, "opportunity_id") == 0
    )

    # Foreign-key integrity.
    results["contacts_company_fk_valid"] = (
        check_foreign_key(
            contacts, "company_id", companies, "company_id"
        ) == 0
    )
    results["leads_contact_fk_valid"] = (
        check_foreign_key(
            leads, "contact_id", contacts, "contact_id"
        ) == 0
    )
    results["leads_company_fk_valid"] = (
        check_foreign_key(
            leads, "company_id", companies, "company_id"
        ) == 0
    )
    results["leads_campaign_fk_valid"] = (
        check_foreign_key(
            leads, "campaign_id", campaigns, "campaign_id"
        ) == 0
    )
    results["activities_lead_fk_valid"] = (
        check_foreign_key(
            activities, "lead_id", leads, "lead_id"
        ) == 0
    )
    results["opportunities_lead_fk_valid"] = (
        check_foreign_key(
            opportunities, "lead_id", leads, "lead_id"
        ) == 0
    )

    # Scores and routing.
    results["scores_unique"] = (
        check_unique(scores, "lead_id") == 0
    )
    results["scores_in_range"] = scores[
        "lead_score"
    ].between(0, 100).all()

    results["routing_unique"] = (
        check_unique(routing, "lead_id") == 0
    )

    # Consent safety: no blocked contact can have an open task.
    blocked_ids = set(
        routing.loc[
            routing["routing_status"] == "BLOCKED",
            "lead_id",
        ]
    )
    open_task_ids = set(
        tasks.loc[
            tasks["task_status"] == "OPEN",
            "lead_id",
        ]
    )

    results["no_open_tasks_for_blocked_leads"] = (
        blocked_ids.isdisjoint(open_task_ids)
    )

    # Opportunity consistency.
    results["opportunity_leads_unique"] = (
        check_unique(opportunities, "lead_id") == 0
    )
    results["opportunity_companies_present"] = (
        opportunities["company_id"].notna().all()
    )

    # Every opportunity has stage history.
    history_opportunities = set(history["opportunity_id"])
    results["all_opportunities_have_history"] = set(
        opportunities["opportunity_id"]
    ).issubset(history_opportunities)

    # Save a human-readable report.
    report = pd.DataFrame(
        [
            {
                "check": name,
                "passed": bool(passed),
            }
            for name, passed in results.items()
        ]
    )

    report.to_csv(
        DATA_DIR / "validation_summary.csv",
        index=False,
    )

    print("\nVALIDATION SUMMARY")
    print("=" * 45)

    for name, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'}  {name}")

    failures = sum(not passed for passed in results.values())

    print("=" * 45)
    print(f"Checks: {len(results)}")
    print(f"Passed: {len(results) - failures}")
    print(f"Failed: {failures}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run_validation()
