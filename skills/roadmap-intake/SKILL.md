---
name: roadmap-intake
description: >
  Sift's intake triage for NEW items in the CCC roadmap backlog — check every idea created
  since the last run for the four intake basics (Prioritization, Goal, a good description,
  1–2 Product Areas), propose the missing values and a drafted problem statement, get the
  batch approved, then apply it with bin/sift-jira. Use when asked to "triage new CCC items",
  "roadmap intake", "review new ideas", "what came into the roadmap this week", "intake", or on the Tuesday sweep
  before backlog-triage.
argument-hint: "[--days 14] [--full] [--max 40]"
---

# Roadmap intake — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
This skill covers **new** CCC ideas only. The CCCT delivery backlog sweep is
`sift:backlog-triage`, which does not check CCC fields; stale CCC items go through
`sift:review-stale-tickets CCC`.

## 1. Scope
- Read `context/2027-themes.md` (the five goals and what each covers — your Goal lens) and
  `context/decisions.md` (standing rulings + declined changes; never re-propose a declined
  change, never act against a ruling).
- Read the live Product Principles (`bin/sift-confluence page 4480958467`). A new idea that
  conflicts with one is a flag: quote and link the principle (`skills/product-principles`).
- **New** = created since the last intake run. Cursor `roadmap-intake` in `~/.sift/state`. First run
  or `--full`: everything created in the last `--days` (default 14). If the asker named keys or
  a window, use those and say so.

## 2. Pull candidates (read-only)
```bash
T=$(mktemp -d); N=14
bin/sift-jira search --max 200 --jql "project = CCC AND statusCategory != Done \
  AND cf[10336] is EMPTY AND cf[10338] is EMPTY AND created >= -${N}d ORDER BY created ASC" > "$T/new.json"
canopy cursor since roadmap-intake --local ~/.sift/state --items - < "$T/new.json" > "$T/todo.json"
```
The `cf[10336]`/`cf[10338]` clauses drop archived ideas (ruling 2026-11-04). The cursor keys
on `{id, ts}`, so an idea edited since it was last reviewed comes back — re-check it; if it now
passes, it produces no finding.

Rows carry `prioritization`, `goal`, `product_area`, `platform`, `has_description`. Read each
idea in full before judging it: `bin/sift-jira issue <KEY>` (description, comments, links —
e.g. the `CI-` interrupt or CCCT ticket it came from). To spot duplicates, keep the open-CCC
list handy (`project = CCC AND statusCategory != Done AND cf[10336] is EMPTY AND cf[10338] is EMPTY`).

## 3. The intake bar — four checks per idea

| # | Check | Passes when | Proposed change |
|---|---|---|---|
| 1 | **Priority** | `Prioritization` (`customfield_12800`) is set: `Must Have`, `Nice to Have`, `Could Have` or `Backlog` | `update` with one value + a one-line reason. Default to `Backlog` unless the idea clearly moves a goal's metric now or comes from a live interrupt |
| 2 | **Goal** | `Goal` (`customfield_14111`) has 1+ of the five goals, or the idea is deliberately off-goal | `update` with the goal(s) it directly serves, citing the "What each goal covers" bullet it matches; if none fits, propose **no Goal** and say so in the report (not a defect) |
| 3 | **Good description** | A PM could pick it up cold: **who** is affected, **what goes wrong today** (the problem, not only the solution), and **why it matters** / what better looks like. Links to the source (CI ticket, Slack, doc) are a plus | `comment` with a drafted 2–4 line problem statement for the reporter to confirm and paste in: the statement alone, no header, no goal tag, no names (ruling 2026-11-04). Never overwrite the description. Skip an idea that already has an intake comment |
| 4 | **Product Area** | `Product Area` (`customfield_10448`) has **1 or 2** values | 0 → `update` with the 1–2 best fits; 3+ → `update` down to the 2 that fit best (say which were dropped). Values must match Jira's list exactly — see below |

Also fill **Platform** (`customfield_10434`, `Web` / `Mobile`) when it's empty and obvious from
the idea — Product Area isn't a stand-in for it.

Jira's `priority` field (P1–P6) is NOT the priority check: almost every CCC idea sits at the
default P6. Ignore it; Prioritization is what the team ranks by.

### Judging Prioritization
- Rulings: rank Must Have > Nice to Have > Could Have; `Backlog` means "not currently going to
  be worked" (parked, not stuck). Connect doesn't commit by quarter.
- Propose `Must Have` only when the idea directly moves a 2027 goal's metric **and** something
  forces timing (a live program blocked, a security finding, a principle being violated in
  production). Otherwise `Nice` / `Could` for on-goal work worth planning, `Backlog` for the rest.
- If you can't tell, propose `Backlog` and put the question in **Flags** for the PM.

### Product Area values
Use only existing values (check the current list from the open-CCC pull if unsure):
`Mobile App Experience`, `Platform and Security`, `Verification`, `Opportunity Setup`,
`PersonalID and Sign-In`, `FLW Payments`, `Opportunity Lifecycle`, `Auditing`,
`Admin and Support Tools`, `Data Export and APIs`, `Dashboards and Reporting`,
`Worker Management`, `Limits and Budgets`, `Notifications`, `Invoicing`,
`LLO Network and Directory`, `Microplanning and Maps`, `Work History and Credentials`,
`Orgs, Roles and Permissions`, `Messaging`, `Tasks`, `Exploratory`.
Pick the area that owns the change, then at most one more it materially touches. Need a new
area? Flag it — don't invent a value.

### Also catch at intake
- **Duplicate** of an open idea → propose `link` Duplicate → keeper and flag for the PM to
  merge (Product Discovery merge archives it); skip the other four checks for it.
- **Delivery work filed as an idea** (a bug or a small task with no product question) → flag it
  to move to CCCT/CI; don't fill its fields.
- **Principle conflict** → flag with the principle quoted.

Be decisive: one value per field, not a menu. Skip anything you aren't confident about and say
how many you skipped and why.

## 4. Plan, report, dry-run
- **Plan** — the `bin/sift-jira apply` input (format in its module docstring), every row with
  a one-line `why`. One `update` per idea combining its field fixes:
  ```json
  {"key": "CCC-483", "op": "update", "why": "intake: Goal 02, Backlog, trim areas to 2",
   "fields": {"customfield_12800": {"value": "Backlog"},
              "customfield_14111": [{"value": "Program integrity and tracability"}],
              "customfield_10448": [{"value": "Verification"}, {"value": "Auditing"}]}}
  ```
  Multi-selects (Goal, Product Area, Platform) replace the whole list — include values that
  stay. Goal 02 is spelled `Program integrity and tracability` in Jira. Cap at `--max` (40).
- **Report** — lead with the outcome ("9 new CCC ideas: 3 pass, 6 need fixes, 11 changes
  proposed"). Then a table, one row per idea: linked key, summary, and ✓ / proposed value for
  Priority · Goal · Description · Product Area. Then the drafted problem statements, then
  **Flags** (duplicates, misfiled delivery work, principle conflicts, prioritization questions),
  then people to @-mention (comments post under Mary's token and don't notify anyone).
- Every Jira key is a link: `[CCC-483](https://dimagi.atlassian.net/browse/CCC-483)`.
- Dry-run: `bin/sift-jira apply plan.json --approved-by dry-run --dry-run`.

## 5. Approval, then apply
Field updates can be approved as a batch. Comments are reviewed **one at a time**: show each drafted comment in full and post only the ones approved, with the approver's edits verbatim (ruling 2026-11-04).
Present the report + plan for approval (turn Step 2). Goal and Prioritization are never written
without this approval (ruling 2026-10-27); the approver may strike or change values line by
line. Log struck lines in `context/decisions.md` (Declined changes) and any rule they state
under Standing rulings. Then:
```bash
bin/sift-jira apply plan.json --approved-by "<approver's name>"
canopy cursor bump roadmap-intake --local ~/.sift/state --items - < "$T/todo.json"
```
Bump with every idea you reviewed, including ones that passed. Re-pull the rows after applying and bump those, so your own comments don't make an idea look edited next run. Report what applied and anything
that errored, one line each.

## Never
- Write to Jira any other way — railed in `config/gating.json`.
- Overwrite an idea's description or summary, change its status, or assign it — propose, flag.
- Re-propose a declined Goal (e.g. PersonalID recovery items for goal 01).
- Touch CCCT or CI — delivery tickets go through `sift:backlog-triage` / `sift:review-interrupt`.
- Post the report to Slack directly — reply in the turn; canopy-web relays it.
