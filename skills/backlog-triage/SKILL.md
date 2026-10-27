---
name: backlog-triage
description: >
  Sift's backlog sweep for Connect — find stale, unowned, unestimated, duplicate,
  under-specified or mis-prioritized tickets in the Connect Jira backlogs (CCC roadmap,
  CCCT delivery), turn each finding into a concrete proposed change, get the batch approved,
  then apply it with bin/sift-jira. Use when asked to "triage the backlog", "groom CCCT",
  "clean up the roadmap", or on Sift's weekly cadence.
---

# Backlog triage — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
Capability lives in `bin/sift-jira`; this skill is the judgment around it.

## 1. Scope the sweep
- Projects: `sift_JIRA_PROJECTS` (default `CCC,CCCT`). `CI` (Connect Interrupt) is out of scope
  unless the asker names it.
- If the asker named a narrower slice (an epic, a component, "just bugs"), use that and say so.
- Recall standing decisions for this counterpart (persona.md › Memory scope) — e.g. changes
  they've already declined. Never re-propose a rejected change.

## 2. Pull candidates (read-only)
Run these and keep the JSON; each row is `{id, ts, key, summary, status, priority, …}`:
```bash
T=$(mktemp -d)
bin/sift-jira search --jql 'project in (CCC, CCCT) AND statusCategory != Done ORDER BY updated ASC' --max 500 > "$T/open.json"
bin/sift-jira search --jql 'project = CCC AND statusCategory != Done' > "$T/roadmap.json"
```
On the weekly cadence, narrow to what changed since last sweep:
`canopy cursor since backlog-triage --local ~/.sift/state --items - < "$T/open.json"`. The cursor lives in
`~/.sift/state` on this machine (Sift has no Google Drive yet). A full sweep (asked for
explicitly, or first run) skips the cursor. Use `bin/sift-jira issue <KEY>`
for any ticket you need to read in full before judging it.

## 3. Judge — one finding per ticket, with a concrete change
Check each open ticket against these signals; a ticket can hit several but gets ONE recommended change:

| Signal | Test | Typical change |
|---|---|---|
| Stale | not updated in 90+ days, not Blocked | `transition` → Won't Do / Backlog + `comment` why |
| Duplicate | same problem as another open ticket (read both) | `link` Duplicate → keeper, `transition` the dup |
| Under-specified | no description or no acceptance criteria, In Progress / Ready | `comment` asking the reporter for AC |
| Unowned | In Progress with no assignee | `comment` @reporter, flag in report |
| Orphaned | CCCT ticket with no parent and no CCC roadmap link | flag; suggest parent if obvious |
| Priority drift | priority higher than its roadmap item's, or High on a stale ticket | `update` priority |
| Empty roadmap item | CCC item In Progress with no linked CCCT work | flag for the owning PM |

Be decisive: recommend the change, don't list options. Skip anything you aren't confident
about — say how many you skipped and why, rather than proposing a weak change.

## 4. Write the plan and the report
- Plan file — the exact input `bin/sift-jira apply` takes (see its `--help`), every change
  with a one-line `why`. Cap a batch at ~40 changes; rank the rest for next time.
- Report — lead with the outcome ("23 changes proposed across 61 open tickets; 4 roadmap items
  have no delivery work"), then the change list grouped by signal, one line per ticket with its
  link, then flags that need a human decision rather than a Jira edit.
- Dry-run the plan before presenting: `bin/sift-jira apply plan.json --approved-by dry-run --dry-run`.

## 5. Approval, then apply
Present the report + plan for approval per the turn's Step 2 ("present for approval"). The
approver may strike lines — remove them from the plan (and remember them as declined). Then:
```bash
bin/sift-jira apply plan.json --approved-by "<approver's name>"
```
Report what applied and anything that errored (one line each), then bump the cursor with the
tickets you reviewed: `canopy cursor bump backlog-triage --local ~/.sift/state --items - < "$T/open.json"`.

## Never
- Write to Jira any other way (Atlassian MCP write tools, curl, `acli`) — railed in `config/gating.json`.
- Delete tickets, change a roadmap item's scope or target date, or reassign someone's work —
  those are product decisions; flag them instead.
- Post the report to a Slack channel directly — reply in the turn; canopy-web relays it.
