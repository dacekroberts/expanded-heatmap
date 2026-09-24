"""The app's city registry: one entry per city page, one page per entry.

    python scripts/check_city_registry.py
    python scripts/check_city_registry.py --file some/cities.py   # for controls

Exits non-zero naming every problem. Read-only; needs only the standard
library, so it runs in either environment.

WHY. On 2026-09-24 merging Rome's branch with master FUSED two cities'
appended `app/cities.py` entries into ONE dict: the conflict region held only
each entry's interior, so resolving it dropped the `}, {` between them.
Rome's keys silently overwrote Amsterdam's. The file parsed, the app loaded,
and the site listed 29 cities with no Amsterdam - no error anywhere. The build
session caught it by counting (DECISIONS.md, "Rome: the page text written,
notices 36 and 37, merged with Amsterdam").

TWO TESTS, because the failure has two faces:

  1. DUPLICATE KEYS in any dict literal in the file. A fused entry has two
     "name"s and two "page"s, and Python keeps the last without a word. This
     is read from the SOURCE (ast), because once the module is imported the
     duplicate is already gone - which is the whole problem.
  2. PAGES <-> ENTRIES. Every app/pages/*_Heatmap.py is referenced by exactly
     one CITIES entry's "page", every entry's "page" exists, and no two entries
     share a name. A fused merge leaves one page with no entry.
"""
import argparse
import ast
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def literal_key(node):
    try:
        return ast.literal_eval(node)
    except ValueError:
        return ast.dump(node)


def duplicate_keys(tree):
    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [literal_key(k) for k in node.keys if k is not None]
        for key, n in Counter(keys).items():
            if n > 1:
                problems.append(f"line {node.lineno}: a dict repeats the key {key!r} "
                                f"{n} times - Python keeps only the last. Two entries "
                                f"fused in a merge look exactly like this.")
    return problems


def city_entries(tree):
    """The dict literals in the module-level CITIES list, read from source."""
    for node in tree.body:
        targets = (node.targets if isinstance(node, ast.Assign)
                   else [node.target] if isinstance(node, ast.AnnAssign) else [])
        if any(isinstance(t, ast.Name) and t.id == "CITIES" for t in targets):
            if isinstance(node.value, ast.List):
                return [e for e in node.value.elts if isinstance(e, ast.Dict)]
    sys.exit("no `CITIES = [...]` list literal found - the registry changed shape; "
             "update this check rather than let it pass vacuously")


def field(entry, name):
    """The value PYTHON would see: the LAST occurrence of a repeated key. The
    first control read the first occurrence and reported Rome's page as the
    orphan, when in the real merge Rome overwrote Amsterdam and Amsterdam
    was the city that vanished."""
    found = None
    for k, v in zip(entry.keys, entry.values):
        if k is not None and literal_key(k) == name:
            try:
                found = ast.literal_eval(v)
            except ValueError:
                found = None
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=Path, default=APP / "cities.py")
    args = ap.parse_args()
    tree = ast.parse(args.file.read_text(encoding="utf-8"))

    problems = duplicate_keys(tree)
    entries = city_entries(tree)
    names = [field(e, "name") for e in entries]
    pages = [field(e, "page") for e in entries]

    for name, n in Counter(names).items():
        if n > 1:
            problems.append(f"{n} entries are named {name!r}")
    for page, n in Counter(pages).items():
        if n > 1:
            problems.append(f"{n} entries point at {page!r}")
    for name, page in zip(names, pages):
        if not page:
            problems.append(f"{name!r} has no \"page\"")
        elif not (APP / page).exists():
            problems.append(f"{name!r} points at {page!r}, which does not exist")
    on_disk = {f"pages/{p.name}" for p in (APP / "pages").glob("*_Heatmap.py")}
    for page in sorted(on_disk - set(pages)):
        problems.append(f"{page} has NO entry in cities.py - it is on disk but the "
                        f"app will never list it (a fused merge leaves exactly this)")

    if problems:
        for p in problems:
            print(f"  PROBLEM  {p}")
        print(f"\n{len(problems)} problem(s) in {args.file.name}")
        return 1
    print(f"OK - {len(entries)} entries, {len(on_disk)} city pages, one to one; "
          f"no dict in {args.file.name} repeats a key.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
