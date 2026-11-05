"""Deterministic simulated user journeys for the pilot."""

from __future__ import annotations

from copy import deepcopy

from .brief import validate_brief
from .funnel import funnel_summary

SCENARIOS = (
    "complete_activation",
    "orphan_delivery",
    "missing_evidence",
    "missing_risk",
    "guarantee_language",
    "repeat_session",
)

_BASE_BRIEF = {
    "instrument": "EUR/JPY",
    "analysis_time": "2026-11-03T07:30:00Z",
    "evidence": [{"claim": "Scheduled event", "source": "simulated calendar input"}],
    "scenarios": [
        {
            "name": "range holds",
            "invalidation": "15m close above the session high",
            "risk_warning": "Simulated levels can be wrong; check them yourself.",
        }
    ],
}


def _event(name: str, session_id: str, minute: int) -> dict:
    return {
        "event_name": name,
        "event_time": f"2026-11-03T08:{minute:02d}:00Z",
        "session_id": session_id,
        "experiment_variant": "simulated",
        "device_class": "laptop",
    }


def run_user_scenario(name: str) -> dict:
    """Run one local journey and return its events, brief, and validation results."""
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario {name!r}; choose from {', '.join(SCENARIOS)}")

    events = [
        _event("landing_viewed", "session-1", 0),
        _event("instrument_selected", "session-1", 1),
        _event("input_submitted", "session-1", 2),
        _event("brief_requested", "session-1", 3),
        _event("brief_delivered", "session-1", 4),
    ]
    brief = deepcopy(_BASE_BRIEF)

    if name == "orphan_delivery":
        events = [
            _event("landing_viewed", "session-1", 0),
            _event("brief_delivered", "session-1", 1),
        ]
    elif name == "missing_evidence":
        brief["evidence"][0].pop("source")
    elif name == "missing_risk":
        brief["scenarios"][0].pop("risk_warning")
    elif name == "guarantee_language":
        brief["scenarios"][0]["name"] = "guaranteed breakout"
    elif name == "repeat_session":
        events.extend(
            [
                _event("landing_viewed", "session-2", 10),
                _event("instrument_selected", "session-2", 11),
                _event("input_submitted", "session-2", 12),
                _event("brief_requested", "session-2", 13),
                _event("brief_delivered", "session-2", 14),
            ]
        )

    return {
        "scenario": name,
        "events": events,
        "brief": brief,
        "violations": validate_brief(brief),
        "funnel": funnel_summary(events),
    }
