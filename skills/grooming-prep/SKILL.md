---
name: grooming-prep
description: >
  Prepare Connect's Thursday grooming session for ONE sprint at a time. Starts by listing the
  upcoming sprints across the whole CCCT project and asking which one to prepare. Then checks
  every open ticket in that sprint for the right component, acceptance criteria, linked issues
  and an adequate description, drafts the changes each one needs, and reviews the sprint's
  capacity against what's planned. Produces one agenda plus an approval-gated plan. Use on
  Sift's Wednesday schedule, or when asked to "prep grooming", "what's ready for grooming",
  "prep Blue for grooming", "prep Sprint 103" or "get tickets ready for Thursday".
---

# Grooming prep — Sift

Reads are free. Jira writes (comments with drafted AC, field fixes, links) go only through
`bin/sift-jira apply` after approval. Read first:
- `context/definition-of-ready.md`: the standard you're checking against
- `context/delivery-model.md`: teams and rosters, Prioritization order (Must > Nice > Could),
  capacity method
- `context/capacity-snapshot.md`: the sprint's capacity and estimated velocity, and who's out
- `context/decisions.md`: rulings and declined changes. Never re-propose a declined change.

Don't use the `connect-tech:groom-sprint-tickets` command. It runs only when a human invokes
it explicitly.

## Shape: one sprint per run
Each run prepares **one Jira sprint**, which is one team's sprint (Mary, 2026-11-04). Never mix
two sprints' tickets into one set of findings or capacity numbers. To prep another sprint,
run the skill again. A ticket in the sprint that looks like it belongs to another team is a
finding on this sprint (see Component, below).

| Team | Jira `Team` (`customfield_10001`) | Expected component | Sprint name looks like |
|---|---|---|---|
| Blue | `Connect: Blue Web Team` | `Web / Server` | `Blue Pod - Sprint 103` |
| Green | `Connect: Green Web Team` | `Web / Server` | `Green Pod - Sprint 103` |
| Mobile | `Connect: Mobile Team` | `Mobile` | `Mobile Team - Sprint 103` |

## 0. Ask which sprint
Always start here, before reading any tickets. List the upcoming sprints across the **whole
CCCT project**:
```bash
bin/sift-jira upcoming-sprints
```
It reads future sprints from the tickets themselves, so it also finds sprints that aren't on
the three team boards (`bin/sift-jira sprints` misses some, e.g. Mobile's). The list is ordered
by sprint number; Mobile's future sprints often have no dates yet.

Ask which sprint to prepare (AskUserQuestion when the asker is present). Offer the soonest
sprints as options, each labeled with its name, start date (or "no dates yet"), ticket count
and points (e.g. "Green Pod - Sprint 103 — 16 Nov, 17 tickets, 45 pts + 6 unestimated").
Recommend the soonest sprint for the team the asker named, or the soonest sprint overall.
Teams share sprint numbers, so several sprints can be "next" at once; list them all.
- If the asker already named a sprint ("prep Green 103"), confirm it from the list and skip
  the question.
- If they named only a team ("prep Blue"), offer that team's upcoming sprints.
- On an unattended run (no one to ask), don't guess: post the list as the turn's output and
  stop.
- A sprint with tickets from several teams, or tickets with no Team, is a finding for step 2,
  not a reason to skip it.

## 1. Get the sprint's tickets
```bash
bin/sift-jira sprint-tickets <sprint_id>
```
This returns every open CCCT ticket in the sprint with its team, type, status, points,
components, parent and any other open sprint it's in. Then fetch each ticket in full with
`bin/sift-jira issue <KEY>` (run them in parallel) for the description, links and comments.
Also fetch each parent epic once, for its component, team and CCC link.

**Carry-over:** tickets already past `Backlog` / `To Do` (In Progress, In Review, In QA, Ready
for Deploy, Blocked) were started in an earlier sprint. Count them in capacity, list them
separately in the report, and don't run the readiness checks on them.

## 2. Check each planned ticket
Run every planned ticket through these four checks. A gap is a finding with a drafted fix, not
a block. Never move a ticket's status because it's not ready.

### Component
- `components` matches the team: `Web / Server` for Blue and Green, `Mobile` for Mobile. Both is
  fine when the ticket really spans both.
- It agrees with the summary's prefix (`[web]`, `[mobile]`) and with the parent epic.
- **Missing:** propose the team's component (`update`).
- **Contradicting:** e.g. a `[web]` ticket on the Mobile team, or `Mobile` on a Blue ticket.
  Either the component or the team is wrong. Flag it as a question for the room and don't pick
  one (`skills/clean-the-backlog` rule). If it moves teams it leaves this sprint's capacity, so say so.

### Acceptance criteria (by type, per the definition of ready)
- **Story:** an Acceptance Criteria section with testable statements. If it's missing or vague
  ("works as expected"), draft 3–6 testable criteria from the description, the epic, the CCC
  idea and any linked spec. Use plain language and mark guesses with "(confirm)".
- **Task:** a clear statement of what "done" means. If there isn't one, draft one or two lines.
- **Bug:** repro steps, expected vs. actual, and where it was seen (app or platform version,
  opportunity). List the specific questions for the reporter.
- **Design / Test:** say what the output is (a spec doc, a test plan). Flag it if that's unclear.

### Linked issues
- **Parent epic:** set for every type except Bug and Test. If it's missing, propose the obvious
  epic (`update` parent), or flag it if there isn't one.
- **Epic → roadmap:** the epic links its CCC idea (`Polaris work item link`), and that idea is
  planned (Prioritization set and not `Backlog`). Report a missing or parked idea **once per
  epic**, not once per ticket.
- **Dependencies:** a ticket named in the description ("Mobile counterpart: CCCT-2994",
  "after CCCT-2838") has a matching link. Web/mobile pairs link each other. Propose the
  `link` (Blocks / Relates).
- **Blocked:** a ticket in `Blocked` names its blocker with a link or a comment. Check the link
  direction too: "X blocks Y" should mean Y waits on X.
- **Duplicates:** if it's linked as a duplicate, check which one is still live.

### Description
The test: could a teammate who wasn't in the room pick it up cold? It needs:
- **What and why:** the change and the user or system problem it solves, not just a title
  restated.
- **Scope:** what's in and what's out, where that's ambiguous.
- **References:** a link to the spec or design when the epic or CCC idea has one, and the
  screens, endpoints or models involved.
If it's thin, draft the missing lines from the epic, the CCC idea and the linked tickets, for
the team to confirm. Don't rewrite a description that already passes.

Also note, but keep short:
- **Points:** missing points are agenda items for grooming, not defects. An 8, or a ticket
  clearly bigger than a sprint, gets a proposed split (titles only).
- **Product Principles:** if a ticket conflicts with one, flag it and quote the principle
  (`skills/product-principles`).

## 3. Review the sprint's capacity
Do this after the ticket checks, using `context/capacity-snapshot.md`. Refresh the snapshot
first (`skills/capacity-refresh`) if it's stale.
- **Capacity line:** the sprint's team capacity days and estimated velocity (rolling velocity per
  team-day × capacity days), with who's out or allocated elsewhere.
- **Planned load:** the sum of points on the planned tickets, plus the count of unestimated
  tickets. Leave out tickets your findings would move to another team, and say so.
- **Verdict:**
  - **Over (above about 1.2× velocity):** name what's likely to slip and propose what to drop,
    ranked by Prioritization (Could first, then Nice, then Must), then by how little the
    ticket moves a 2027 goal.
  - **Under (below about 0.8×):** suggest backlog candidates to pull in, up to about velocity.
    Take open Backlog-status tickets for this sprint's team that aren't in another sprint,
    under epics whose CCC idea is planned, ranked Must > Nice > Could, then by goal, then Implementation before Technical
    Specification. Run each through step 2 too. Skip ideas with Prioritization `Backlog`.
  - **About right:** say so in one line.
- The snapshot gives Web capacity for Blue and Green together. When there's no per-team split,
  estimate each team's share from its headcount after PTO and say it's an estimate.

## 4. Report: one sprint
Lead with the sprint's name, dates and team, then give:
1. **Ready:** the planned tickets that pass every check, one line each with points.
2. **Needs changes:** one line per ticket, grouped by check (Component / AC / Links /
   Description). Each line has the specific change: drafted AC inline, the field value, or the
   link to add.
3. **Capacity:** the capacity line, planned load and verdict, with what to drop or pull in.
4. **Questions for the room:** decisions only humans can make, like team moves, splits, scope
   and conflicting signals.

Link every key. Then give the plan: `comment` ops for drafted AC, done statements, description
additions and repro questions; `update` ops for components and epics (components replace the
whole list, so include the existing ones); `link` ops for missing dependencies. Field mechanics
are in `skills/clean-the-backlog` (CCCT hygiene). Dry-run the plan before presenting it:
`bin/sift-jira apply plan.json --approved-by "<name>" --dry-run`.

## 5. Approval, then apply
Present the agenda and plan for approval. Record struck lines in `context/decisions.md`
(Declined changes), and add any rule someone states to Standing rulings. Then run
`bin/sift-jira apply plan.json --approved-by "<name>"` and report what applied.
