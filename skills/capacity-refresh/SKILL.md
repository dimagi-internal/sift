---
name: capacity-refresh
description: >
  Refresh Sift's picture of Connect team capacity, throughput and velocity from the Connect
  Tech Sprint Performance dashboard, and rewrite context/capacity-snapshot.md. Use when the
  snapshot is over 14 days old, when a new sprint has started since its date, before a
  capacity/prioritization answer, or when asked to "refresh capacity", "check velocity" or
  "how loaded are the teams".
---

# Capacity refresh — Sift

Read-only. It touches nothing outside this repo's `context/capacity-snapshot.md`.

## When
- **Every turn:** check the date line at the top of `context/capacity-snapshot.md`. If it is
  over 14 days old, or the sprint it calls "in progress" has ended (sprints are two weeks,
  starting Monday; see `context/delivery-model.md`), refresh before any triage, prioritization
  or capacity answer. Otherwise use the snapshot as it is.
- On request, at any time.

## Source: the dashboard (preferred)
Site: https://sites.google.com/dimagi.com/connect-sprint-performance/connect-sprint-metrics
Each page embeds a Google Apps Script web app inside a sandboxed iframe. There's no
readable API, and `get_page_text` on the Sites page returns only navigation. So:
1. Open each page in the browser (Claude in Chrome, which has the dimagi.com sign-in). Use
   the Sites URLs below. Navigating straight to an Apps Script `/exec` URL also works.
2. Wait about 6 seconds for the data to load, then read it from **screenshots**, scrolling
   down. The Sprint History table on the main page is the key data. Zoom on it if the
   numbers are small.
3. Close your tab when done.

| Page | URL path | Capture |
|---|---|---|
| Connect Sprint Metrics | `/connect-sprint-metrics` | Current/upcoming sprint header: capacity days, rolling vel/day, each pod's estimated velocity, **Capacity Notes** (PTO, allocations). **Sprint History table**: last ~10 sprints × capacity / commitment / velocity / % complete, Total / Mob / Web |
| Sprint Summary | `/sprint-summary` | Latest sprint's delivery summary for Mobile and Web (only when it's useful context) |
| Interrupt | `/interrupt` | Total open, bugs / tasks, P3 / P4, median age, median cycle time and its trend |
| Flow & Discovery | `/flow-discovery` | Backlog Flow: open, median backlog age, lead time, cycle time, created vs. resolved. Discovery Funnel tab: idea counts by stage, discovery and build lead time, ideas not yet linked |
| Quality | `/quality` | Open pre-deploy bugs, bugs logged this sprint, bug cycle time, escaped defect rate, test automation coverage |
| DORA | `/dora` | Web tab: deploy frequency and lead time per repo, incidents per deploy, MTTR |

## Fallback: Jira
If no browser is available (for example a cloud runner), don't skip the refresh. Recompute
what you can from `bin/sift-jira search`:
- velocity = Story Points of CCCT tickets resolved in each closed sprint (`customfield_10010`),
  by team
- open WIP by status
- lead time and cycle time from the changelog

Mark the snapshot **"Jira-derived, dashboard not read"**. Jira undercounts because many tickets
lack a Team, so treat team-level numbers as a lower bound.

## Write the snapshot
Rewrite `context/capacity-snapshot.md` in its existing shape:
- date line and source
- sprint table (newest first, about 10 sprints)
- read-outs: average throughput, rolling vel/day vs. target, commitment vs. velocity,
  capacity trend
- the upcoming sprint's capacity notes
- the Flow, Discovery, Interrupts, Quality and DORA sections

Keep the read-outs to judgments Sift will reuse. Don't transcribe every chart.

Then compare with the previous snapshot (`git diff`). Put anything that moved enough to change
a recommendation in the turn report, in one line each. Examples: velocity down more than 20%,
a pod's capacity cut by PTO, interrupt cycle time spiking, commitment far above estimate.

Ship it like any other repo change (`skills/shipping`). It's a context file, so a direct
commit to a branch, a PR and a self-merge are fine.
