#!/usr/bin/env python3
"""Bump this agent plugin's PATCH version in lock-step across every file that
carries it. Run from the repo root (or anywhere — paths resolve off this file).

The three fields that MUST agree, and drifted in the past when hand-bumped:
  * .claude-plugin/plugin.json          -> version
  * .claude-plugin/marketplace.json     -> metadata.version
  * .claude-plugin/marketplace.json     -> plugins[*].version

Used by the auto-version-bump GitHub Action (bump-on-every-merge, GitHub #357)
and runnable by hand. Prints "OLD -> NEW". stdlib only.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKET = ROOT / ".claude-plugin" / "marketplace.json"


def bump_patch(version: str) -> str:
    parts = version.strip().split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise SystemExit(f"unparseable version: {version!r}")
    parts[2] = str(int(parts[2]) + 1)
    return ".".join(parts)


def _load(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _save(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def main() -> None:
    plugin = _load(PLUGIN)
    old = plugin.get("version")
    if not old:
        raise SystemExit("plugin.json has no version")
    new = bump_patch(old)
    plugin["version"] = new
    _save(PLUGIN, plugin)

    if MARKET.exists():
        market = _load(MARKET)
        market.setdefault("metadata", {})["version"] = new
        for entry in market.get("plugins", []):
            entry["version"] = new
        _save(MARKET, market)

    print(f"{old} -> {new}")


if __name__ == "__main__":
    main()
