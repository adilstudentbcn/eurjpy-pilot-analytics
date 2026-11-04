from pilot_analytics import funnel_summary


def ev(name, session, t="2026-11-03T08:00:00Z"):
    return {
        "event_name": name,
        "event_time": t,
        "session_id": session,
        "experiment_variant": "A",
        "device_class": "laptop",
    }


def test_delivery_without_instrument_and_input_is_not_activation():
    """S1: a delivered brief alone is not activation."""
    events = [
        ev("landing_viewed", "full"),
        ev("instrument_selected", "full"),
        ev("input_submitted", "full"),
        ev("brief_requested", "full"),
        ev("brief_delivered", "full"),
        ev("brief_delivered", "orphan"),  # delivered, never selected or submitted
    ]
    assert funnel_summary(events)["activated_sessions"] == 1


def test_counts_unique_sessions_not_events():
    """S2: three landing events from one session = 1 session, 3 events."""
    events = [ev("landing_viewed", "s1") for _ in range(3)]
    out = funnel_summary(events)
    assert out["stages"]["landing_viewed"] == 1
    assert out["n_events"] == 3


def test_rate_is_none_when_denominator_is_zero():
    """S3: nobody selected an instrument, so the next rate is unknown, not 0."""
    out = funnel_summary([ev("landing_viewed", "s1")])
    assert out["rates"]["input_submitted"] is None
