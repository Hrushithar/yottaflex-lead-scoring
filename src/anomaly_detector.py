
import json


def detect_anomaly(issue_type, details):
    """Return True when the supplied test case violates a business rule."""

    if issue_type == "OPTED_OUT_LEAD_CONTACTED":
        return (
            details.get("attempted_contact") is True
            and details.get("channel") == "SALES_EMAIL"
            and details.get("consent_status") == "OPTED_OUT"
        )

    if issue_type == "POST_CONVERSION_EVENT_USED":
        return (
            details.get("score_includes_event") is True
            and details.get("activity_date", "")
            > details.get("conversion_date", "")
        )

    if issue_type == "LEAD_OUTSIDE_TERRITORY":
        return (
            details.get("company_territory")
            != details.get("incorrect_rep_territory")
            and details.get("incorrect_rep_id") is not None
        )

    if issue_type == "DUPLICATE_OPPORTUNITY":
        return (
            details.get("same_lead_id") is True
            and details.get("original_opportunity_id")
            != details.get("duplicate_opportunity_id")
        )

    if issue_type == "STAGE_HISTORY_GAP":
        sequences = details.get("test_sequences", [])
        expected = list(range(min(sequences), max(sequences) + 1)) if sequences else []
        return sequences != expected

    return False


def detect_fixture_row(row):
    details = json.loads(row["details_json"])
    return detect_anomaly(row["issue_type"], details)
