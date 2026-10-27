
from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("data/output")


def test_all_anomaly_fixtures_have_ground_truth():
    cases = pd.read_csv(OUTPUT_DIR / "anomaly_cases.csv")
    truth = pd.read_csv(OUTPUT_DIR / "ground_truth.csv")

    assert len(cases) == 5
    assert len(truth) == 5
    assert cases["case_id"].is_unique
    assert truth["case_id"].is_unique
    assert set(cases["case_id"]) == set(truth["case_id"])


def test_all_required_anomaly_types_exist():
    cases = pd.read_csv(OUTPUT_DIR / "anomaly_cases.csv")

    expected_types = {
        "OPTED_OUT_LEAD_CONTACTED",
        "POST_CONVERSION_EVENT_USED",
        "LEAD_OUTSIDE_TERRITORY",
        "DUPLICATE_OPPORTUNITY",
        "STAGE_HISTORY_GAP",
    }

    assert set(cases["issue_type"]) == expected_types


def test_ground_truth_labels_are_anomalies():
    truth = pd.read_csv(OUTPUT_DIR / "ground_truth.csv")

    assert (truth["ground_truth"] == "ANOMALY").all()
    assert truth["expected_detection"].notna().all()



from src.anomaly_detector import detect_fixture_row


def test_all_five_anomalies_are_detected():
    cases = pd.read_csv(OUTPUT_DIR / "anomaly_cases.csv")

    results = cases.apply(detect_fixture_row, axis=1)

    assert len(results) == 5
    assert results.all(), (
        "Undetected anomaly cases: "
        + ", ".join(cases.loc[~results, "case_id"].tolist())
    )


from src.anomaly_detector import detect_anomaly


def test_unknown_issue_type_is_not_flagged():
    details = {
        "attempted_contact": False,
        "channel": "SALES_EMAIL",
        "consent_status": "OPTED_IN",
    }

    assert detect_anomaly("UNKNOWN_ISSUE", details) is False
