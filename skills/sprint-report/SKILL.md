---
name: sprint-report
description: >
  Write the summary report for a Connect sprint that has just closed in Jira: what was
  completed, what wasn't (and where it went), the general areas of work, which epics were
  fully finalized, and how the sprint split across stories, tasks and bugs. Use when a sprint
  closes (on Sift's schedule it checks for newly closed sprints), or when asked for a "sprint
  report", "sprint summary", "what did we finish in Sprint 101" or "how did the sprint go".
---

# Sprint report — Sift

Read-only. Jira is only read (`bin/sift-jira sprints`, `sprint-data`); nothing is written to
Jira. The report is a draft: sending it anywhere beyond the turn's reply (email, a shared
doc) needs the human's approval like any other outbound action.

Read first:
- `context/delivery-model.md`: teams, sprint cadence, what each status means
- `context/2027-themes.md`: the five goals, for naming the areas of work
- `context/capacity-snapshot.md`: the sprint's commitment and velocity, if it covers this sprint

## 1. Find sprints that need a report
**One report covers one pod: Blue, Green or Mobile, never a mix.** Each pod closes its own
sprint under a shared number, usually within a day of the others. Blue and Green sometimes
share a single Jira sprint, so a sprint's name or board does not tell you whose work it holds.
**The Jira `Team` field does** (`Connect: Blue Web Team`, `Connect: Green Web Team`,
`Connect: Mobile Team`). A pod's report contains only tickets whose Team is that pod.
```bash
bin/sift-jira sprints --state closed --since <14 days ago>
```
- Each pod with a closed sprint gets its own report, written separately and never combined.
  A sprint shared by Blue and Green is reported once for each pod, with that pod's `--team`.
- Skip any pod-sprint already reported: `canopy cursor since sprint-report --local ~/.sift/state --items - < "$T/closed.json"`
  (id = `<sprintId>-<pod>`, `ts` = the sprint's `completed` time). A named request ("Green
  Sprint 101") skips the cursor. If the asker doesn't name a pod, list the pods with closed
  sprints and ask which, or write one report per pod, each stand-alone.

## 2. Pull the data
```bash
bin/sift-jira sprint-data <sprintId> --team Blue|Green|Mobile
```
The output already does the counting. Use it as it is; don't recount from the issue list.
- `completed`: Done by the time the sprint closed. `finished_after_close`: carried over, then
  done since. `dropped`: closed as Won't Do / Duplicate and never counts as delivered work.
  Everything else is **not completed**, with `carried_to` naming the sprint it moved to (empty
  means it went back to the backlog).
- `mix_all` is the committed mix, `mix_completed` is the delivered mix, in issues and Story
  Points, by Story / Task / Bug / Design / Test / Other. `mix_all` includes dropped tickets, so
  subtract them for "committed". `unpointed` counts tickets with no estimate, so points
  understate the mix wherever it is above zero (Bugs are mostly unpointed).
- `epics`: per epic, how many children are done and `fully_finalized` (every child done and at
  least one finished this sprint). Children can belong to other pods, so say "all children done",
  not "this pod finished it".
- `excluded_other_or_no_team`: tickets in the sprint whose Team is another pod or empty. They
  are NOT in the report's numbers. List them in one line at the end ("not counted: CCCT-2980,
  no Team set") so the pod can fix the field.
- Limits worth stating once: tickets removed from the sprint mid-way don't show up (Jira keeps no
  membership for them in a search).

## 3. Write the report
Plain language for product people, who read the ticket keys, not the tool output. Link every key
as `https://dimagi.atlassian.net/browse/<KEY>`. Keep it to what a PM can read in two minutes.

```
# <Pod> Sprint <N> report — <date range>

**Overall:** <issues completed>/<committed> tickets (<points completed>/<points> pts)
for the <pod> pod. <One or two sentences: the headline, e.g. a strong sprint, or most of the
miss is one epic.>

## What was completed
<Grouped by area of work, not by ticket order. One line per ticket: key, plain-language summary,
who. Say when a group of tickets together delivers something a PM would name.>

## What was not completed
<Each ticket: key, summary, status when the sprint closed, and where it went (next sprint /
backlog). Group by reason when it is plain from the ticket (blocked, started late, bigger than
estimated, bug found late); otherwise don't guess. Won't Do / Duplicate tickets go in a
separate one-line "closed without delivery" note, not here.>

## Areas of work
<3–6 themes the sprint touched, each with ticket count and share of the sprint. Name the 2027
goal each one serves where it plainly does (`context/2027-themes.md`); say "no clear goal"
for platform upkeep and don't force a fit.>

## Epics
- **Fully finalized:** <epic key, name, N of N children done. Or "None this sprint".>
- **Moved forward:** <epic, children done / total, what's left. Only epics with work this sprint.>

## Stories, tasks and bugs
| | Committed | Completed | Share of completed |
|---|---|---|---|
| Stories | n (pts) | n (pts) | % |
| Tasks | | | |
| Bugs | | | |
| Design / Other | | | |
<One sentence on what the split says, e.g. a bug-heavy sprint. Use issue counts for the share
and add points only where most tickets are pointed. Say which one you used.>

## Not counted
<Tickets in the sprint filed under another team or no team, one line. Omit if none.>
```
Rules:
- Count only what the data says. A ratio like "73% complete" needs the numerator and the
  denominator next to it.
- Don't judge people or teams. Say what slipped and where it went, not who failed.
- Measure "areas of work" from the epics and components first. Group tickets with no epic by
  their summary and label them as your grouping.
- Flag anything that conflicts with `context/decisions.md` or the Product Principles, the same
  as in any other skill. Don't re-litigate.
- If the sprint's commitment or velocity is in the capacity snapshot, give one line comparing
  delivered points with it. If the snapshot predates the sprint, skip the comparison.

## 4. Present and record
Put the report in the turn's reply (canopy-web relays it to the asker). If the turn was
scheduled rather than asked, draft it and wait for approval before it goes anywhere else.

After the report is delivered, mark the sprints done so the next run skips them:
`canopy cursor bump sprint-report --local ~/.sift/state --items - < "$T/closed.json"`.
