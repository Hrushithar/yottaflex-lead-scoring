
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/output")

# Transparent, versioned scoring configuration.
SCORE_RULES = {
    "version": "1.0",
    "fit_max": 30,
    "intent_max": 40,
    "engagement_max": 30,
}

HIGH_INTENT_EVENTS = {
    "DEMO_REQUEST": 40,
    "PRICING_PAGE_VISIT": 20,
    "WEBINAR_ATTENDANCE": 15,
    "CONTENT_DOWNLOAD": 10,
    "EMAIL_CLICK": 10,
    "EMAIL_OPEN": 5,
}

ENGAGEMENT_EVENTS = {
    "EMAIL_OPEN": 2,
    "EMAIL_CLICK": 5,
    "PRICING_PAGE_VISIT": 5,
    "CONTENT_DOWNLOAD": 4,
    "WEBINAR_ATTENDANCE": 6,
    "DEMO_REQUEST": 8,
}


def calculate_scores(
    leads: pd.DataFrame,
    companies: pd.DataFrame,
    activities: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate reproducible fit, intent and engagement scores."""

    # Each lead must reference an existing company.
    company_data = companies[
        ["company_id", "industry", "employee_count"]
    ]

    scored = leads.merge(
        company_data,
        on="company_id",
        how="left",
        validate="many_to_one",
        indicator=True,
    )

    if (scored["_merge"] != "both").any():
        raise ValueError("Some leads reference missing companies.")

    scored = scored.drop(columns="_merge")

    # FIT: target industries and company size.
    target_industries = {"Technology", "Finance", "Healthcare"}

    scored["fit_score"] = (
        scored["industry"].isin(target_industries).astype(int) * 20
        + scored["employee_count"].ge(50).astype(int) * 10
    )

    # Aggregate activity evidence per lead.
    events = activities.copy()

    # Prevent future information from influencing the score.
    events["activity_date"] = pd.to_datetime(
        events["activity_date"], errors="raise"
    )
    events["created_date"] = pd.to_datetime(
        events["lead_id"].map(
            leads.set_index("lead_id")["created_date"]
        ),
        errors="raise",
    )

    valid_events = events[
        events["activity_date"] <= events["created_date"]
    ].copy()

    # INTENT: stronger buying signals receive higher points.
    valid_events["intent_points"] = (
        valid_events["activity_type"]
        .map(HIGH_INTENT_EVENTS)
        .fillna(0)
    )

    intent = valid_events.groupby("lead_id")[
        "intent_points"
    ].sum()

    scored["intent_score"] = (
        scored["lead_id"].map(intent).fillna(0).clip(upper=40)
    )

    # ENGAGEMENT: reward activity, with a maximum of 30.
    valid_events["engagement_points"] = (
        valid_events["activity_type"]
        .map(ENGAGEMENT_EVENTS)
        .fillna(0)
    )

    engagement = valid_events.groupby("lead_id")[
        "engagement_points"
    ].sum()

    scored["engagement_score"] = (
        scored["lead_id"]
        .map(engagement)
        .fillna(0)
        .clip(upper=30)
    )

    scored["lead_score"] = (
        scored["fit_score"]
        + scored["intent_score"]
        + scored["engagement_score"]
    ).clip(upper=100).astype(int)

    scored["priority"] = pd.cut(
        scored["lead_score"],
        bins=[-1, 39, 69, 100],
        labels=["LOW", "MEDIUM", "HIGH"],
    ).astype(str)

    scored["score_rule_version"] = SCORE_RULES["version"]

    return scored


def main():
    leads = pd.read_csv(DATA_DIR / "leads.csv")
    companies = pd.read_csv(DATA_DIR / "companies.csv")
    activities = pd.read_csv(DATA_DIR / "activities.csv")

    scores = calculate_scores(leads, companies, activities)

    output = scores[
        [
            "lead_id",
            "company_id",
            "fit_score",
            "intent_score",
            "engagement_score",
            "lead_score",
            "priority",
            "score_rule_version",
        ]
    ]

    output.to_csv(DATA_DIR / "lead_scores.csv", index=False)

    print("Lead scoring completed.")
    print(f"Scored leads: {len(output):,}")
    print("\nPriority distribution:")
    print(output["priority"].value_counts().to_string())
    print("\nAverage score:", round(output["lead_score"].mean(), 2))
    print(f"Saved to {DATA_DIR / 'lead_scores.csv'}")


if __name__ == "__main__":
    main()
