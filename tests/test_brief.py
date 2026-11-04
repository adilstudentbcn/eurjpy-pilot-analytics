from pilot_analytics import validate_brief


def good_brief():
    return {
        "instrument": "EUR/JPY",
        "analysis_time": "2026-11-03T07:30:00Z",
        "evidence": [{"claim": "BoJ speaks at 09:00", "source": "calendar screenshot"}],
        "scenarios": [
            {
                "name": "range holds",
                "invalidation": "15m close above the session high",
                "risk_warning": "Levels can be wrong; check them yourself.",
            }
        ],
    }


def test_a_complete_brief_has_no_violations():
    assert validate_brief(good_brief()) == []


def test_scenario_without_invalidation_is_flagged():
    """S4"""
    brief = good_brief()
    del brief["scenarios"][0]["invalidation"]
    assert "scenario_without_invalidation" in validate_brief(brief)


def test_guarantee_language_is_flagged():
    """S5"""
    brief = good_brief()
    brief["scenarios"][0]["name"] = "guaranteed breakout"
    assert "guarantee_language" in validate_brief(brief)


def test_missing_instrument_is_flagged():
    """S6"""
    brief = good_brief()
    del brief["instrument"]
    assert "missing_instrument" in validate_brief(brief)
