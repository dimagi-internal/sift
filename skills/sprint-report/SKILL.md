---
name: sprint-report
description: >
  Write the summary report for a Connect sprint that has just closed in Jira: what was
  completed, what carried over, the areas of work and the 2027 goals they serve, which epics
  finished, and the story / task / bug split. One pod per report, kept short. Use when a sprint
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
A short summary a PM reads in a minute, in the style of the team's earlier Slack summaries
(Sprint 98). Ticket keys go in the "Details" line only, not in the body. Write for people who
don't read Jira: say what changed for workers, LLOs or staff, not what the ticket was called.

Format (Slack: emoji shortcodes, no headings or tables, one pod only):
```
*Sprint <N> Summary — <Mon D> – <Mon D>, <year>*
:iphone: *Mobile Pod*   (or :globe_with_meridians: Blue Pod / Green Pod)

:<emoji>: *<Area of work>* | <One sentence on what was delivered, in plain language.>
:<emoji>: *<Area of work>* | ...            (4–6 lines, biggest first)
:<emoji>: *<Area still open>* | Still to come: <what's left>.

<Paragraph, 4–6 sentences: "Sprint <N> was a <steady/high-output/slower> sprint for the <pod>
pod, with <X> of <Y> issues closed — highlighted by <the biggest delivery>." Then what else
shipped, and which items carry into the next sprint and why (in QA, blocked, not started).>

*Mix:* <S> stories, <T> tasks, <B> bugs<, D design> closed of <S'>/<T'>/<B'> committed (<pts> of <pts'> pts).
*Goals:* <one line: which of the five 2027 goals the sprint moved, e.g. "Goal 4 (LLO network):
LLO Directory and Solicitations. The rest is upkeep.">
*Epics finished:* <epic names, or "none">.
_Details: <KEY>, <KEY> ... carried over · <KEY> not counted (no Team)_
```
Rules:
- **Concise.** The whole report should fit one screen. Group tickets into areas of work (epic
  and component first; label your own grouping when tickets have no epic). Don't list tickets
  one by one.
- Issue counts in the paragraph are *closed of committed*, with Won't Do / Duplicate tickets
  left out of "committed". Say so only if it changes the picture.
- A ticket finished after the sprint closed counts as carried over, and the paragraph says it
  finished since.
- The Mix line gives story / task / bug counts and points, from `mix_completed` and `mix_all`.
  Bugs are mostly unpointed, so don't quote a bug share of points.
- Goals come from `context/2027-themes.md`. Name a goal only where the work plainly serves it;
  say "upkeep" for the rest and don't force a fit. Flag anything that conflicts with the
  Product Principles or `context/decisions.md`, the same as in any other skill.
- An epic is "finished" only when `fully_finalized` is true and the epic wasn't already done
  before this sprint began.
- Tickets in `excluded_other_or_no_team` are not in the numbers. Name them in the Details line.
- Don't judge people. Say what slipped and where it went, not who is behind.

## 4. Present and record
Put the report in the turn's reply (canopy-web relays it to the asker). If the turn was
scheduled rather than asked, draft it and wait for approval before it goes anywhere else.

After the report is delivered, mark the sprints done so the next run skips them:
`canopy cursor bump sprint-report --local ~/.sift/state --items - < "$T/closed.json"`.
