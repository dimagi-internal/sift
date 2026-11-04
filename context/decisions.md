# Sift decisions log

What the people Sift serves have decided about Sift's own proposals and judgments: standing
rulings ("always/never do X") and specific changes they declined. Read this **before proposing
anything**. Never re-propose a declined change, and never act against a standing ruling.

This is not the product principles. How the *product* must behave lives on the
[Connect Product Principles](https://dimagi.atlassian.net/wiki/spaces/connect/pages/4480958467/Connect+Product+Principles)
page (`skills/product-principles`). This file holds how *Sift* should triage, rank and propose.

## How to keep it
- **When:** at the end of any approval step where the approver
  - strikes or declines a proposed change → add a row to **Declined changes**
  - rewords it in a way that implies a rule → add it to **Standing rulings**
  - states a rule outright ("don't flag X", "Y means Z") → add it to **Standing rulings**

  Approvals of one-off changes don't go here (the Jira history has them).
- **What:** one line each, with date (YYYY-MM-DD), who decided, and the scope. Quote the
  person's wording when it's short. Note the reason if they gave one.
- **Overturning:** if someone later reverses a ruling, strike it through (`~~…~~`) and add the
  new one with a pointer. Never silently delete.
- **Where it's enforced:** if a ruling changes how a skill or context file works, also edit that
  file in the same change, and cite the ruling's date here.
- **Ship:** it's a normal repo change (branch → PR → self-merge, `skills/shipping`). Batch a
  turn's additions into one commit.

## Standing rulings
| Date | Decided by | Scope | Ruling | Enforced in |
|---|---|---|---|---|
| 2026-10-27 | Mary Rocheleau | CCC Goal | Sift proposes Goals and never sets them without approval. PersonalID recovery items were deliberately left out of goal 01; don't re-propose them, and raise them only as a coverage gap. | `context/2027-themes.md` |
| 2026-10-27 | Mary Rocheleau | CCC Goal | Don't propose closing a CCC item just because it has no Goal. Off-goal work is a finding, not a defect. | `context/2027-themes.md` |
| 2026-10-27 | Mary Rocheleau | CCCT Team | Test tickets are exempt from the web team check. | `skills/backlog-triage` |
| 2026-11-03 | Mary Rocheleau | 2027 goals | The five goals are not in priority order. Rank items by how directly they move a goal, never one goal over another. | `context/2027-themes.md` |
| 2026-11-03 | Mary Rocheleau | CCCT fields | Ignore `Connect Release Path`: don't flag it, propose it or rank by it. | `context/delivery-model.md` |
| 2026-11-03 | Mary Rocheleau | CCC Prioritization | Connect doesn't commit by quarter. CCC items with Prioritization = `Backlog` are "not currently going to be worked": they're parked, not stuck. Don't nudge them, count them as load, or close them for age. | `context/delivery-model.md` |
| 2026-11-03 | Mary Rocheleau | CCC Prioritization | Rank planned items Must Have (1) > Nice to Have (2) > Could Have (3). Nice ranks above Could. | `context/delivery-model.md` |
| 2026-11-03 | Mary Rocheleau | Definition of ready | CCC needs owner, Goal + Prioritization, a linked spec doc and a problem statement before Technical Specification. CCCT Stories need AC to enter a sprint; Tasks need a clear done; Bugs need repro. | `context/definition-of-ready.md` |
| 2026-11-03 | Mary Rocheleau | Cadence | Grooming is Thursday. Sift runs a backlog sweep Tuesday and grooming prep Wednesday (08:00 ET), on Mary's machine when it's on. | canopy-web schedules 31, 32 |
| 2026-11-03 | Mary Rocheleau | Shipping | Capacity snapshot refreshes are shipped by Mary. Sift leaves them uncommitted and hands her the command. | `skills/capacity-refresh` |
| 2026-11-04 | Mary Rocheleau | Grooming prep | Prep team by team (Blue, Green, Mobile), each on its own. Focus on the CCCT tickets planned in the team's next sprint: check component, acceptance criteria, linked issues and description, and suggest the changes needed. Then review capacity. | `skills/grooming-prep`, `context/definition-of-ready.md` |
| 2026-11-04 | Mary Rocheleau | CCC archived ideas | Exclude archived CCC ideas from sweeps, stale reviews and counts. Product Discovery archives ideas (e.g. on merge) without changing status; filter with `cf[10336] is EMPTY AND cf[10338] is EMPTY`. | `skills/backlog-triage`, `skills/review-stale-tickets` |
| 2026-11-04 | Mary Rocheleau | CCC intake comments | Drafted problem-statement comments are the statement alone: no "Proposed problem statement" header, no "Supports goal …" tag, no named follow-ups. Reviewed one at a time before posting. | `skills/roadmap-intake` |

## Declined changes
Specific proposals that were struck. Before proposing a change to a ticket, check here for that
key and op. Re-propose only if the ticket has materially changed since, and say so.

| Date | Declined by | Ticket | Proposed change | Reason |
|---|---|---|---|---|
| 2026-10-27 | Mary Rocheleau | [CCCT-2347](https://dimagi.atlassian.net/browse/CCCT-2347) | Re-parent under epic [CCCT-2067](https://dimagi.atlassian.net/browse/CCCT-2067) | — |
| 2026-11-04 | Mary Rocheleau | [CCCT-2945](https://dimagi.atlassian.net/browse/CCCT-2945) | Comment asking Manish whether the contact migration is still blocked | Manish is on PTO |
| 2026-11-04 | Mary Rocheleau | [CCC-292](https://dimagi.atlassian.net/browse/CCC-292) | Set Goal 01 (FLW identity) | Moved to Prioritization = Backlog instead of Could Have |
| 2026-11-04 | Mary Rocheleau | [CCC-292](https://dimagi.atlassian.net/browse/CCC-292) | Move status back to Backlog to match Prioritization = Backlog (do not flag the mismatch) | Leave as is |
| 2026-11-04 | Mary Rocheleau | [CCC-464](https://dimagi.atlassian.net/browse/CCC-464) | Intake comment with a drafted problem statement (Celery schedules drift) | — |
| 2026-11-04 | Mary Rocheleau | [CCC-470](https://dimagi.atlassian.net/browse/CCC-470) | Intake comment with a drafted problem statement (Sunset Superset) | — |
| 2026-11-04 | Mary Rocheleau | [CCC-482](https://dimagi.atlassian.net/browse/CCC-482) | Link as Duplicate of [CCC-477](https://dimagi.atlassian.net/browse/CCC-477) (supervisor app data) | Leave it |
