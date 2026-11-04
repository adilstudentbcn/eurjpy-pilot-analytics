# Pilot event schema

## Purpose

Record the validation funnel without storing personal data, credentials, raw broker identifiers, or unnecessary uploaded content. Use a random `session_id` for each pilot session.

## Common fields

| Field | Type | Rule |
|---|---|---|
| `event_name` | string | One name from the event table |
| `event_time` | ISO timestamp | UTC |
| `session_id` | random string | No email, account name, or broker ID |
| `experiment_variant` | string | Landing-page and price variant |
| `device_class` | enum | `phone`, `laptop`, `tablet`, `unknown` |
| `asset_category` | enum/null | `forex`, `stock_index`, `commodities`, `crypto`, `multi_asset` |
| `instrument` | string/null | Selected instrument; do not record account identifiers |

## Events

| Event | Required properties | Success meaning |
|---|---|---|
| `landing_viewed` | common fields | Visit reached |
| `instrument_selected` | `instrument`, `asset_category` | User starts a workflow |
| `input_intent_recorded` | `input_types` | User says they can upload/connect inputs |
| `input_submitted` | `input_types`, `input_count` | At least one real input submitted |
| `brief_requested` | `input_count` | User requests analysis |
| `brief_delivered` | `brief_id`, `missing_input_count` | Analysis result returned |
| `brief_usefulness_rated` | `rating`, `rating_reason` | User reports perceived usefulness |
| `risk_detail_opened` | `brief_id`, `risk_type` | User inspects a risk or uncertainty |
| `follow_up_submitted` | `brief_id`, `question_topic` | User challenges or asks for explanation |
| `return_session_started` | `days_since_prior_session` | User returns |
| `paid_intent_recorded` | `price_variant`, `intent_type` | Pre-order, waitlist, or interview request |
| `qualified_interview_completed` | `workflow_completed`, `repeated_problem` | Interview meets the pilot qualification rules |

## Data-quality rules

- Do not count a `brief_delivered` event as activation unless `instrument_selected` and `input_submitted` occurred in the same session.
- Keep event counts and unique-session counts separate.
- Record failures as explicit events with a reason category; do not convert failures into successful delivery.
- Preserve raw event data and generate funnel summaries from code.
- Report sample size, missing fields, date range, and experiment variant with every result.
