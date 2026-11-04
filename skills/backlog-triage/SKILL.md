---
name: backlog-triage
description: >
  Sift's CCCT backlog sweep — keep the Connect delivery backlog (CCCT) clean: find stale,
  unowned, duplicate, under-specified or mis-classified (component / team / epic / roadmap link)
  tickets and CCCT work on parked roadmap items, turn each finding into a concrete proposed
  change, get the batch approved, then apply it with bin/sift-jira. CCC roadmap fields are
  roadmap-intake's job, not this one. Use when asked to "triage the backlog", "groom CCCT",
  "clean up CCCT", or on Sift's weekly cadence.
---

# Backlog triage — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
Capability lives in `bin/sift-jira`; this skill is the judgment around it.

**Scope: the CCCT delivery backlog only** (ruling 2026-11-04). CCC roadmap items are read for
context (an epic's roadmap item and its Prioritization) but never judged or changed here: CCC
fields (Prioritization, Goal, description, Product Area, Platform) belong to
`sift:roadmap-intake`, and stale CCC items to `sift:review-stale-tickets CCC`.

## 1. Scope the sweep
- Read `context/2027-themes.md` first — the five 2027 goals frame what to rank first and the
  per-goal capacity line (CCCT epics reach a goal through the CCC item they implement).
- Read `context/delivery-model.md` and `context/capacity-snapshot.md` (run `skills/capacity-refresh`
  first if the snapshot is stale). Use them to judge stuck vs. queued, route findings by team, and
  add a per-goal capacity line to the report (in-flight points vs. team velocity, in sprints).
- Read the live Product Principles (`bin/sift-confluence page 4480958467`). A ticket or idea that
  conflicts with one is a finding (quote and link the principle). Collect principle candidates
  for the report (`skills/product-principles` §2).
- Project: `CCCT` only. `CI` (Connect Interrupt) gets its own weekly `sift:review-interrupt`
  run; CCC goes through `sift:roadmap-intake`, which runs first on the Tuesday sweep.
- If the asker named a narrower slice (an epic, a component, "just bugs"), use that and say so.
- Read `context/decisions.md`: standing rulings and declined changes. Never re-propose a
  declined change or act against a ruling.

## 2. Pull candidates (read-only)
Run these and keep the JSON; each row is `{id, ts, key, summary, status, priority, type,
parent, parent_type, components, team, links, …}`:
```bash
T=$(mktemp -d)
bin/sift-jira search --jql 'project = CCCT AND statusCategory != Done ORDER BY updated ASC' --max 500 > "$T/open.json"
bin/sift-jira search --jql 'project = CCC AND statusCategory != Done AND cf[10336] is EMPTY AND cf[10338] is EMPTY' > "$T/roadmap.json"
```
`open.json` is what you judge. `roadmap.json` is read-only context: resolving an epic's roadmap
link and that item's `prioritization`. The `cf[10336]`/`cf[10338]` clauses drop archived CCC
ideas (ruling 2026-11-04): Product Discovery archives an idea (e.g. on merge) without changing
its status, so an epic linked only to an archived idea counts as having no live roadmap link.
On the weekly cadence, narrow to what changed since last sweep:
`canopy cursor since backlog-triage --local ~/.sift/state --items - < "$T/open.json"`. The cursor lives in
`~/.sift/state` on this machine (Sift has no Google Drive yet). The cursor narrows only the
per-ticket signals: run the epic Roadmap link check against the full `open.json`. A full sweep (asked for
explicitly, or first run) skips the cursor. Use `bin/sift-jira issue <KEY>`
for any ticket you need to read in full before judging it.

## 3. Judge — one finding per ticket, with a concrete change
Check each open ticket against these signals; a ticket can hit several but gets ONE recommended change:

| Signal | Test | Typical change |
|---|---|---|
| Stale | no status change in 90+ days | run `sift:review-stale-tickets CCCT` — its rules, not a blanket close |
| Duplicate | same problem as another open CCCT ticket (read both) | `link` Duplicate → keeper, `transition` the dup |
| Under-specified | fails `context/definition-of-ready.md` while in a current/next sprint or In Progress: Story without AC, Task without a clear done, Bug without repro | `comment` with the drafted fix (AC, done criteria, repro questions) |
| Unowned | In Progress with no assignee | `comment` @reporter, flag in report |
| Work on a parked roadmap item | ticket is In Progress or in a current/next sprint, and its epic implements a CCC item whose Prioritization is `Backlog` (parked) | flag for the owning PM: either the roadmap item is planned now, or the work should wait. Don't edit either ticket |

**Never use Jira's `priority` field (P1–P6)** for any judgment — Connect doesn't use it
(ruling 2026-11-04). Ranking comes from the roadmap item's Prioritization
(Must > Nice > Could; `Backlog` = parked), see `context/delivery-model.md`.

### CCCT hygiene — classification rules
Every CCCT ticket must also pass these. They are the most common findings, so check them on
every sweep, not only when something else is wrong:

| Rule | Test | Typical change |
|---|---|---|
| Component | `components` has `Web / Server` or `Mobile` (both is fine) | `update` components, inferred from the parent epic or summary; flag if unclear |
| Web team | any ticket with `Web / Server` (except type Test — those are exempt) has `team` = `Connect: Blue Web Team` or `Connect: Green Web Team` | `update` team, inherited from the parent epic; flag for the PM if the epic has none |
| Epic | Story or Bug has `parent_type` = Epic | `update` parent to the obvious epic; else flag. Tasks (and Design/Test) without an epic: count them in the report, don't propose changes |
| Roadmap link | **every open CCCT Epic** links to a live (non-archived) `CCC-` item (normally `Polaris work item link`, "implements"). Check every epic on every sweep, not only changed ones | `link` the epic to its CCC item if obvious; else flag for the owning PM |

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
- Report — lead with the outcome ("23 changes proposed across 61 open CCCT tickets"), then a
  hygiene line (tickets missing a component, a web team, an epic, and epics missing a CCC link:
  counts before → after this plan), then the per-goal capacity line, then the change list
  grouped by signal, one line per ticket with its link, then flags that need a human decision
  rather than a Jira edit.
- Every Jira key you write (report, flags, replies) is a link:
  `[CCCT-1234](https://dimagi.atlassian.net/browse/CCCT-1234)`. Never a bare key.
- Dry-run the plan before presenting: `bin/sift-jira apply plan.json --approved-by dry-run --dry-run`.

## 5. Approval, then apply
Present the report + plan for approval per the turn's Step 2 ("present for approval"). The
approver may strike lines — remove them from the plan and log each in `context/decisions.md`
(Declined changes; any rule they state goes under Standing rulings). Then:
```bash
bin/sift-jira apply plan.json --approved-by "<approver's name>"
```
Report what applied and anything that errored (one line each), then bump the cursor with the
tickets you reviewed: `canopy cursor bump backlog-triage --local ~/.sift/state --items - < "$T/open.json"`.

## Never
- Write to Jira any other way (Atlassian MCP write tools, curl, `acli`) — railed in `config/gating.json`.
- Change any CCC item — roadmap fields are `sift:roadmap-intake`'s job.
- Use or change Jira's `priority` (P1–P6) field.
- Delete tickets, change a roadmap item's scope or target date, or reassign someone's work —
  those are product decisions; flag them instead.
- Post the report to a Slack channel directly — reply in the turn; canopy-web relays it.
