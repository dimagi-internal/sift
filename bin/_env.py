"""Canonical .env resolver for Sift's scripts — reads the WORKTREE-CLEAN global home.

Sift runs each turn in a fresh emdash worktree; a per-repo `.env` would be absent there and
get recreated every turn. So secrets live ONCE at ~/.sift/.env (filled from .env.tpl
by /sift:setup — `canopy agent env --plugin sift`; override the home with
$sift_ENV, upper-cased). A repo-local `.env` still works as a per-KEY dev override (it wins).

    from _env import get, load
    val = get("sift_PRIMARY_CHANNEL", "")   # os.environ wins, then global .env, then default

Never `source` the .env from bash — values with `>`/`!`/`=` break shell parsing; use this module.
"""
import os

_SLUG = "sift"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOBAL_ENV = os.environ.get(_SLUG.upper() + "_ENV") or os.path.expanduser("~/." + _SLUG + "/.env")
REPO_ENV = os.path.join(REPO, ".env")
ENV_PATH = GLOBAL_ENV


def load(path=None):
    """Parse .env(s) into a dict — global home merged with an optional repo-local override (repo
    wins per key). Splits on the FIRST '=', value verbatim (so `>`/`!`/`=`/spaces survive)."""
    out = {}
    for p in ([path] if path else [GLOBAL_ENV, REPO_ENV]):
        if not p or not os.path.exists(p):
            continue
        for raw in open(p, encoding="utf-8"):
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                v = v[1:-1]
            out[k] = v
    return out


def get(key, default=None):
    """Resolve one var: os.environ first (caller override), then the .env home, else default."""
    if os.environ.get(key):
        return os.environ[key].strip()
    return load().get(key, default)
