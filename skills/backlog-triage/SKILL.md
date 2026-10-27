---
name: backlog-triage
description: >
  Sift's backlog sweep for Connect — find stale, unowned, unestimated, duplicate,
  under-specified, mis-prioritized or mis-classified (component / team / epic / roadmap link)
  tickets in the Connect Jira backlogs (CCC roadmap, CCCT delivery), turn each finding into a concrete proposed change, get the batch approved,
  then apply it with bin/sift-jira. Use when asked to "triage the backlog", "groom CCCT",
  "clean up the roadmap", or on Sift's weekly cadence.
---

# Backlog triage — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
Capability lives in `bin/sift-jira`; this skill is the judgment around it.

## 1. Scope the sweep
- Projects: `sift_JIRA_PROJECTS` (default `CCC,CCCT`). `CI` (Connect Interrupt) is out of scope
  here — it gets its own weekly `sift:review-interrupt` run.
- If the asker named a narrower slice (an epic, a component, "just bugs"), use that and say so.
- Recall standing decisions for this counterpart (persona.md › Memory scope) — e.g. changes
  they've already declined. Never re-propose a rejected change.

## 2. Pull candidates (read-only)
Run these and keep the JSON; each row is `{id, ts, key, summary, status, priority, type,
parent, parent_type, components, team, links, …}`:
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
| Stale | no status change in 90+ days | run `sift:review-stale-tickets` for that project — its rules, not a blanket close |
| Duplicate | same problem as another open ticket (read both) | `link` Duplicate → keeper, `transition` the dup |
| Under-specified | no description or no acceptance criteria, In Progress / Ready | `comment` asking the reporter for AC |
| Unowned | In Progress with no assignee | `comment` @reporter, flag in report |
| Priority drift | priority higher than its roadmap item's, or High on a stale ticket | `update` priority |
| Empty roadmap item | CCC item In Progress with no linked CCCT work | flag for the owning PM |

### CCCT hygiene — classification rules
Every CCCT ticket must also pass these. They are the most common findings, so check them on
every sweep, not only when something else is wrong:

| Rule | Test | Typical change |
|---|---|---|
| Component | `components` has `Web / Server` or `Mobile` (both is fine) | `update` components, inferred from the parent epic or summary; flag if unclear |
| Web team | any ticket with `Web / Server` has `team` = `Connect: Blue Web Team` or `Connect: Green Web Team` | `update` team, inherited from the parent epic; flag for the PM if the epic has none |
| Epic | Story or Bug has `parent_type` = Epic | `update` parent to the obvious epic; else flag. Tasks (and Design/Test) without an epic: count them in the report, don't propose changes |
| Roadmap link | every Epic has a link to a `CCC-` item (normally `Polaris work item link`, "implements") | `link` the epic to its CCC item if obvious; else flag for the owning PM |

Field mechanics for `update` changes:
- Components replace the whole list, so include the ones already there:
  `{"components": [{"name": "Web / Server"}, …existing]}`.
- Team is `customfield_10001` and takes the team id: Blue `80f2acc0-097f-4971-b8d4-6e61bb1b8c49`,
  Green `6ed657a0-a3c9-4aaf-9b26-98d106f4a9d4`. Example: `{"customfield_10001": "<id>"}`.
- Epic: `{"parent": {"key": "CCCT-1234"}}`.
- A `Web / Server` ticket on `Connect: Mobile Team` is a mismatch, and either field could be the
  wrong one: flag it, don't pick.
- Choosing Blue vs Green with no epic to inherit from is a staffing call: flag it, don't guess.
- After the first roadmap `link` applies, check with `bin/sift-jira issue <EPIC>` that the
  epic reads "implements CCC-…" and not the reverse.

Be decisive: recommend the change, don't list options. Skip anything you aren't confident
about — say how many you skipped and why, rather than proposing a weak change.

## 4. Write the plan and the report
- Plan file — the exact input `bin/sift-jira apply` takes (see its `--help`), every change
  with a one-line `why`. Cap a batch at ~40 changes; rank the rest for next time.
- Report — lead with the outcome ("23 changes proposed across 61 open tickets; 4 roadmap items
  have no delivery work"), then a hygiene line (tickets missing a component, a web team, an epic,
  and epics missing a CCC link: counts before → after this plan), then the change list grouped
  by signal, one line per ticket with its link, then flags that need a human decision rather
  than a Jira edit.
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
