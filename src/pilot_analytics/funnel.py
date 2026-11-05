"""Funnel summary from raw pilot events."""

from __future__ import annotations

from datetime import datetime
from itertools import pairwise

STAGES = [
    "landing_viewed",
    "instrument_selected",
    "input_submitted",
    "brief_requested",
    "brief_delivered",
]
COMMON_FIELDS = ["event_name", "event_time", "session_id", "experiment_variant", "device_class"]


def funnel_summary(events: list[dict]) -> dict:
    sessions_by_stage = {stage: set() for stage in STAGES}
    for event in events:
        session_id = event.get("session_id")
        if session_id and event.get("event_name") in sessions_by_stage:
            sessions_by_stage[event["event_name"]].add(session_id)

    stages = {stage: len(sessions_by_stage[stage]) for stage in STAGES}
    rates = {}
    for previous, current in pairwise(STAGES):
        denominator = stages[previous]
        rates[current] = None if denominator == 0 else stages[current] / denominator

    session_events = {}
    for event in events:
        session_id = event.get("session_id")
        if session_id:
            session_events.setdefault(session_id, set()).add(event.get("event_name"))
    activated_sessions = sum(
        all(
            stage in session_events.get(session_id, set())
            for stage in (
                "instrument_selected",
                "input_submitted",
                "brief_delivered",
            )
        )
        for session_id in session_events
    )

    missing_fields = {
        field: sum(not event.get(field) for event in events) for field in COMMON_FIELDS
    }
    timestamps = []
    for event in events:
        value = event.get("event_time")
        if value:
            try:
                timestamps.append(datetime.fromisoformat(value))
            except ValueError:
                continue

    date_range = None
    if timestamps:
        date_range = {
            "start": min(timestamps).isoformat().replace("+00:00", "Z"),
            "end": max(timestamps).isoformat().replace("+00:00", "Z"),
        }

    return {
        "n_events": len(events),
        "stages": stages,
        "rates": rates,
        "activated_sessions": activated_sessions,
        "missing_fields": missing_fields,
        "date_range": date_range,
    }


def calculate_funnel_dropoff(frame) -> dict:
    """Calculate step-by-step conversion rates from a DataFrame-like object."""
    results = {}
    previous_users = None
    for _, row in frame.iterrows():
        stage = row["stage"]
        users = row["users"]
        if previous_users is None or previous_users == 0:
            rate = 1.0
        else:
            rate = users / previous_users
        results[stage] = {"users": users, "conversion_rate": rate}
        previous_users = users
    return results
