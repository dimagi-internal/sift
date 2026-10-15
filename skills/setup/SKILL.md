---
name: setup
description: >
  Set up this machine to run Sift: bind this install to ONE agent instance on
  canopy-web and fill ~/.sift/.env from that instance's 1Password vault. Use on first
  run, a new machine, or a missing/stale .env.
argument-hint: "[--agent <instance>] [--vault <name>] [--force]"
---

# Setup — Sift

A plugin is code; an **instance** is canopy-web's Agent record — identity, workspace and
1Password vault. This install is bound to exactly ONE instance, chosen here, once. Using a
different instance means running this again (with `--force`).

Run, from this repo's root (pass through any arguments the user gave — `$ARGUMENTS`):

```bash
canopy agent env --plugin sift --template .env.tpl --out ~/.sift/.env $ARGUMENTS
```

Read its output and act on it — never guess past it:

- **one instance** → it says which one it bound to and how many vars it wrote. Done.
- **several instances** → it lists each with the exact re-run line. Ask the user which one
  this install is for, then run that line. Do not pick one yourself.
- **no instance** → the user cannot see any Sift instance on canopy-web; they need
  its owner to add them to the agent's workspace.
- **no vault recorded** → the instance's owner must set its 1Password vault on canopy-web
  (`/agents/<slug>` → Settings). There is no default vault name.
- **1Password errors** → it names the vault and `dimagi.1password.com`; the user signs in
  (`op signin`) or asks the agent's owner for access to that vault.
- **already bound to another instance** → only re-run with `--force` if the user means to
  switch this install to a different instance.

`canopy agent env --plugin sift --print` shows the resolved instance and vault as
JSON without changing anything.
