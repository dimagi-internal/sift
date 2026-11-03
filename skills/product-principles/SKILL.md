---
name: product-principles
description: >
  Read, apply and maintain the Connect Product Principles — the Confluence page of product
  principles and decisions that have been made (payments, visits, FLW communication, support).
  Use it to check roadmap items and tickets against settled decisions, and to draft and apply
  updates to the page once a human approves them. Triggers: "add a principle", "we decided
  X", "update the principles", "does this conflict with our principles", and any triage or
  roadmap judgment where a settled decision applies.
---

# Product principles — Sift

**Source of truth:** [Connect Product Principles](https://dimagi.atlassian.net/wiki/spaces/connect/pages/4480958467/Connect+Product+Principles)
(page `4480958467`, owned by Mary Rocheleau). It links out to the
[2–3 Year Vision](https://dimagi.atlassian.net/wiki/spaces/connect/pages/3457286146/Connect+Product+Platform+2-3+Year+Vision)
for overall direction. The page wins over any summary, including the one in CLAUDE.md.

Reads are free. A page edit is a public write: it happens **only** through
`bin/sift-confluence apply`, after the human approves the exact wording.

## 1. Reference: apply the principles
- **Read the live page** at the start of any triage, stale review or roadmap answer:
  `bin/sift-confluence page 4480958467` (gives text plus version).
- **A conflict is a finding.** When a ticket, idea or proposal contradicts a principle, flag it,
  quote the principle and link the page. Examples:
  - a flow that ends in "contact Dimagi support" conflicts with **Support** (fully self-service)
  - paying on form submission conflicts with **Payments** (pay on approval)
  - FLWs claiming unfunded work conflicts with **Conducting visits**
  - a rejection with no FLW-readable reason conflicts with **Communicating with FLWs**
- **Don't re-litigate.** A settled principle is not an open question. Don't propose
  alternatives to it unless the asker asks to revisit it.
- **Goals vs. principles:** the 2027 goals (`context/2027-themes.md`) say what to work on. The
  principles say how the product must behave. Work can be on-goal and still break a principle.

## 2. Spot candidate updates
Sift doesn't decide principles; it notices when one may have been made. A candidate is a
**durable product rule**: a statement about how Connect must always or never behave that
future work should follow. One-off ticket calls and implementation details don't count.
Sources:
- The person in the turn saying "we decided…", "going forward…", "the rule is…".
- CCC idea descriptions and comments, spec decisions, and resolved debates in tickets read
  during a sweep.
- A recurring conflict, where the same question comes up across several tickets, which shows
  a missing principle.

Collect candidates as you work. **Don't interrupt a sweep for them.** List them at the end of
the turn report under **"Principle candidates"**: one line each, with the proposed wording,
section and source link. If a candidate contradicts an existing principle, say so plainly:
that's a change to a principle, not an addition.

## 3. Update the page (on request, or once a candidate is accepted)
1. Read the current page and save its body:
   `bin/sift-confluence page 4480958467 --storage <scratch>/principles.html`. Note `version`.
2. Draft the edit in the page's own style:
   - short, declarative bullets
   - the "(not …)" contrast when it clarifies
   - FLW, LLO and Connect terms as the page uses them
   - placed under the right existing section, or a new `## Regarding <topic>` heading when none fits

   Edit only what's needed; leave every other node untouched, including `local-id`s and
   macros. Keep the storage XHTML valid (`<li><p>…</p></li>` inside the section's `<ul>`).
3. Write the plan: `{"page_id": "4480958467", "base_version": <version>, "summary": "<one
   line>", "body_file": "<scratch>/principles.new.html"}`. Run `bin/sift-confluence apply
   <plan> --approved-by "<name>" --dry-run` to get the diff.
4. **Present for approval:** show the diff, the section, and why it's a principle. Ask once.
   Reword on feedback and dry-run again.
5. After an explicit yes, run `bin/sift-confluence apply <plan> --approved-by "<approver>"`.
   - `REFUSED: … version` means someone edited the page in the meantime: go back to step 1.
     Never force it.
   - Report the new version and link.
6. Update the principles summary in `CLAUDE.md` (Standing context) to match. It's a short
   pointer list, so keep it to one line per principle.

## Periodic review
On a monthly cadence (or when asked "what should we add to the principles?"), roll up the
candidates collected since the last review, plus any repeated conflicts from triage. Present
them as one numbered batch for the owner to pick from. Never edit the page without that pick.
