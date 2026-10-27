---
name: review-interrupt
description: >
  Review Interrupt — Sift's weekly pass over the CI (Connect Interrupt) board, where ad hoc
  support issues are reported. Finds interrupts that nobody owns, that stopped moving, that
  have been open too long or that don't belong on the board, decides per ticket whether to
  nudge, flag or re-home it, and gets the batch approved before bin/sift-jira applies it.
  Use when asked to "review interrupts", "are interrupts moving", "check the CI board", or on
  Sift's weekly cadence.
argument-hint: "[--days 14] [--max 40]"
---

# Review Interrupt — Sift

Reads are free; Jira writes happen only via `bin/sift-jira apply` on a plan a human approved.
Someone outside the team reported each interrupt and is waiting on it, and most close within a
week (p50 ≈ 5 days, p90 ≈ 40 as of Oct 2026). The job is to keep every one moving — never to
clean the board by closing things.

**Interrupt coordinator: smhlanga.** They acknowledge new tickets ("added to the queue for the
interrupt dev") and chase owners. Untriaged / queue flags go to them. Update this line if the
role moves.

## 1. Scope
- Project `CI` only. CCCT / CCC staleness is `sift:review-stale-tickets`.
- **Cadence: weekly.** No cursor — every run looks at every open interrupt again, including the
  ones nudged last week that still haven't moved.
- `--days` (default 14) = "not moving" threshold. `--max` (default 40 changes).
- Recall standing decisions for this counterpart (persona.md › Memory scope). Never re-propose
  a change someone declined.

## 2. Pull candidates — three searches
An interrupt can be moving and still be in trouble, so one query isn't enough:
```bash
T=$(mktemp -d); N=14
bin/sift-jira search --jql "project = CI AND statusCategory != Done \
  AND NOT status CHANGED AFTER -${N}d AND created <= -${N}d" > "$T/stuck.json"   # not moving
bin/sift-jira search --jql "project = CI AND statusCategory != Done \
  AND assignee is EMPTY AND created <= -7d" > "$T/unowned.json"                  # nobody on it
bin/sift-jira search --jql "project = CI AND statusCategory != Done \
  AND created <= -30d" > "$T/aging.json"                                          # open a month+
```
Merge by key and keep which searches each ticket hit — that goes in the report.

## 3. Read each candidate in full
`bin/sift-jira issue <KEY>` returns fields, comments and the changelog. For every candidate:
- **Read the latest comments in full**, not a truncated summary — the last comment is usually
  the one that decides the disposition (a direct question to someone, a "this needs a rework").
- **Check the changelog, not just comments.** `updated` moves for attachments, field edits and
  status changes that leave no comment. If a ticket was updated recently with no new comment,
  find out what changed (e.g. the video someone promised was attached) before nudging.
  `changelog.histories` is newest-first; each entry lists `field` / `toString` (status,
  assignee, Attachment, …).
- **Find its PRs and their state.** Ticket text often doesn't link them. Search GitHub by key
  and by the bug's distinctive terms:
  ```bash
  for r in commcare-connect commcare-android commcare-hq; do
    gh pr list -R dimagi/$r --state all --search "<KEY>" --json number,state,title,updatedAt,mergedAt
  done
  gh pr view <n> -R dimagi/<repo> --json state,mergedAt,reviewDecision,updatedAt
  ```
- **Note the last nudge**: who last asked the assignee/reporter for an update, when, and
  whether anyone answered after it.

## 4. Classify ownership — unassigned is not the same as untriaged
The coordinator often acknowledges a ticket without assigning it, so `assignee is EMPTY`
mixes two different states:
| State | Test | Disposition |
|---|---|---|
| **Untriaged** | unassigned, 3+ days old, no comment from the coordinator or any dev | **flag** to the coordinator: nobody has looked at it |
| **Queued** | unassigned, but acknowledged ("added to the queue …") | fine under 14 days; **flag** 14+ days to the coordinator to assign or re-prioritize |
| **Owned** | has an assignee | judge in step 5 |

## 5. Judge — one disposition per ticket
Pick ONE: **nudge**, **flag**, **re-home**, or **leave** (moving — report only). Be decisive;
skip what you aren't confident about and say how many and why.

**First, the recent-nudge rule.** If someone (the approver, the coordinator, a dev) already
asked for an update within the last 7 days and nobody has replied yet, do NOT nudge again —
**leave** it and report "awaiting reply to <who>'s <date> nudge". If that nudge is older than
7 days and unanswered, a new nudge must cite it ("following up on the 14 Oct question") and
name a concrete next step or date.

| Situation | Disposition |
|---|---|
| To Do / In Progress, no status change in 14 days | **nudge** the assignee: what's next, and when? |
| In Review / In QA / Ready for Deploy, no status change in 14 days | **nudge** the assignee to chase the review, QA pass or deploy |
| **Status and PR disagree** — In QA / Ready for Deploy with the fix PR still open; In Progress with the PR merged; Done-looking PR but ticket open | **nudge** naming the mismatch — it's often the real blocker |
| PR open with no reviewer / `REVIEW_REQUIRED` for 7+ days | **nudge** asking who can review, or whether to drop it |
| Blocked on the reporter's information, 30+ days | **nudge** the reporter with a date after which it closes as unable to reproduce |
| Blocked on another ticket | blocker Done → **nudge** to unblock; blocker unrelated → **flag** the link |
| Comments say it's fixed / deployed but it's still open | **nudge** the reporter or assignee to confirm so it can close |
| A direct question to the approver is unanswered in the comments | **flag** it at the top of the report — it's waiting on them |
| Feature work, not a support issue (a Story, "automate…", "create ability to…", a behaviour/rule change) | **re-home**: **flag** to move to CCCT — `sift-jira` can't move tickets between projects |
| The context it was reported in has ended (program complete, one-off data fix done) | **nudge** the reporter: still worth doing? |
| Possibly wider impact than its priority says (affects all users, data correctness, payments) | **flag** for a priority change with the evidence |
| Open 30+ days and moving | **leave**, but list it as aging every week until it closes |

Before any `transition`, check the target is reachable: `bin/sift-jira transitions <KEY>`.

## 6. Write comments people will act on
- Comments post under the Jira token's account (today Mary's). Write as she would sign: plain,
  specific, no Sift boilerplate.
- Say the evidence ("PR #1582 is still open"), the ask, and what happens on each answer.
- `sift-jira` comments are plain text: naming someone does NOT notify them. List the people to
  ping in the report so the approver can @-mention them by hand.

## 7. Plan, report, dry-run
- **Plan** — the `bin/sift-jira apply` input (format in the module docstring), one-line `why`
  per row.
- **Report** — lead with the outcome ("CI: 22 open, 13 matched; 5 nudges, 6 flags, 3 moving"),
  then **waiting on you** (direct questions to the approver), then rows grouped by disposition
  with link, status, age, which searches it hit and its PR state, then **awaiting reply** (the
  recent-nudge skips), then **people to @-mention**.
- Dry-run: `bin/sift-jira apply plan.json --approved-by dry-run --dry-run` (today it only echoes
  the plan; it doesn't validate keys or transitions).

## 8. Approval, then apply
Present the report + plan for approval (turn Step 2). The approver may strike rows — drop them
and remember them as declined for this counterpart. Then
`bin/sift-jira apply plan.json --approved-by "<approver's name>"` and report what applied and
what errored, one line each.

## Never
- Close an interrupt for being stale — nudge, flag or re-home it instead.
- Nudge someone who was already asked in the last 7 days and hasn't had a chance to answer.
- Write to Jira any other way — railed in `config/gating.json`.
- Reassign someone's work or change priority directly — flag it.
- Post the report to Slack directly — reply in the turn; canopy-web relays it.
