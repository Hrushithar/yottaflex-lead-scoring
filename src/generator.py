
import argparse
import random
from pathlib import Path
import pandas as pd
from datetime import date, timedelta


SEED = 20261022
OUTPUT_DIR = Path("data/output")


def generate_companies(n: int, rng: random.Random) -> pd.DataFrame:
    """Generate company master records."""
    industries = [
        "Technology",
        "Healthcare",
        "Finance",
        "Manufacturing",
        "Retail",
        "Education",
    ]

    territories = ["North", "South", "East", "West"]

    records = []

    for i in range(1, n + 1):
        records.append(
            {
                "company_id": f"CO-{i:06d}",
                "company_name": f"Company {i:06d}",
                "industry": rng.choice(industries),
                "employee_count": rng.choice(
                    [10, 25, 50, 100, 250, 500, 1000]
                ),
                "territory": rng.choice(territories),
                "is_customer": False,
            }
        )

    return pd.DataFrame(records)


def generate_contacts(
    n: int,
    companies: pd.DataFrame,
    rng: random.Random,
) -> pd.DataFrame:
    """Generate contact records linked to existing companies."""
    first_names = [
        "Rahul", "Priya", "Arjun", "Ananya",
        "Kiran", "Neha", "Vikram", "Asha",
    ]

    last_names = [
        "Sharma", "Rao", "Patel", "Kumar",
        "Reddy", "Singh", "Nair", "Das",
    ]

    job_titles = [
        "CEO",
        "CTO",
        "IT Manager",
        "Sales Manager",
        "Finance Manager",
        "Data Analyst",
    ]

    company_ids = companies["company_id"].tolist()
    records = []

    for i in range(1, n + 1):
        records.append(
            {
                "contact_id": f"CON-{i:06d}",
                "company_id": rng.choice(company_ids),
                "first_name": rng.choice(first_names),
                "last_name": rng.choice(last_names),
                "job_title": rng.choice(job_titles),
            }
        )

    return pd.DataFrame(records)


def generate_campaigns(n: int = 20) -> pd.DataFrame:
    """Generate marketing campaign master records."""
    channels = ["Email", "Webinar", "Paid Search", "Social Media"]

    records = []

    for i in range(1, n + 1):
        records.append(
            {
                "campaign_id": f"CAMP-{i:04d}",
                "campaign_name": f"Campaign {i:04d}",
                "channel": channels[(i - 1) % len(channels)],
                "status": "Active",
            }
        )

    return pd.DataFrame(records)

def generate_consents(contacts: pd.DataFrame) -> pd.DataFrame:
    """Create consent records for contacts."""
    records = []

    for i, contact in enumerate(
        contacts.itertuples(index=False), start=1
    ):
        # Deterministic distribution for reproducibility.
        status = (
            "OPTED_OUT"
            if i % 10 == 0
            else "OPTED_IN"
        )

        records.append(
            {
                "consent_id": f"CONS-{i:06d}",
                "contact_id": contact.contact_id,
                "channel": "SALES_EMAIL",
                "status": status,
                "effective_date": "2026-01-01",
            }
        )

    return pd.DataFrame(records)


def generate_leads(
    n: int,
    contacts: pd.DataFrame,
    campaigns: pd.DataFrame,
    rng: random.Random,
) -> pd.DataFrame:
    """Generate leads linked to valid contacts and campaigns."""

    sources = [
        "Website",
        "Webinar",
        "Paid Search",
        "Referral",
        "Social Media",
    ]

    products = [
        "AI Analytics",
        "AI Automation",
        "Data Platform",
    ]

    reference_date = date(2026, 10, 27)
    contact_records = contacts.to_dict("records")
    campaign_ids = campaigns["campaign_id"].tolist()

    records = []

    for i in range(1, n + 1):
        contact = rng.choice(contact_records)

        # Leads created 0–180 days before the fixed reference date.
        age_days = rng.randint(0, 180)
        created_date = reference_date - timedelta(days=age_days)

        records.append(
            {
                "lead_id": f"LEAD-2026-{i:06d}",
                "contact_id": contact["contact_id"],
                "company_id": contact["company_id"],
                "campaign_id": rng.choice(campaign_ids),
                "source": rng.choice(sources),
                "product": rng.choice(products),
                "created_date": created_date.isoformat(),
                "status": "NEW",
                "is_stale": age_days > 30,
            }
        )

    return pd.DataFrame(records)

def generate_activities(
    leads: pd.DataFrame,
    rng: random.Random,
) -> pd.DataFrame:
    """Generate activity events linked to existing leads."""

    activity_types = [
        "EMAIL_OPEN",
        "EMAIL_CLICK",
        "PRICING_PAGE_VISIT",
        "CONTENT_DOWNLOAD",
        "WEBINAR_ATTENDANCE",
        "DEMO_REQUEST",
    ]

    weights = [25, 20, 20, 15, 12, 8]
    records = []

    for lead in leads.itertuples(index=False):
        # Generate 1–5 events per lead.
        event_count = rng.randint(1, 5)

        for sequence in range(1, event_count + 1):
            activity_type = rng.choices(
                activity_types,
                weights=weights,
                k=1,
            )[0]

            records.append(
                {
                    "activity_id": (
                        f"ACT-{lead.lead_id}-{sequence:03d}"
                    ),
                    "lead_id": lead.lead_id,
                    "activity_type": activity_type,
                    "activity_date": lead.created_date,
                    "occurred_after_conversion": False,
                }
            )

    return pd.DataFrame(records)


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic CRM master data."
    )
    parser.add_argument("--companies", type=int, default=5000)
    parser.add_argument("--contacts", type=int, default=10000)
    parser.add_argument("--campaigns", type=int, default=20)
    parser.add_argument("--leads", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=SEED)

    args = parser.parse_args()

    if min(
        args.companies,
        args.contacts,
        args.campaigns,
        args.leads,
    ) < 1:
        parser.error("All record counts must be at least 1.")

    rng = random.Random(args.seed)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate parent/master records first.
    companies = generate_companies(args.companies, rng)
    contacts = generate_contacts(args.contacts, companies, rng)
    campaigns = generate_campaigns(args.campaigns)

    # Generate dependent records after their parents exist.
    consents = generate_consents(contacts)
    leads = generate_leads(
        args.leads, contacts, campaigns, rng
    )
    activities = generate_activities(leads, rng)

    companies.to_csv(OUTPUT_DIR / "companies.csv", index=False)
    contacts.to_csv(OUTPUT_DIR / "contacts.csv", index=False)
    campaigns.to_csv(OUTPUT_DIR / "campaigns.csv", index=False)
    consents.to_csv(OUTPUT_DIR / "consents.csv", index=False)
    leads.to_csv(OUTPUT_DIR / "leads.csv", index=False)
    activities.to_csv(OUTPUT_DIR / "activities.csv", index=False)

    print("Synthetic CRM data generation completed.")
    print(f"Companies: {len(companies):,}")
    print(f"Contacts: {len(contacts):,}")
    print(f"Campaigns: {len(campaigns):,}")
    print(f"Consents: {len(consents):,}")
    print(f"Leads: {len(leads):,}")
    print(f"Activities: {len(activities):,}")
    print(f"Output directory: {OUTPUT_DIR}")



if __name__ == "__main__":
    main()
