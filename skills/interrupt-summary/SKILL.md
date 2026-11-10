---
name: interrupt-summary
description: >
  Interrupt Summary — Sift's monthly read-out of what lands on the CI (Connect Interrupt) board:
  tickets per month by type (task / bug / story), what each category of request is, and the
  product change that would take it off the board. Rebuilds the shared "Connect Interrupt
  Summary" artifact page for a rolling six-month window and republishes it after approval. Use
  when asked for "the interrupt summary", "what's coming into CI", "interrupt trends", "update the
  interrupt page", or on Sift's monthly cadence. Per-ticket nudging is sift:review-interrupt.
argument-hint: "[--from YYYY-MM-DD] [--to YYYY-MM-DD]"
---

# Interrupt Summary — Sift

Read-only on Jira. The output is one page, published to the existing shared artifact:
**https://claude.ai/artifact/2vochcmx84jjjk2gBFCkwY** ("Connect Interrupt Summary", shared with
the Dimagi org — viewers see an update the moment it publishes). Republishing it is an outbound
action: draft, show, publish only on the approver's yes.

This is the *trend* view. Keeping individual interrupts moving is `sift:review-interrupt`.

## 1. Scope
- Project `CI`, tickets **created** in the window. Default: the six months up to today (same
  day-of-month). `--from` / `--to` override; a named month range ("May to October") is fine.
- Types other than Bug and Story (Employee offboarding, Sub-Task, …) count as **Task**.
- **Cadence: monthly.** `~/.sift/state/interrupt-summary/last-run` holds the last publish date;
  the Tuesday sweep runs this skill when that date is 28+ days old (or missing).
- Read `context/decisions.md` first; the "Product change" column must not contradict a ruling
  or the Product Principles (CLAUDE.md). Flag any that does.

## 2. Fetch and pre-classify
```bash
D=$(mktemp -d)
bin/sift-interrupt-summary fetch -o "$D/tickets.json"            # [--from …] [--to …]
bin/sift-interrupt-summary classify "$D/tickets.json" -o "$D/assign.json"
```
`classify` gives every ticket a category from `skills/interrupt-summary/taxonomy.json`, in this
order: the category it had in an earlier run (`"by": "prior"`), the first keyword rule that
matches the title (`"keyword"`), else the type's catch-all (`"fallback"`: Other dev work /
Product bugs / Platform & admin). It prints per-category counts and lists every fallback.

## 3. Manual pass — the part that makes the numbers worth reading
Keywords are a first cut. Edit `$D/assign.json` (change `category` only):
- **Every `fallback` ticket**: put it in the right category; leave it in the catch-all only when
  it really is general dev work / a product defect / a platform ask.
- **Every `keyword` ticket**: skim titles per category and move the misfits (e.g. "Test Ready to
  Deploy automation" is dev work, not routine ops; a "Request to unblock" filed as a Bug is a
  lockout, not a "request filed as bug"). Open the ticket (`bin/sift-jira issue <KEY>`) when the
  title can't decide it.
- `prior` tickets were already reviewed — leave them unless clearly wrong.
- Categories are fixed so months compare. If a real new cluster appears (5+ tickets that fit
  nowhere), add a category to `taxonomy.json` (name, `match`, `what`, `change`) and say so in
  the report; don't rename existing ones.

## 4. Render, read the numbers, write the notes
```bash
bin/sift-interrupt-summary render "$D/tickets.json" "$D/assign.json" -o "$D/interrupt-summary.html"
```
It refuses to render if any ticket is unassigned or in a category that isn't its type's, and
prints the computed numbers. **Every number on the page is computed** — the headline counts, the
peak month, partial-month labels, category counts and percentages, story statuses. Sift writes
only the judgment, in `$D/notes.json`, using numbers from that printout:
```json
{"headline_note": "Of the 135 tasks, 73 are requests users could handle themselves with the right controls (feature flags, unblocks, access, data fixes), and 34 are routine ops.",
 "bugs_note": "More than a third (68) are lockouts or service requests rather than product defects.",
 "stories_note": "The interrupt board is mostly acting as an idea inbox. Next step for all themes: route stories to a CCCT intake instead of CI.",
 "overrides": {"Task": {"Feature flags & opp config": {"change": "…"}}}}
```
- One or two sentences each, plain words, British spelling, no Jira jargon.
- `what` / `change` text lives in `taxonomy.json`. Update a cell when the facts moved — a
  proposed product change has shipped or been rejected, or the mix inside a category changed.
  Use `overrides` for this run only; edit `taxonomy.json` when it should stick (commit it).
- Compare with last month's snapshot (`~/.sift/state/interrupt-summary/stats-*.json`, newest):
  note big shifts (a category doubling, a product change that should have cut volume but
  didn't) in the report, and in a note if they matter to readers.
Re-run `render` with `--notes "$D/notes.json"`.

## 5. Check the page before showing it
Open `$D/interrupt-summary.html` and look at it: chart bars and totals present, three tables
filled, partial months labelled. All content is static HTML/SVG (the script only adds chart
tooltips), so it must also read correctly with scripts off — file previews show it that way.

## 6. Present for approval
Turn reply (turn Step 2):
- Lead with the outcome: "CI, 10 May – 10 Nov: 362 tickets (180 bugs, 140 tasks, 42 stories),
  peak 94 in July. Draft ready to replace the shared page."
- What changed since the last published version (biggest category moves, notes rewritten,
  taxonomy edits), and how many tickets the manual pass moved.
- Attach or link the draft HTML. Ask: publish to the shared page?

## 7. Publish, then save
On a yes:
- **Interactive session with the Artifact tool:** `Artifact read` the URL above (the publish is
  refused otherwise), then publish `$D/interrupt-summary.html` with
  `url: https://claude.ai/artifact/2vochcmx84jjjk2gBFCkwY`. Never create a new artifact for the
  monthly update — the link people have must keep working.
- **No Artifact tool (headless/canopy-web turn):** stop at the draft. Say the page is ready and
  needs an interactive session to publish; leave the HTML attached to the turn.
- After a successful publish only: `bin/sift-interrupt-summary save "$D"` (carries the
  category assignments forward, snapshots the stats, stamps `last-run`). If `taxonomy.json`
  changed, ship it (branch → PR → merge, per CLAUDE.md).

## Never
- Hand-type a count into notes that the printout doesn't show.
- Publish without an explicit yes, or to a new artifact URL.
- Write to Jira — this skill is read-only.
- Post the page or summary to Slack directly — reply in the turn; canopy-web relays it.
