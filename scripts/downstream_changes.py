"""What a push changed that the Visuals and Analytics sessions build from.

    python scripts/downstream_changes.py <old-ref> [<new-ref>]   # new defaults to HEAD
    python scripts/downstream_changes.py --selftest              # touches nothing

Prints a message ready to send to both sessions (docs/session_roles.md,
"Downstream sessions"), or "nothing downstream" and exits 0 either way.
Read-only; standard library only.

WHY. The Visuals session's city cards are built from `city_notices()`, the
city registry and each city's outputs; the Analytics session reads each
city's outputs and processed data. Neither sees master move. On 2026-10-02
both had to be told by hand that the notices had landed, and the owner asked
for a standing rule (2026-10-03): tell them whenever their inputs change or a
city lands.

WHAT COUNTS as downstream, by path:
  - a city added to or removed from `app/cities.py` (read from source by ast);
  - any other change to `app/cities.py` (labels, regions, modes, tiers);
  - `outputs/<city>/`: a re-rendered map, changed station or business files;
  - the notices or credits in `app/components.py`;
  - `app/macro_facts.json`;
  - category rules and taxonomies (`docs/category_rules.md`,
    `docs/excluded_categories.md`, `pipeline/taxonomies/`);
  - licence rows (`docs/data_sources.md`, `docs/data_sources/*.md`,
    `docs/licence_positions.md`), which decide card credits;
  - `pipeline/map_common.py` and `pipeline/theme.py` (map look and colors).
Each city's `pipeline/<city>/` change shows up through its outputs, so it is
not listed separately.
"""
import argparse
import ast
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Above this many cities with the same changed files, the line gives a count.
MAX_NAMED = 12

# (label, test on a repo-relative POSIX path), checked in order; first match wins.
GROUPS = [
    ("City registry (app/cities.py)", lambda p: p == "app/cities.py"),
    ("Notices and credits (app/components.py)", lambda p: p == "app/components.py"),
    ("Macro-map facts (app/macro_facts.json)", lambda p: p == "app/macro_facts.json"),
    ("Category rules and taxonomies",
     lambda p: p in ("docs/category_rules.md", "docs/excluded_categories.md")
     or p.startswith("pipeline/taxonomies/")),
    ("Licence rows (card credits)",
     lambda p: p in ("docs/data_sources.md", "docs/licence_positions.md")
     or p.startswith("docs/data_sources/")),
    ("Map look (shared map code and theme)",
     lambda p: p in ("pipeline/map_common.py", "pipeline/theme.py")),
]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def city_names(source):
    """The "name" of every dict in CITIES, read without importing the module."""
    if source is None:
        return set()
    for node in ast.parse(source).body:
        if (isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CITIES" for t in node.targets)
                and isinstance(node.value, ast.List)):
            names = set()
            for item in node.value.elts:
                if isinstance(item, ast.Dict):
                    for k, v in zip(item.keys, item.values):
                        if (isinstance(k, ast.Constant) and k.value == "name"
                                and isinstance(v, ast.Constant)):
                            names.add(v.value)
            return names
    return set()


def show(ref, path):
    try:
        return git("show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None


def summarize(paths, old_cities, new_cities):
    """The message lines for a list of changed paths and two city-name sets."""
    lines = []
    added = sorted(new_cities - old_cities)
    removed = sorted(old_cities - new_cities)
    if added:
        lines.append(f"Cities added ({len(added)}): {', '.join(added)}")
    if removed:
        lines.append(f"Cities removed ({len(removed)}): {', '.join(removed)}")
    outputs = defaultdict(set)
    grouped = defaultdict(list)
    for p in paths:
        parts = p.split("/")
        if parts[0] == "outputs" and len(parts) > 2:
            outputs[parts[1]].add(parts[-1])
            continue
        for label, test in GROUPS:
            if test(p):
                grouped[label].append(p)
                break
    if outputs:
        # One line per distinct set of changed files; a full re-render
        # names its count, not 144 slugs.
        by_files = defaultdict(list)
        for slug, files in outputs.items():
            by_files[tuple(sorted(files))].append(slug)
        lines.append(f"City outputs changed ({len(outputs)} cities):")
        for files, slugs in sorted(by_files.items(), key=lambda kv: -len(kv[1])):
            who = (", ".join(sorted(slugs)) if len(slugs) <= MAX_NAMED
                   else f"{len(slugs)} cities")
            lines.append(f"  - {', '.join(files)}: {who}")
    for label, _ in GROUPS:
        if grouped[label]:
            lines.append(f"{label}: {', '.join(sorted(grouped[label]))}")
    return lines


def selftest():
    cases = [
        ("nothing downstream", ["README.md", "scripts/x.py"], set(), set(), 0),
        ("a city added", ["app/cities.py"], {"A"}, {"A", "B"}, 2),
        ("outputs grouped by city", ["outputs/rome/heatmap.html",
                                     "outputs/rome/stations.csv",
                                     "outputs/oslo/heatmap.html"], set(), set(), 3),
        ("licence rows", ["docs/data_sources/france.md"], set(), set(), 1),
        ("taxonomy", ["pipeline/taxonomies/naics.py"], set(), set(), 1),
    ]
    ok = 0
    for name, paths, old, new, want in cases:
        got = len(summarize(paths, old, new))
        status = "ok" if got == want else "FAIL"
        ok += got == want
        print(f"{status:4} {name}: {got} line(s), wanted {want}")
    src = 'CITIES = [{"name": "Paris", "page": "p"}, {"name": "Rome"}]\nX = 1\n'
    names_ok = city_names(src) == {"Paris", "Rome"}
    print(f"{'ok' if names_ok else 'FAIL':4} registry read by ast")
    ok += names_ok
    total = len(cases) + 1
    print(f"{ok} of {total} cases behaved as intended.")
    return 0 if ok == total else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("old", nargs="?")
    ap.add_argument("new", nargs="?", default="HEAD")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.old:
        ap.error("give the old ref (the master the push started from)")
    paths = [p for p in git("diff", "--name-only", f"{args.old}..{args.new}").splitlines() if p]
    lines = summarize(paths, city_names(show(args.old, "app/cities.py")),
                      city_names(show(args.new, "app/cities.py")))
    if not lines:
        print("nothing downstream")
        return 0
    new_sha = git("rev-parse", "--short", args.new).strip()
    old_sha = git("rev-parse", "--short", args.old).strip()
    print(f"Master moved {old_sha} -> {new_sha}. Changes your work builds from:")
    print("\n".join(lines))
    print("Merge master before regenerating anything. The landing's reasoning is "
          "in DECISIONS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
