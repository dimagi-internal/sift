---
name: sprint-start-report
description: >
  Report on the first day of a Connect sprint: what tickets each team (Blue, Green, Mobile) has
  picked up, grouped by the 2027 goals. Runs on Sift's Monday schedule and only produces a report
  when a sprint actually started that day. Use also for "what did each team pick for Sprint 104",
  "sprint kickoff report", "what's in the sprint".
---

# Sprint start report — Sift

Read-only. Jira is only read. The report is a draft: sending it beyond the turn's reply
(Slack post, email) needs the human's approval like any other outbound action.

Read first: `context/delivery-model.md` (teams, cadence), `context/2027-themes.md` (goals),
`context/capacity-snapshot.md` (velocity, for the commitment check).

## 1. Is it a sprint's first day?
Sprints are two weeks, start on a Monday and share a number across teams, so the schedule fires
every Monday and this step decides whether to proceed.
```bash
bin/sift-jira sprints --state active
```
- Proceed only if at least one active sprint has `start` on today's date (America/New_York).
  If none did, say "no sprint started today" and stop. A named request ("Sprint 104") skips this check.
- Teams start within a day of each other. If only some have started, report those and note the rest.
- Skip a team-sprint already reported: `canopy cursor since sprint-start-report --local ~/.sift/state --items - < "$T/started.json"`
  (id = `<sprintId>`, `ts` = the sprint's `start`).

## 2. Pull the picks
```bash
bin/sift-jira sprint-tickets <sprintId>
```
One call per started sprint. **Group by the Jira `Team` field, never by sprint name** (Blue and
Green sometimes share a sprint). Tickets with another team or none are listed in one line at the
end so the pod can fix the field. Drop tickets already Done.

## 3. Write the report
Slack format: bold markers only, no emojis, no headings or tables. One block per team, Blue,
Green, Mobile, in that order. Each block:
```
*<Team> — Sprint <N> picked, <Mon D> – <Mon D>*
<count> tickets, <pts> pts (<unestimated> unestimated). <One line: capacity-snapshot velocity vs this commitment, only if it differs notably.>
*<Goal name>*
• <https://dimagi.atlassian.net/browse/CCCT-1234|1234> <short plain title> (<points>, <assignee or "unassigned">)
*Not tied to a 2027 goal*
• ...
```
Rules:
- Goals from `context/2027-themes.md` via the ticket's epic (`parent`); use goal names, no
  numbers; order goals by how much work each holds. Anything not plainly serving a goal goes
  under "Not tied to a 2027 goal". One ticket, one goal.
- Titles are short and plain: what changes for Connect Workers, LLOs or staff. British spellings.
- Flag, in one line per team at most: unestimated tickets, unassigned tickets, a ticket not
  ready per `context/definition-of-ready.md` (no AC), carry-overs (`other_open_sprints` non-empty),
  and a commitment well above velocity. Say what, not who is behind.
- Flag anything conflicting with the Product Principles or `context/decisions.md`.
- Keep it to a screen per team.

## 4. Present and record
Put the report in the turn's reply. If the turn was scheduled rather than asked, draft it and
wait for approval before posting anywhere else (e.g. #connect-sift). After delivery:
`canopy cursor bump sprint-start-report --local ~/.sift/state --items - < "$T/started.json"`.
