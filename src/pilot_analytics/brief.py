"""Validate a brief against product-directive invariants 1-4."""

from __future__ import annotations

GUARANTEE_TERMS = ("guaranteed", "guarantee", "certain", "no-risk", "risk-free")


def validate_brief(brief: dict) -> list[str]:
    violations = []

    if not brief.get("instrument"):
        violations.append("missing_instrument")
    if not brief.get("analysis_time"):
        violations.append("missing_analysis_time")

    for evidence in brief.get("evidence", []):
        if not evidence.get("source"):
            violations.append("claim_without_source")
            break

    for scenario in brief.get("scenarios", []):
        if not scenario.get("invalidation"):
            violations.append("scenario_without_invalidation")
        if not scenario.get("risk_warning"):
            violations.append("scenario_without_risk_warning")

    searchable_text = str(brief).lower()
    if any(term in searchable_text for term in GUARANTEE_TERMS):
        violations.append("guarantee_language")

    return violations
