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
| 2026-11-03 | Mary Rocheleau | Shipping | Capacity snapshot refreshes are shipped by Mary. Sift leaves them uncommitted and hands her the command. | `skills/capacity-refresh` |

## Declined changes
Specific proposals that were struck. Before proposing a change to a ticket, check here for that
key and op. Re-propose only if the ticket has materially changed since, and say so.

| Date | Declined by | Ticket | Proposed change | Reason |
|---|---|---|---|---|
| 2026-10-27 | Mary Rocheleau | [CCCT-2347](https://dimagi.atlassian.net/browse/CCCT-2347) | Re-parent under epic [CCCT-2067](https://dimagi.atlassian.net/browse/CCCT-2067) | — |
