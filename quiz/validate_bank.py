#!/usr/bin/env python3
"""Validate the quiz question bank: structure, per-format keys, and the
grounding gate (every item must cite a wiki/raw file that exists on disk).

Usage:  python validate_bank.py [questions.json]
Exit code 0 = pass, 1 = problems found.
"""
import json, sys, collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
BANK = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "questions.json"

def err(item_id, msg, errors): errors.append(f"[{item_id}] {msg}")

def main():
    data = json.loads(BANK.read_text(encoding="utf-8"))
    items = data["items"]
    errors, ids = [], set()
    fmt_count = collections.Counter()
    dom_count = collections.Counter()

    for it in items:
        i = it.get("id", "<no-id>")
        if i in ids: err(i, "duplicate id", errors)
        ids.add(i)
        for req in ("id","domain","subtopic","format","difficulty","stem","scoring","rationale","citations","version_target"):
            if not it.get(req): err(i, f"missing required field '{req}'", errors)
        if it.get("version_target") != "dbt-core-1.11":
            err(i, "version_target must be dbt-core-1.11", errors)
        fmt = it.get("format"); fmt_count[fmt]+=1; dom_count[it.get("domain","?")[:2]]+=1

        # grounding gate: >=1 citation pointing at an existing file
        cites = it.get("citations") or []
        if not cites: err(i, "no citations (grounding gate)", errors)
        for c in cites:
            w = c.get("wiki","")
            if not (w.startswith("wiki/") or w.startswith("raw/")):
                err(i, f"citation wiki path must start with wiki/ or raw/: {w}", errors)
            elif not (PROJECT / w).exists():
                err(i, f"cited source file does not exist: {w}", errors)

        # per-format key sanity
        if fmt == "mcq":
            opts = it.get("options") or []
            if len([o for o in opts if o.get("correct")]) < 1: err(i, "mcq has no correct option", errors)
            if not it.get("select_all") and len([o for o in opts if o.get("correct")]) > 1:
                err(i, "multiple correct options but select_all not set", errors)
        elif fmt == "domc":
            opts = it.get("options") or []
            if not any(o.get("correct") for o in opts): err(i, "domc has no correct option", errors)
        elif fmt == "fitb":
            for b in it.get("blanks") or []:
                if b.get("type")=="dropdown" and (not b.get("options") or b.get("answer") not in (b.get("options") or [])):
                    err(i, f"fitb dropdown blank {b.get('id')} answer not in options", errors)
                if b.get("type")=="short_answer" and not b.get("accepted"):
                    err(i, f"fitb short_answer blank {b.get('id')} has no accepted answers", errors)
        elif fmt == "matching":
            left = it.get("left") or []; key = it.get("key") or {}
            for l in left:
                if l not in key: err(i, f"matching left '{l}' missing from key", errors)
        elif fmt == "build_list":
            ids_ = {x.get("id") for x in it.get("items") or []}
            order = (it.get("answer") or {}).get("order") or []
            if set(order) != ids_: err(i, "build_list answer.order must cover exactly the item ids", errors)

    # report
    print(f"Bank: {BANK.name}  |  {len(items)} items")
    print("By format:", dict(fmt_count))
    print("By domain:", dict(sorted(dom_count.items())))
    if errors:
        print(f"\nFAILED — {len(errors)} problem(s):")
        for e in errors: print("  -", e)
        return 1
    print("\nPASS — all items valid and grounded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
