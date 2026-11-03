# Connect delivery model — teams, cadence and how work flows

This file covers how Connect builds things: who the delivery teams are, what each status means,
and how a roadmap idea becomes shipped code. Use it to turn "this goal has 23 items" into "this
goal is overloaded for the people behind it", and to judge whether a ticket is stuck or just
waiting its turn.

**Current numbers live in [`context/capacity-snapshot.md`](capacity-snapshot.md)**: capacity,
velocity, throughput, lead and cycle time, interrupts, quality and DORA. They come from the
[Connect Tech Sprint Performance dashboard](https://sites.google.com/dimagi.com/connect-sprint-performance/connect-sprint-metrics)
and are kept fresh by `skills/capacity-refresh`. This file holds what changes rarely.

## Teams (Jira `Team`, `customfield_10001`)
| Team | Platform | People |
|---|---|---|
| Connect: Mobile Team | Android app, PersonalID | Jignesh Tank, Shubham Goyal, David (Dave) Viggiano, Conroy Ricketts |
| Connect: Blue Web Team | Web (Django) | Sravan Reddy, Charl Smit, Ajeet Yadav, Pawan Verma |
| Connect: Green Web Team | Web (Django) | Manish Kangia, Chris Smit, Zandre Engelbrecht, Hemant Singh Yadav |

- **Across both web teams:** Simon Kelly (tech lead) and Nitin Saxena (QA).
- The dashboard treats Blue and Green together as the **Web Pod** and Mobile as the **Mobile Pod**.
  Web split into Blue and Green at Sprint 101 (2026-10-20).
- Allocations change over time (e.g. 20% to the AI workgroup) and so does PTO. Read the
  snapshot's capacity notes for the current sprint. Don't assume full capacity.
- Every CCCT ticket should carry a Team. Many done tickets don't, so a missing Team is a
  standing hygiene finding. Propose one from the ticket's epic, or from the assignee's team
  above.

## Cadence
- **Two-week sprints** starting Monday, numbered across all teams (Sprint 102 started 2026-11-03).
  Mobile and each web team run their own sprint under the same number.
- Sprint names drift (`(Web) Sprint 99 - …`, `Web\Blue Sprint 102 - …`, `Green Pod - Sprint
  103`). Match on team and number, not on the exact name.
- **Capacity days** = team-days available after PTO and allocations. Engineering estimates a
  sprint's velocity as the 5-sprint rolling velocity per team-day × capacity days. Use the same
  method when Sift sizes work.

## Estimation
- **Story Points (`customfield_10017`)** is the estimate in use: Fibonacci 1/2/3/5/8, mostly 3
  and 5. About 75% of done tickets have points; about 45% of open ones do.
- Ignore `Story point estimate` (`customfield_10029`, never used), `Effort (migrated)`
  (`customfield_12534`, always "L1", left over from a migration) and time estimates (unused).
- A missing estimate is a finding **only** for tickets in the current or next sprint, or In
  Progress. The team estimates at planning, so don't nag Backlog items for points.
- An 8 is a smell: those rarely ship as-is, so suggest splitting.

## CCC (roadmap) flow: Jira Product Discovery ideas
`Backlog` → `Defining Requirements` → `Requirements Validation` → `Prioritized` →
`Technical Specification` → `Implementation` → done.
- **In flight** = Prioritized, Technical Specification, Implementation. These items should have
  goals and owners, and from Technical Specification on, a linked CCCT ticket.
- An idea links to its delivery epic through a **`Polaris work item link`** (CCC ↔ CCCT). An
  Implementation idea with no linked epic, or an epic with no CCC link, is a roadmap↔backlog gap.

## CCCT (delivery) flow
`Backlog` / `Open` / `To Do` → `In Progress` → `In Review` → `In QA` → `Ready for Deploy` → `Done`.
`Blocked` can happen from any status.
- Hierarchy: Epic → Story / Task / Bug / Design / Test. An epic inherits its goal from the CCC
  idea it implements.
- Ignore `Connect Release Path` (`customfield_11457`). Don't flag it, propose it or rank by it
  (Mary, 2026-11-03).
- **Stuck vs. queued:** judge against the snapshot's cycle time (active work, about 9 days at
  the median), not its lead time (about 40 days, mostly waiting). For example, a story In
  Progress for more than a sprint, or In Review / In QA for more than a week, is worth a nudge.
  A Backlog ticket that is merely old is not stuck.

## WIP
- More than about 2 In Progress per person, or a pile-up in In Review / In QA, points to a
  review/QA bottleneck rather than a capacity one. Say which. Nitin is the single QA across
  web, so In QA pile-ups on web are expected to queue behind him.
- Blocked tickets need a named blocker (a link or a comment). Blocked with neither is a finding.

## How Sift uses it
- **Capacity check per goal.** Sum the points (or the count, if unestimated) of in-flight work
  under each 2027 goal, by team. Compare that against the team's velocity in the snapshot and
  express it in sprints, e.g. "goal 02 has ~4 sprints of Web work queued".
  Flag a goal that is many sprints deep on one team, or a team carrying most goals at once.
- **Commitment realism.** When the current sprint's commitment is well above the estimated
  velocity, say so. Name what's likely to slip, ranked by which items move a goal least.
- **Route by team.** Findings on CCCT work go to that team's people. Interrupt load (CI) and
  bug volume come out of the same capacity, so mention them when a team looks short.
