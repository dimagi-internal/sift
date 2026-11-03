---
name: grooming-prep
description: >
  Prepare Connect's Thursday grooming session: pick the candidate CCCT tickets per team, check
  each against the definition of ready, draft the fixes (acceptance criteria, bug repro
  questions, splits), and produce a ranked agenda plus an approval-gated plan. Use on Sift's
  Wednesday schedule, or when asked to "prep grooming", "what's ready for grooming" or "get
  tickets ready for Thursday".
---

# Grooming prep — Sift

Reads are free. Jira writes (comments with drafted AC, field fixes) go only through
`bin/sift-jira apply` after approval. Read first:
- `context/definition-of-ready.md`: the standard you're checking against
- `context/delivery-model.md`: teams, Prioritization order (Must > Nice > Could), capacity method
- `context/capacity-snapshot.md`: next sprint's capacity and estimated velocity per team
- `context/decisions.md`: rulings and declined changes
- `context/2027-themes.md`: goals

Don't use the `connect-tech:groom-sprint-tickets` command. It runs only when a human invokes
it explicitly.

## 1. Pick candidates (per team: Mobile, Blue, Green)
1. Tickets already in the **next** sprint for that team (`customfield_10010`, state `future`,
   earliest one).
2. Then, until the candidates add up to about 1.5× the team's estimated velocity for that
   sprint (from the snapshot), take open Backlog-status CCCT tickets under epics whose CCC
   idea is **planned**. Rank them by:
   - Prioritization: Must > Nice > Could
   - then whether they move a 2027 goal
   - then CCC status, with Implementation before Technical Specification
3. Skip anything whose CCC idea has Prioritization `Backlog`. It's parked, not a candidate.

## 2. Check readiness
Run each candidate through the CCCT table in `context/definition-of-ready.md`. Also check
the parent epic's CCC idea against the four CCC items. An idea that isn't ready makes its
tickets a risk; say so once per idea, not once per ticket.

## 3. Draft the fixes
Draft only. Nothing is written until approved.
- **Story without AC:** draft 3–6 testable acceptance criteria from the description, the
  epic, the CCC idea and its spec. Keep them in plain language. Mark any guesses with "(confirm)".
- **Bug missing repro:** list the specific questions for the reporter.
- **Missing Team or epic:** propose a value, inherited from the epic or the assignee's team
  (`context/delivery-model.md` rosters).
- **An 8, or a ticket clearly bigger than a sprint:** propose a split, as titles only.
- Check principles: if a ticket conflicts with a Product Principle, flag it and quote the
  principle (`skills/product-principles`).

## 4. Report (the grooming agenda)
One report, one section per team. For each:
- **Capacity line:** next sprint's capacity days and estimated velocity versus the points
  already committed, with notes on who's out.
- **Ready:** tickets that pass, ranked, one line each with points.
- **Needs work before Thursday:** each gap, one line each, with the drafted fix linked or
  inlined.
- **Questions for the room:** decisions only humans can make, such as scope, splits and
  conflicting signals.

Link every key. Put the CCC-level risks at the top, then the plan: `comment` ops posting the
drafted AC or questions on each ticket, and `update` ops for Team or epic fixes.

## 5. Approval, then apply
Present the agenda and plan for approval. Struck lines go in `context/decisions.md`
(Declined changes), and any stated rule goes under Standing rulings. Then run
`bin/sift-jira apply plan.json --approved-by "<name>"` and report what applied.
