# Sift — what it does and how to start using it

Sift is Dimagi's backlog and roadmap agent for Connect. It keeps the Jira backlogs honest so
product people spend their time deciding, not grooming. It recommends; product people decide.

## Who it's for
Connect product people: the PMs and product leads who own the roadmap (Jira `CCC`, Connect
Roadmap) and the delivery backlog (`CCCT`, Connect Tech). Sift also watches the `CI` (Connect
Interrupt) board.

## What Sift does

| You ask / it runs | What you get |
|---|---|
| **Intake of new CCC ideas** ("triage new CCC items") | Every idea created since the last run is checked for the four intake basics: Prioritization, Goal, a good description, and 1–2 Product Areas. Sift proposes the missing values and drafts a short problem statement for the owner to confirm. |
| **Backlog triage** ("triage the backlog", "clean up CCCT") | A ranked change list: stale, unowned, unestimated, duplicate, under-specified, mis-prioritized or mis-classified tickets, each with a concrete fix (close as a duplicate of X, ask for acceptance criteria, re-rank under epic Y). Also flags roadmap items with no delivery tickets, and tickets whose priority doesn't trace to a roadmap item. |
| **Stale-ticket review** (monthly) | Per ticket in one project (CCCT or CCC): close, nudge, or leave. |
| **Interrupt review** (weekly) | On the CI board: tickets nobody owns, that stopped moving, that have been open too long, or that don't belong there. Each gets a nudge, a flag, or a re-home. |
| **Interrupt summary** (monthly, "interrupt summary") | The shared "Connect Interrupt Summary" page, rebuilt for the last six months: CI tickets per month by type, what each category of request is, and the product change that would take it off the board. Published after you approve the draft. |
| **Grooming prep** ("prep grooming", "what's ready for Thursday") | One agenda per team (Blue, Green, Mobile): every CCCT ticket in the next sprint checked for component, acceptance criteria, links and description, with drafted fixes, and the team's capacity set against what's planned. |
| **Roadmap questions** ("where does this fit?", "what matters most?") | Answers framed by the five 2027 goals (below), with capacity from the real team rosters, so recommendations are sized in sprints, not item counts. |
| **Product-principles check** | Flags work that conflicts with a settled decision, notices when a new decision has been made, and drafts updates to the Confluence page. |
| **Capacity refresh** | Re-reads the Connect Tech Sprint Performance dashboard for velocity and capacity, so sizing stays current. |

Schedules (on canopy-web, America/New_York):
- **Tuesday 08:00**: backlog sweep (roadmap intake, then triage and interrupts, plus the monthly stale, principles and interrupt-summary reviews when due).
- **Wednesday 08:00**: grooming prep for Thursday's grooming.

Sift can also be asked at any time, in plain language.

### The lens: Connect 2027 goals
Not in priority order. Detail and the Jira `Goal` mapping: `context/2027-themes.md`.
1. Reliable self-serve FLW identity
2. Program integrity and traceability
3. Platform health, security and support
4. LLO network and multi-org model
5. Data access for LLOs, funders and Labs

### Standards Sift checks against
- `context/definition-of-ready.md`: what a CCC idea needs to reach Technical Specification, and what a CCCT ticket needs to enter a sprint.
- `context/delivery-model.md` and `context/capacity-snapshot.md`: teams, rosters, how work flows, current capacity.
- `context/decisions.md`: standing rulings and changes people have declined. Sift reads it before proposing anything and never re-proposes a declined change.
- The [Connect Product Principles](https://dimagi.atlassian.net/wiki/spaces/connect/pages/4480958467/Connect+Product+Principles) page.

## How it works with you
1. **Reads are free.** Sift searches Jira, Confluence and the dashboard without asking.
2. **Writes need your approval.** Every finding becomes a reviewable change plan. Sift presents the batch; a human approves, strikes or rewords; only then does it apply the plan to Jira (`bin/sift-jira apply`, stamped with who approved it). Sift cannot write to Jira, Confluence or Slack any other way. This is enforced by rails in `config/gating.json`, not just by instruction.
3. **It learns your rulings.** When you strike a change or state a rule ("don't flag X"), Sift logs it in `context/decisions.md` so it holds next time.
4. **It reports plainly.** What it did, its recommendation, and what else it could do. Tickets are always linked.

Sift does not set strategy or decide what goes on the roadmap.

## Getting started

**Just talking to Sift (most people)**
- Email **sift@dimagi.ai**, or use Sift's page on canopy-web: `/agents/sift` (the board is where work is queued and approvals happen).
- Say what you want in plain words: "triage new CCC items", "prep Blue for grooming", "which CCCT tickets in Sprint 103 aren't ready?".
- Access is granted on canopy-web. Someone who can steer Sift (today: Mary Rocheleau, the owner) adds you to the Sift agent's access list there. Without a grant, Sift treats your message as read-only and surfaces it to the owner instead of acting on it.
- You approve or decline the change plans Sift brings back. That is the whole interaction.

**Running Sift on your own machine (people who maintain it)**
1. Install Claude Code with the **canopy** plugin and CLI (Sift builds on it; shared infrastructure lives there, not in this repo).
2. Get this repo: `github.com/dimagi-internal/sift`.
3. Run `/sift:setup`. It binds the install to one Sift instance on canopy-web and fills `~/.sift/.env` (Jira and Confluence credentials) from that instance's Canopy vault. If it finds no instance, ask the owner to add you to the agent's workspace.
4. Start a turn by telling Claude "do a turn" (follows `skills/turn/SKILL.md`).

## Maintaining Sift
- Identity and voice: `persona.md`. Standing instructions: `CLAUDE.md`.
- Skills (`skills/*/SKILL.md`) hold the procedures; `bin/` holds the Jira, Confluence and email tools.
- Code changes ship by branch, PR and self-merge (no human code review). Runtime guardrails still apply: outbound actions need human approval.
