# ADR-0001: Pilot analytics as a plain Python package, tested with pytest

## Context
The pilot needs trustworthy funnel numbers and a way to check that briefs respect the directive. The
terminal itself is a single HTML file that runs only inside claude.ai, which is hard to test automatically.

## Decision
Keep the measurable logic (funnel rules, brief invariants) in a standard-library Python package with
pytest tests. The HTML terminal stays outside this package.

## Consequences
Rules are testable and reviewable; no network or model calls in tests. The package cannot judge whether a
brief is *good*, only whether it breaks a stated invariant. A change of approach (a live service, a database)
needs a new ADR that supersedes this one; this one is not edited.
