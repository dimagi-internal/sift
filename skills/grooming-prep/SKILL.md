---
name: grooming-prep
description: >
  Prepare Connect's Thursday grooming session for ONE sprint at a time, focused on ticket
  quality. Starts by listing the upcoming sprints across the whole CCCT project and asking which
  one to prepare. Then checks every planned ticket in that sprint for a clear description,
  acceptance criteria (or the type's equivalent) and links to related tickets, especially
  anything that could block it, and drafts the changes each one needs. Produces one agenda plus
  an approval-gated plan. Capacity is out of scope for now. Use on Sift's Wednesday schedule, or
  when asked to "prep grooming", "what's ready for grooming", "prep Blue for grooming",
  "prep Sprint 103" or "get tickets ready for Thursday".
---

# Grooming prep — Sift

Reads are free. Jira writes (comments with drafted AC, field fixes, links) go only through
`bin/sift-jira apply` after approval. Read first:
- `context/definition-of-ready.md`: the standard you're checking against
- `context/delivery-model.md`: teams, rosters and the CCCT flow
- `context/decisions.md`: rulings and declined changes. Never re-propose a declined change.

Don't use the `connect-tech:groom-sprint-tickets` command. It runs only when a human invokes
it explicitly.

## Scope: ticket quality only
This skill checks whether the sprint's tickets are **ready to be worked**: a clear description,
acceptance criteria and links to related or blocking tickets (Mary, 2026-11-04). It does not
review capacity, points or what to drop or pull in. That may come back later; until then,
don't add it to the report.

## Shape: one sprint per run
Each run prepares **one Jira sprint**, which is one team's sprint (Mary, 2026-11-04). Never mix
two sprints' tickets into one set of findings. To prep another sprint,
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
for Deploy) were started in an earlier sprint. List them separately in the report and don't
run the readiness checks on them. A ticket in `Blocked` is the exception: run the Links check
on it, since its blocker is exactly what grooming needs to see.

## 2. Check each planned ticket
Run every planned ticket through these three checks, in this order. A gap is a finding with a
drafted fix, not a block. Never move a ticket's status because it's not ready.

### Description
The test: could a teammate who wasn't in the room pick it up cold? It needs:
- **What and why:** the change and the user or system problem it solves, not just the title
  restated.
- **Scope:** what's in and what's out, where that's ambiguous. Watch for sentences that
  contradict each other, and for open questions left in the description ("Open product
  question: …"). An open question is a question for the room, not a pass.
- **References:** a link to the spec or design when the epic or CCC idea has one, and the
  screens, endpoints or models involved.
- **Decisions made in comments:** if a comment settles something (wording, scope, an
  approach), the description should say it too. Draft the line to add.
If it's thin, draft the missing lines from the epic, the CCC idea and the linked tickets, for
the team to confirm. Don't rewrite a description that already passes.

### Acceptance criteria (by type, per the definition of ready)
- **Story:** an Acceptance Criteria section with testable statements. If it's missing or vague
  ("works as expected", "emails to be sent"), draft 3–6 testable criteria from the
  description, the epic, the CCC idea and any linked spec. Use plain language and mark guesses
  with "(confirm)".
- **Task:** a clear statement of what "done" means ("Done when" counts). If there isn't one,
  draft one or two lines.
- **Bug:** repro steps, expected vs. actual, and where it was seen (app or platform version,
  opportunity). A description of the fix is not a repro. List the specific questions for the
  reporter.
- **Design / Test:** say what the output is (a spec doc, a test plan) and where it lives. Flag
  it if that's unclear.

### Links to related tickets and blockers
The question for each ticket: **is anything it depends on missing, unlinked or not going to be
ready in time?**
1. **Find what it depends on.** Look for:
   - tickets named in the description or comments ("Depends on CCCT-2996", "Mobile
     counterpart: CCCT-2994", "after CCCT-2838");
   - its web/mobile counterpart (same feature, `[web]` / `[mobile]` prefix, often in the same
     epic);
   - siblings in the same epic whose work it builds on (a model, an endpoint, a screen it
     extends).
2. **Check each one is linked**, with the right type and direction: "X blocks Y" means Y waits
   on X; use Relates for a pair that doesn't wait on each other. Propose any missing `link`.
3. **Check each blocker will be ready.** For every ticket this one is blocked by:
   - Done → fine.
   - In this sprint → fine, but say the order if both are in the sprint.
   - In the current sprint and not started, in a later sprint, or in no sprint → **finding**:
     this ticket can't start until it moves. Say which.
4. **Status `Blocked`:** it names its blocker with a link or a comment.
5. **Stale links:** a link to a Won't Do or duplicate ticket ("implements CCCT-2728 [Won't
   Do]") is a finding. Say what it should point to instead, if anything.
6. **Parent epic:** set for every type except Bug and Test. If it's missing, propose the obvious
   epic (`update` parent), or flag it if there isn't one. Once per epic, check the epic links a
   CCC idea (`Polaris work item link`).

Also note, but keep short:
- **Component:** `Web / Server` for Blue and Green, `Mobile` for Mobile. Propose it when
  missing; when it contradicts the team or the `[web]` / `[mobile]` prefix, flag it as a
  question for the room and don't pick one.
- **Product Principles:** if a ticket conflicts with one, flag it and quote the principle
  (`skills/product-principles`).

## 3. Report: one sprint
Lead with the sprint's name, dates and team, then give:
1. **Ready:** the planned tickets that pass every check, one line each.
2. **Needs changes:** one line per ticket, grouped by check (Description / AC / Links). Each
   line has the specific change: drafted AC inline, the line to add, or the link to add.
3. **Blockers at risk:** tickets whose blocker isn't done and isn't scheduled ahead of them.
4. **Carry-over:** tickets already started, one line each, unchecked.
5. **Questions for the room:** decisions only humans can make, like open product questions,
   scope, splits, team moves and conflicting signals.

Link every key. Then give the plan: `comment` ops for drafted AC, done statements, description
additions and repro questions; `link` ops for missing dependencies; `update` ops for epics and
components (components replace the whole list, so include the existing ones). Field mechanics
are in `skills/clean-the-backlog` (CCCT hygiene). Dry-run the plan before presenting it:
`bin/sift-jira apply plan.json --approved-by "<name>" --dry-run`.

## 4. Approval, then apply
Present the agenda and plan for approval. Record struck lines in `context/decisions.md`
(Declined changes), and add any rule someone states to Standing rulings. Then run
`bin/sift-jira apply plan.json --approved-by "<name>"` and report what applied.
