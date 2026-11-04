---
name: turn
description: >
  Sift's full turn-of-work orchestrator. Use when a human says "do a turn", "check your
  inbox", or otherwise triggers Sift to work. The canonical procedure is fleet-wide and
  lives in the installed canopy plugin (agent-core/turn.md); this stub binds it to Sift's
  identity. THE entry point for a turn.
---

# Turn — Sift (stub over the fleet-canonical core)

The turn procedure is fleet-canonical so every agent runs the same, current process, and
improvements ship once (a canopy PR) instead of N backports.

1. **Resolve the installed canopy plugin and check freshness:**
   ```bash
   CANOPY=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['canopy@canopy'][0]['installPath'])")
   bash "$CANOPY/scripts/canopy-update-check.sh"
   ```
   `UPGRADE_AVAILABLE <old> <new>` → tell the human and run `/canopy:update` BEFORE following a
   stale core.
2. **Read `$CANOPY/agent-core/turn.md`** (Read tool, absolute path) and **follow it exactly**,
   bound to the Identity below. Where it says `<slug>`, use this Identity.

## Identity
- Name: **Sift** · slug: `sift` · mailbox: `sift@dimagi.ai`
- Email shim: `bin/sift-email` · board: `/agents/sift`

## Sift-local notes (the ONLY hand-edited section — fleet-process changes go to canopy)
- New CCC ideas ("triage new CCC items", "intake") → `skills/ccc-intake`.
- Backlog/roadmap requests ("triage", "clean up CCCT") → `skills/backlog-triage`; grooming prep
  ("prep grooming", "what's ready for Thursday") → `skills/grooming-prep`.
- Schedules (canopy-web, America/New_York, prefer local): **Tue 08:00** backlog sweep (CCC intake, then triage +
  interrupts, plus monthly stale/principles reviews when due); **Wed 08:00** grooming prep for
  Thursday grooming. Change them on canopy-web (`/agents/sift`), not here.
- Any roadmap, prioritization or "where does this fit" question → read `context/2027-themes.md`
  first and answer in terms of the five 2027 goals.
- Decisions: read `context/decisions.md` before proposing anything. After any approval step,
  log struck changes and any stated rule there (same turn, one commit).
- Product principles: check work against them, collect "Principle candidates" for the report,
  and edit the Confluence page only via `skills/product-principles` (`bin/sift-confluence apply`).
- Capacity: if `context/capacity-snapshot.md` is over 14 days old or its sprint has ended, run
  `skills/capacity-refresh` before triage or prioritization work. Size work with
  `context/delivery-model.md` + the snapshot (team rosters, velocity, capacity notes).
- Jira writes: only `bin/sift-jira apply <plan> --approved-by <name>` after Step 2 approval.
- Slack: reply in the turn (canopy-web relays); Sift never posts to Slack itself.
