# Connect capacity snapshot

**Snapshot as of 2026-11-03 (Sprint 102 in progress).** Refresh with `skills/capacity-refresh`
when this is over 14 days old or a new sprint has started. Source: the
[Connect Tech Sprint Performance dashboard](https://sites.google.com/dimagi.com/connect-sprint-performance/connect-sprint-metrics)
(engineering's own numbers — prefer them over anything Sift derives from Jira).

## Sprint velocity, commitment and capacity
Capacity = team-days available (PTO and allocations already netted out). Velocity = story
points done. Mobile = Mobile Team; Web = Blue + Green web teams combined.

| Sprint | Dates | Capacity (Tot / Mob / Web) | Commitment (Tot / Mob / Web) | Velocity (Tot / Mob / Web) | % complete (Tot / Mob / Web) |
|---|---|---|---|---|---|
| S103 (upcoming) | 16–30 Nov | 76 / 25 / 51 | — | est. 85 / 33 / 52 | — |
| S102 (in progress) | 2–16 Nov | 79 / 27 / 52 | 163 / 52 / 111 | — | — |
| S101 | 19 Oct–2 Nov | 94 / 34 / 60 | 134 / 56 / 78 | 97 / 45 / 52 | 72% / 80% / 67% |
| S100 | 5–19 Oct | 87 / 29 / 58 | 94 / 25 / 69 | 88 / 42 / 46 | 94% / 168% / 67% |
| S99 | 21 Sep–5 Oct | 73 / 35 / 38 | 122 / 66 / 56 | 99 / 60 / 39 | 81% / 91% / 70% |
| S98 | 7–21 Sep | 60 / 30 / 30 | 99 / 46 / 53 | 63 / 29 / 34 | 64% / 63% / 64% |
| S97 | 24 Aug–7 Sep | 66 / 36 / 30 | 127 / 52 / 75 | 79 / 42 / 37 | 62% / 81% / 49% |
| S96 | 10–24 Aug | 106 / 37 / 69 | 136 / 50 / 86 | 72 / 25 / 47 | 53% / 50% / 55% |
| S95 | 27 Jul–10 Aug | 100 / 37 / 63 | 133 / 48 / 85 | 91 / 27 / 64 | 68% / 56% / 75% |
| S94 | 13–27 Jul | 108 / 35 / 73 | 125 / 47 / 78 | 92 / 33 / 59 | 74% / 70% / 76% |
| S93 | 29 Jun–13 Jul | 111 / 39 / 72 | 122 / 47 / 75 | 108 / 41 / 67 | 89% / 87% / 89% |
| S92 | 15–29 Jun | 105 / 38 / 67 | 114 / 47 / 67 | 108 / 39 / 69 | 95% / 83% / 103% |

**Read-outs (S92–S101):**
- **Throughput:** ~90 pts/sprint combined (range 63–108). Mobile ~38 (25–60), Web ~51 (34–69).
- **Rolling velocity per team-day:** 0.92 total (target ≥ 1.0). Mobile 1.36, Web 0.95 (5-sprint
  rolling). The dashboard's estimate for a sprint = rolling vel/day × capacity days.
- **Over-commitment is the norm:** commitment exceeds delivered velocity most sprints; %
  complete averages ~75% against an 80% target. Web runs below Mobile on completion. S102
  commits 163 pts against an estimated ~85–100 → expect ~55–65% completion.
- **Capacity dipped Aug–Sep** (60–73 days in S97–S99, down from ~105) and is ~76–94 now.

**S103 capacity notes:** Dave (Mobile) and Charl (Web Blue) each allocate 20% to the AI
workgroup. PTO — Mobile: Conroy, Shubham · Blue: Ajeet, Pawan, Sravan · Green: Zandre.

## Flow (CCCT Story/Task/Bug)
- 140 open; median backlog age 35 days; ~43 of them are 90+ days old (the largest age bucket).
- **Median lead time 39.6 days** (created → resolved); **median cycle time 8.8 days**
  (In Progress → resolved). Most of a ticket's life is waiting, not being worked.
- Resolved ~15–27 per week in Sep–Oct while ~25–33 were created → the backlog is growing.

## Discovery funnel (CCC → CCCT)
- 416 CCC ideas: ~223 backlog, ~45 in progress, ~148 done.
- **Median discovery lead time 14.9 days** (idea created → CCCT ticket created); **median
  build lead time 68.3 days** (CCCT ticket created → resolved). Only 1 idea in Technical
  Specification or later has no linked CCCT ticket.

## Interrupts (CI project)
- 21 open (14 bugs, 5 tasks); 8 P3, 13 P4. Median age 20 days.
- Median interrupt cycle time **25.3 days**, up sharply since early October (was under 10).
  Open-bug count is steady at ~12–20/week.

## Quality
- 17 open pre-deploy bugs; 6 logged in S101; median bug cycle time 3.4 days.
- Escaped defect rate 0% for S96–S101; test automation covers 65% (16 of 25) of core workflows.
- Bugs logged peaked in S100 (~27), back to ~6 in S101.

## DORA (web, last 4 weeks)
- commcare-connect deploys 1.8/week, lead time 5.7 days; connect-id deploys 2.0/week, lead time
  5.6 days (both "High"). Incidents per deploy 0.00; MTTR not measured.
