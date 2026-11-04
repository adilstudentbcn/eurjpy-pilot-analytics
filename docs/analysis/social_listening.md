# Social listening — multi-market trading intelligence terminal

## Method

Notebook Block 6 queried the Hacker News Algolia API on 2026-10-29 for:

- `habit tracker`
- `habit app`
- `habit tracking`
- `streaks app`
- `procrastination app`

The result contained **911 deduplicated comments** dated from 2023 onward. Cue words classified comments into candidate groups, and pain words included forgetting, quitting, guilt, broken streaks, annoyance, subscriptions, and expense.

Hacker News is useful for discovering jobs and pains, but it is not representative of traders or the general population. These results are `research` evidence for shape and ranking only.

## Share of voice and pain overlap

| Candidate group | Mentions | With pain | Share of classified mentions | Pain among mentions |
|---|---:|---:|---:|---:|
| Students | 55 | 7 | 25.9% | 12.7% |
| Remote workers | 84 | 16 | 39.6% | 19.0% |
| Parents | 51 | 14 | 24.1% | 27.5% |
| Health/55+ | 22 | 6 | 10.4% | 27.3% |

The share-of-voice ranges recorded in the notebook ledger widen each observed share by ±30% because the source is selective. These counts describe habit-app discussions, not trading audiences.

## Topics observed

The NMF topic scan surfaced:

- habit trackers, loops, and streaks
- procrastination and productivity
- quitting habits such as smoking or alcohol
- social accountability and feedback
- AI and daily task workflows
- subscription and app-quality concerns

## Exact anonymized quotes

Names and handles were not stored. The following excerpts are reproduced from public comments and shortened only to fit the research record:

> “Most habit trackers are built around a streak: miss one day and the big number goes back to zero, and that reset is often the moment people quit.”

> “I’ve tried Todoist, Notion, Pomodoro, habit trackers, morning routines, ‘don’t break the chain,’ Beeminder, public Twitter commitments. All abandoned within weeks.”

> “Many of your ideas ... I’d want a server. Habits Tracker, need to access from whatever device I’m on at that moment.”

> “There are no notifications.”

## Implications to test for the trading product

1. A rigid streak-style experience may punish missed sessions; trading workflows should support review and recovery rather than gamification.
2. Cross-device continuity and saved context may matter for traders moving between desktop and mobile.
3. Users may abandon systems that add another workflow without reducing manual effort.
4. For trading, the equivalent pain hypotheses are missed catalysts, fragmented context, unclear invalidation, and alert fatigue; none is measured by this dataset.

## Missing evidence

No direct forex, stock, commodity, or crypto trader conversations were used in this pass. The next research route should query trading-specific communities and conduct workflow interviews, preserving exact quotes without names and recording source/date for each quote.
