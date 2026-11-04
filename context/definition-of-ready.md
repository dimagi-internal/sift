# Definition of ready — CCC and CCCT

What a ticket needs before it moves forward. Set by Mary Rocheleau on 2026-11-03. Sift checks
work against it in triage and in Wednesday grooming prep (`skills/grooming-prep`). A gap is a
finding with a concrete fix, not a block: Sift proposes, and the PM or team decides.

## CCC idea → ready for Technical Specification
An idea moving into (or already in) `Technical Specification` or later needs all four:

| # | Needs | Check | Typical fix Sift proposes |
|---|---|---|---|
| 1 | **Owner** | `assignee` set | Ask the area's PM to name one; propose one if the Product Area makes it obvious |
| 2 | **Goal + Prioritization** | `Goal` (`customfield_14111`) set or a deliberate "none"; `Prioritization` (`customfield_12800`) set and not `Backlog` | Propose values. Never write either unprompted (see `context/decisions.md`) |
| 3 | **Spec doc linked** | A spec or design doc linked from the idea: a Confluence / Google Doc URL in the description, a remote link, or a linked spec issue | Ask the owner for the link. Offer to draft one from the idea (`jira-spec-doc` skill) |
| 4 | **Problem statement** | The description says the user problem and why it matters (who is affected and what goes wrong today), not just the solution | Draft a 2–3 line problem statement from the idea and linked tickets, for the owner to confirm |

Baseline on 2026-11-03: most Technical Specification and Implementation items have an owner and
a linked CCCT ticket, but few link a spec doc and few state the problem. Expect #3 and #4 to be
the common gaps. Report them as a count plus the in-flight items by name, rather than one
nag per item.

## CCCT ticket → ready to enter a sprint
A ticket in the next sprint, or a candidate for Thursday grooming:

| Applies to | Needs |
|---|---|
| All | A description a teammate could pick up cold; `Team` set; a parent epic (except Bugs and Tests) |
| All | A component that matches the team: `Web / Server` for Blue and Green, `Mobile` for Mobile (added 2026-11-04) |
| All | Dependencies named in the description are linked; a Blocked ticket names its blocker (added 2026-11-04) |
| **Story** | An **Acceptance Criteria** section: testable statements of done |
| **Task** | A clear statement of what "done" means. A formal AC section isn't required |
| **Bug** | Repro steps, expected vs. actual behavior, and where it was seen (platform/version, opportunity) |
| Estimated work | Story Points (`customfield_10017`) once groomed. An 8 is a smell, so suggest a split |
| Under a CCC epic | The epic links its CCC idea (`Polaris work item link`), and that idea is planned (not `Backlog`) |

- An assignee isn't required to be ready. The team assigns at planning.
- Points are expected *after* grooming, so a missing estimate on a grooming candidate is
  agenda, not a defect.
- Baseline on 2026-11-03: about half of in-sprint tickets have AC, and most have points and an
  epic.

## How Sift uses it
- **Grooming prep (Wednesday):** check every grooming candidate against the CCCT list. For
  each gap, draft the fix (proposed AC for a Story, repro questions for a Bug, a split for an 8)
  so grooming spends its time deciding, not writing.
- **Triage:** the "Under-specified" signal means failing this definition. For CCC, check the
  four items above on anything in Technical Specification or later.
- **Never** move a ticket's status because it's not ready. Flag it and propose the fix.
