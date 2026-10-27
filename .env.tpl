# Sift's env template — the fleet-standard `.env.tpl` + `op inject` provisioning
# path (canopy agent-core/agent-runtime.md). `op inject` resolves this file's 1Password refs into
# the WORKTREE-CLEAN global env home ~/.sift/.env (mode 0600) — NOT a per-worktree repo
# .env. emdash runs each turn in a fresh worktree, so a repo-local .env would vanish; every
# worktree instead reads the global home via bin/_env.py.
#
# Resolve with /sift:setup, i.e.:
#   canopy agent env --plugin sift --template .env.tpl --out ~/.sift/.env
# It binds this install to ONE agent instance on canopy-web and runs `op inject` with
# AGENT_VAULT set to that instance's recorded 1Password vault. NEVER write a vault name here:
# every ref names the vault as ${AGENT_VAULT}, never literally — the vault belongs to the instance, not
# to this repo (someone may run this agent with a different vault).
#
# CRITICAL: `op inject` resolves 1Password refs ANYWHERE IN THIS FILE, INCLUDING COMMENTS — a real
# reference left in a comment/example gets resolved too and can leak that secret to stdout on
# the next `op inject ... | cat` (or similar). NEVER paste a real item name in a comment. Every
# example below uses an angle-bracket PLACEHOLDER for the item (`<item>`) for exactly this
# reason — keep doing that when you add a var.
#
# One line per var, `KEY=value`. A literal (not environment-varying) value is fine as-is;
# anything that differs per environment — a key, an id, a folder — must be a 1Password reference,
# never the literal value. For a non-env credential FILE (e.g. an OAuth-client json), don't put
# it here — resolve it directly with `op read` into the file instead.
#
# The gog OAuth client is the SHARED fleet app (`canopy`), not per-agent: a gog "client" is the
# APP identity (client_id + client_secret), reused by every agent's mailbox. The per-agent,
# never-shared identity is the mailbox (sift@dimagi.ai).

sift_PRIMARY_CHANNEL=sift@dimagi.ai
# Jira (bin/sift-jira). Site and project list are literal; the account + API token are per-instance.
sift_JIRA_SITE=dimagi.atlassian.net
sift_JIRA_PROJECTS=CCC,CCCT
sift_JIRA_EMAIL=op://${AGENT_VAULT}/jira/username
sift_JIRA_API_TOKEN=op://${AGENT_VAULT}/jira/credential
# sift_SOME_SECRET=<1Password ref: AGENT_VAULT / item / field>
# Sift's own canopy-web token (login sift@dimagi.ai) — never fall back to a person's.
CANOPY_WEB_PAT=op://${AGENT_VAULT}/canopy-pat/credential
