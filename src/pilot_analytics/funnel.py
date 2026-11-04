"""Funnel summary from raw pilot events. STUB: the tests come first; the agent implements this."""

from __future__ import annotations

STAGES = [
    "landing_viewed",
    "instrument_selected",
    "input_submitted",
    "brief_requested",
    "brief_delivered",
]
COMMON_FIELDS = ["event_name", "event_time", "session_id", "experiment_variant", "device_class"]


def funnel_summary(events: list[dict]) -> dict:
    raise NotImplementedError("write the tests first, then implement")
