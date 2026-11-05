import pytest

from pilot_analytics import run_user_scenario


def test_complete_activation_is_valid_and_activated():
    result = run_user_scenario("complete_activation")

    assert result["violations"] == []
    assert result["funnel"]["activated_sessions"] == 1


def test_orphan_delivery_is_not_activation():
    result = run_user_scenario("orphan_delivery")

    assert result["funnel"]["activated_sessions"] == 0


@pytest.mark.parametrize(
    ("scenario", "violation"),
    [
        ("missing_evidence", "claim_without_source"),
        ("missing_risk", "scenario_without_risk_warning"),
        ("guarantee_language", "guarantee_language"),
    ],
)
def test_invalid_briefs_are_reported(scenario, violation):
    assert violation in run_user_scenario(scenario)["violations"]


def test_repeat_session_counts_two_activated_sessions():
    result = run_user_scenario("repeat_session")

    assert result["funnel"]["activated_sessions"] == 2
    assert result["funnel"]["stages"]["brief_delivered"] == 2


def test_unknown_scenario_is_rejected():
    with pytest.raises(ValueError, match="Unknown scenario"):
        run_user_scenario("unknown")
