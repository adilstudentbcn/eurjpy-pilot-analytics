# Feature extraction — multi-market trading intelligence terminal

## Method and evidence

The notebook's Block 5b fetched a live App Store snapshot on 2026-10-29:

- 8 habit apps
- 400 reviews
- Mean rating: 3.68
- 12 transparent lexicon features

The lexicon identifies feature mentions in descriptions and reviews. It is reproducible and interpretable, but it can miss paraphrases. The optional LLM cross-check was skipped because no API key was available; therefore, lexicon/LLM agreement is **not established**.

This is indirect evidence from habit apps. It informs workflow and coaching hypotheses, not the demand level for trading software.

## Features extracted

| Existing-app feature | Trading-product analogue | Evidence status |
|---|---|---|
| Reminders | Session alerts, event alerts, risk warnings | Lexicon |
| Streaks / progress | Trading journal history, process consistency, performance review | Lexicon |
| Social accountability | Shared watchlists, educator/community workflows | Lexicon |
| Coaching guidance | Scenario explanation, entry/stop/target reasoning, follow-up chat | Lexicon |
| Flexible schedule | Pre-session planning and asynchronous alerts | Lexicon |
| Sync/backup | Saved instruments, history, and preferences across devices | Lexicon |
| Widgets/watch | Compact watchlist and market-risk view | Lexicon |
| Price/subscription | Subscription and plan objections | Lexicon |
| AI | AI-assisted synthesis and explanation | Lexicon; low review frequency |

## Overall review salience

The most frequent lexicon topics were:

1. Price/subscription — 23.2%
2. Flexible schedule — 8.8%
3. Gamification — 8.0%
4. Social accountability and progress — 6.2% each
5. Widgets/watch — 6.0%

These are shares of the 400 reviews mentioning a feature and are not market shares or willingness-to-pay rates.

## Group signals

The notebook used cue words to identify reviews that mentioned students, remote workers, parents, or health/older users. Reviews per group were:

| Group | Reviews | Strongest relative mentions |
|---|---:|---|
| Students | 6 | Mood/self-care, sync/backup, flexible schedule |
| Remote workers | 5 | Mood/self-care, social accountability, streaks |
| Parents | 9 | Social accountability, gamification, coaching guidance |
| Health/55+ | 0 | No evidence; treated as unknown, not as zero demand |

The strongest relative coaching relevance weights were students 0.74, remote workers 1.27, parents 1.78, and health/55+ 1.00 neutral. The group samples are too small for reliable product decisions; the notebook labels most Kano classifications as “too few.” The only clear classification was social accountability for parents as a possible delighter.

## Product implications to test

1. Prioritise a concise risk brief, alerts, and explanation before adding social or gamification features.
2. Treat price transparency and subscription value as a first-class research question.
3. Test pre-session planning and asynchronous alerts for part-time traders.
4. Test educator/community workflows separately from individual traders.
5. Do not claim feature importance for health/55+ or any trading niche from this dataset.

## Validation status

- Lexicon extraction: completed.
- LLM agreement check: not completed; no API key.
- Trading-specific feature evidence: not yet collected.
- Feature priorities above: research hypotheses, not market-level facts.
