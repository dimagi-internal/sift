---
name: review-stale-tickets
description: >
  Review Stale Tickets — sweep ONE Connect Jira project for tickets that have stopped moving
  (CCCT = implementation/delivery, CCC = roadmap), decide per ticket whether to close, nudge
  or leave it, and get the batch approved before bin/sift-jira applies it. Use when asked to
  "review stale tickets", "clean up stale CCCT", "what's stuck on the roadmap", or when
  backlog-triage hits its Stale signal. Monthly cadence. The CI interrupt board has its own
  weekly skill, sift:review-interrupt.
argument-hint: "<CCCT|CCC> [--days 90] [--max 40] [--full]"
---

# Review Stale Tickets — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
One project per run — each goes stale for different reasons and needs different calls.
If the asker didn't name one, ask which before pulling anything.

## 1. Scope
| Project | What it is | Cadence | `--days` default |
|---|---|---|---|
| `CCCT` | implementation / delivery | monthly | 90 |
| `CCC` | roadmap | monthly | 90 |

Nothing else — CI interrupts go through `sift:review-interrupt`. **Batch cap**: `--max` (default 40 changes; rank the rest).
- **Cursor**: `review-stale-<project>` in `~/.sift/state`. `--full` (or a first run) skips it.
- Recall standing decisions for this counterpart (persona.md › Memory scope). Never re-propose
  a change someone declined.

## 2. Pull candidates — "stuck", not just "untouched"
`updated` is a weak signal: a comment, a bulk edit or a sprint sweep resets it without the
ticket moving (CCC had bulk edits on 2026-06-09 and 07-13). Staleness = **no status change in
N days**. Keep `updated` as a second column so you can tell "stuck but discussed" from
"abandoned".
```bash
T=$(mktemp -d); P=CCCT; N=90
bin/sift-jira search --max 500 --jql "project = $P AND statusCategory != Done \
  AND NOT status CHANGED AFTER -${N}d AND created <= -${N}d ORDER BY updated ASC" > "$T/stuck.json"
```
Repeat runs: `canopy cursor since review-stale-$P --local ~/.sift/state --items - < "$T/stuck.json"`.

Read every candidate in full before judging it — `bin/sift-jira issue <KEY>` (description,
comments, links). Also pull, as the type needs:
- **Epic / CCC item** → its delivery: `bin/sift-jira search --jql "parent = <KEY>"` and, for CCC,
  the CCCT tickets linked via "implements".
- **Blocked** → the blocker's current status.
- **PR mentioned in a comment** → `gh pr view <n> -R dimagi/commcare-connect --json state,mergedAt`.

## 3. Rule out false positives first
Drop a candidate (count it under "skipped", with the reason) when any of these hold:
- It's a container (Epic, or CCC item past Prioritized) and any child / linked CCCT ticket was
  updated within N days — the work is moving, the container just doesn't show it.
- A comment records a deliberate hold ("hold off until …", "parked for Q…") whose condition
  hasn't been met.
- It was created or re-scoped in the last N days by a bulk import (look at `created`).

## 4. Judge — one disposition per ticket
Pick ONE: **close**, **nudge**, **re-home**, or **flag**. Be decisive; skip what you aren't
confident about and say how many you skipped and why.

### CCCT — implementation
| Situation | Disposition |
|---|---|
| Backlog/To Do/Open, unowned, no linked active CCC item, nothing in comments since | **close** → Won't Do, with a comment saying why and how to reopen |
| Its ask already shipped (merged PR, done sibling, a later epic covers it) | **nudge** the owner/reporter: "this looks done by X — close?" |
| Product discovery parked in CCCT ("review…", "determine user stories…") | **close** with a comment pointing it to CCC as a roadmap item |
| In Progress / In Review, stuck | **nudge** the assignee for status; **flag** if unassigned |
| Blocked | blocker Done → **nudge** to unblock; blocker unrelated → **flag** the link; else skip |
| Epic, all children Done/Won't Do | **close** → Done |
| Assigned, P1–P3, untouched | **nudge** the assignee: schedule it, lower priority, or close |

### CCC — roadmap
Roadmap state is a product decision: Sift proposes, the owning PM decides. Never change an
item's scope or target date.
| Situation | Disposition |
|---|---|
| Backlog idea, merely old | **leave** — the backlog is an idea bank; count it, don't touch it |
| Backlog idea, superseded / duplicate / about something since removed | **close** → Won't Do with a comment naming what superseded it (link Duplicate if a keeper exists) |
| Prioritized, nothing started in N days | **flag** for the owner: still a priority? |
| Defining Requirements / Requirements Validation / Technical Specification, stuck | **nudge** the assignee; **flag** if unassigned |
| Implementation with no linked CCCT work, or all of it Done | **flag** (no delivery) / **nudge** to move to Rollout Planning or Done |

Before any `transition`, check the target is reachable: `bin/sift-jira transitions <KEY>`
(CCC's Won't Do and CCCT's Won't Do are different statuses with the same name).

## 5. Write comments people will act on
- Comments post under the Jira token's account (today Mary's). Write as she would sign: plain,
  specific, no Sift boilerplate.
- Say the evidence ("PR #1079 merged 1 April"), the ask, and what happens on each answer
  ("if so, this can be closed; if not, …").
- `sift-jira` comments are plain text: naming someone does NOT notify them. Put the people to
  ping in the report so the approver can @-mention them by hand, until mentions are supported.

## 6. Plan, report, dry-run
- **Plan** — the `bin/sift-jira apply` input (format in the module docstring), every row with a
  one-line `why`. For a close, the `transition` row comes BEFORE its comment row.
- **Report** — lead with the outcome ("CCCT: 62 stuck, 14 changes proposed, 9 skipped as
  active"), then rows grouped by disposition, one line per ticket with its link and the
  `updated` / status-change ages, then **flags** (human decisions, no Jira edit) and
  **people to @-mention**.
- Dry-run: `bin/sift-jira apply plan.json --approved-by dry-run --dry-run`. It only echoes the
  plan today — it does NOT prove the transitions or keys are valid, which is why step 4 checks
  transitions by hand.

## 7. Approval, then apply
Present the report + plan for approval (turn Step 2). The approver may strike rows — drop them
from the plan and remember them as declined for this counterpart. Then:
```bash
bin/sift-jira apply plan.json --approved-by "<approver's name>"
canopy cursor bump review-stale-$P --local ~/.sift/state --items - < "$T/stuck.json"
```
Report what applied and anything that errored, one line each.

## Never
- Write to Jira any other way — railed in `config/gating.json`.
- Sweep more than one project in one plan.
- Touch `CI` — that's `sift:review-interrupt`.
- Delete tickets, reassign someone's work, or change a roadmap item's scope or date — flag it.
- Post the report to Slack directly — reply in the turn; canopy-web relays it.
