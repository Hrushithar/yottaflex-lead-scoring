from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/output")


def generate_opportunities(
    routing: pd.DataFrame,
    activities: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create deterministic opportunities and stage history."""

    # Only assigned leads are eligible to enter the sales pipeline.
    eligible = routing[
        routing["routing_status"].eq("ASSIGNED")
    ].copy()

    # Use all assigned leads as the initial candidate pool.
    # A demo request is a strong signal, but not the only
    # possible qualification signal.
    demo_leads = set(
        activities.loc[
            activities["activity_type"].eq("DEMO_REQUEST"),
            "lead_id",
        ]
    )

    eligible["has_demo_request"] = eligible["lead_id"].isin(
        demo_leads
    )

    # Prioritize stronger buying signals, then score and ID.
    eligible = eligible.sort_values(
        ["has_demo_request", "lead_score", "lead_id"],
        ascending=[False, False, True],
    )

    # Keep unique leads and create no more than one opportunity
    # per lead in this initial model.
    eligible = eligible.drop_duplicates("lead_id").head(3000)

    opportunities = []
    stage_history = []

    for i, lead in enumerate(
        eligible.itertuples(index=False), start=1
    ):
        opportunity_id = f"OPP-2026-{i:06d}"

        # Outcomes are derived from an explicit, reproducible rule.
        score = int(lead.lead_score)

        if score >= 85:
            outcome = "WON"
            lost_reason = None
        elif score >= 70:
            outcome = "LOST"
            lost_reason = "BUDGET_CONSTRAINT"
        else:
            outcome = "OPEN"
            lost_reason = None

        opportunities.append(
            {
                "opportunity_id": opportunity_id,
                "lead_id": lead.lead_id,
                "company_id": lead.company_id,
                "sales_rep_id": lead.sales_rep_id,
                "product": lead.product,
                "amount": 10000 + score * 1000,
                "stage": outcome,
                "outcome": outcome,
                "lost_reason": lost_reason,
            }
        )

        stages = ["QUALIFICATION", "PROPOSAL", outcome]

        for sequence, stage in enumerate(stages, start=1):
            stage_history.append(
                {
                    "stage_history_id": (
                        f"SH-{opportunity_id}-{sequence:02d}"
                    ),
                    "opportunity_id": opportunity_id,
                    "stage": stage,
                    "sequence": sequence,
                }
            )

    return (
        pd.DataFrame(opportunities),
        pd.DataFrame(stage_history),
    )


def main():
    routing = pd.read_csv(DATA_DIR / "lead_routing.csv")
    activities = pd.read_csv(DATA_DIR / "activities.csv")

    opportunities, history = generate_opportunities(
        routing, activities
    )

    opportunities.to_csv(
        DATA_DIR / "opportunities.csv", index=False
    )
    history.to_csv(
        DATA_DIR / "stage_history.csv", index=False
    )

    print("Opportunity generation completed.")
    print(f"Opportunities: {len(opportunities):,}")
    print("\nOutcomes:")
    print(opportunities["outcome"].value_counts().to_string())


if __name__ == "__main__":
    main()
