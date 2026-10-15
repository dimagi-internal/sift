---
name: task-tracker
user-invocable: false   # internal: Claude invokes it; it is not a human-launchable /command
description: >
  Sift's project/task state — one board task per iterative thread/project, backed by
  canopy-web (kanban at /agents/sift). The canonical procedure is fleet-wide and lives
  in the installed canopy plugin (agent-core/task-tracker.md); this stub binds it to
  Sift. Use when taking on multi-turn work, when a new request arrives, and at every
  turn's board-drain and close.
---

# Task Tracker — Sift (stub over the fleet-canonical core)

1. **Resolve the installed canopy plugin and check freshness:**
   ```bash
   CANOPY=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['canopy@canopy'][0]['installPath'])")
   bash "$CANOPY/scripts/canopy-update-check.sh"
   ```
   `UPGRADE_AVAILABLE` → tell the human and run `/canopy:update` BEFORE following a stale core.
2. **Read `$CANOPY/agent-core/task-tracker.md`** and **follow it exactly**, bound to the
   Identity below. Where it says `<slug>`/`<mailbox>`, use this Identity.

## Identity
- Name: **Sift** · slug: `sift` · mailbox: `sift@example.com`
- Board: `/agents/sift` · Drive root env: `GDRIVE_ROOT_FOLDER` (from `~/.sift/.env`)

## Sift-local notes (the ONLY hand-edited section — fleet-process changes go to canopy)
- (none yet)
