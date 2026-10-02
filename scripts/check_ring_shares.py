"""Each city's in-ring share - the storefronts inside its station rings, out of all
it maps - read from the committed maps, never hand-kept (owner, 2026-09-28).

    python scripts/check_ring_shares.py            # check (the pre-push hook)
    python scripts/check_ring_shares.py --write    # regenerate app/ring_shares.json

WHY. The "Why the maps differ" page (app/pages/Why_the_Maps_Differ.py) shows
each city's share in its summary table and quotes the site-wide range in its
prose. Both are open-ended - the next city can move the range - so they come
from a generated file, the way app/macro_facts.json carries the macro map's
storefront counts.

WHAT IS COUNTED. Every map carries two heat layers: "Commercial Density (Within
Station Proximity)" and "Commercial Density (All <city> Businesses)"
(`pipeline/map_common.py`, `render_heatmap`). The share is the first layer's
points over the second's - the same measure docs/map_inconsistencies.md table D
and theme 7 use. The layers are found by their names in the layer control, not
by their order in the file.

WHY IT IS CHEAP ENOUGH FOR THE HOOK. The committed maps are about 200 MB.
`--write` records each map's git blob id alongside its counts; the check
compares blob ids from `git ls-files -s` (no file read) and re-parses only a map
whose blob changed. A re-render that moves no point (Folium's ids, line endings)
passes; one that moves the counts fails and names `--write`.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from cities import CITIES  # noqa: E402
from station_scope import slug  # noqa: E402

OUT = ROOT / "app" / "ring_shares.json"
IN_RING = "Commercial Density (Within Station Proximity)"
ALL_PREFIX = "Commercial Density (All "

LAYER = re.compile(r'var (heat_map_\w+) = L\.heatLayer\(\s*JSON\.parse\(("(?:[^"\\]|\\.)*")\)')
OVERLAY = re.compile(r'"(Commercial Density \([^"]*\))"\s*:\s*(heat_map_\w+)')


def map_path(entry):
    return f"outputs/{slug(entry['page'])}/heatmap.html"


def blob_ids():
    """Committed (index) blob id of every map, keyed by its repo path."""
    out = subprocess.run(["git", "ls-files", "-s", "--", "outputs/*/heatmap.html"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    ids = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        ids[path] = meta.split()[1]
    return ids


def count_points(path):
    """(in_ring, all) heat points in one map, found by layer name."""
    text = (ROOT / path).read_text(encoding="utf-8")
    sizes = {name: len(json.loads(json.loads(data)))
             for name, data in LAYER.findall(text)}
    names = dict(OVERLAY.findall(text))
    del text
    in_ring = [sizes[v] for k, v in names.items() if k == IN_RING and v in sizes]
    whole = [sizes[v] for k, v in names.items() if k.startswith(ALL_PREFIX) and v in sizes]
    if len(in_ring) != 1 or len(whole) != 1:
        raise ValueError(f"{path}: expected one in-ring and one whole-city heat layer, "
                         f"found {len(in_ring)} and {len(whole)}")
    return in_ring[0], whole[0]


def write():
    ids = blob_ids()
    facts = {}
    for entry in CITIES:
        path = map_path(entry)
        in_ring, whole = count_points(path)
        facts[slug(entry["page"])] = {"in_ring": in_ring, "all": whole,
                                      "map_blob": ids.get(path)}
    OUT.write_text(json.dumps(facts, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(facts)} cities")
    return 0


def check():
    try:
        facts = json.loads(OUT.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"PROBLEM: {OUT.relative_to(ROOT)} is missing - run with --write")
        return 1
    ids = blob_ids()
    problems, reparsed = [], 0
    slugs = {slug(e["page"]) for e in CITIES}
    for entry in CITIES:
        key, path = slug(entry["page"]), map_path(entry)
        rec = facts.get(key)
        if rec is None:
            problems.append(f"{entry['name']}: no entry in {OUT.name}")
            continue
        if path not in ids:
            problems.append(f"{entry['name']}: {path} is not committed")
            continue
        if rec.get("map_blob") == ids[path]:
            continue
        reparsed += 1
        try:
            counts = count_points(path)
        except (OSError, ValueError) as exc:
            problems.append(str(exc))
            continue
        if counts != (rec["in_ring"], rec["all"]):
            problems.append(f"{entry['name']}: the map has {counts[0]:,} of {counts[1]:,} "
                            f"heat points in its rings; {OUT.name} says "
                            f"{rec['in_ring']:,} of {rec['all']:,}")
    for key in sorted(set(facts) - slugs):
        problems.append(f"{key}: in {OUT.name} but not a city in app/cities.py")
    if problems:
        print(f"PROBLEMS {len(problems)}")
        for p in problems:
            print("  " + p)
        print(f"\nRun python scripts/check_ring_shares.py --write and commit {OUT.name}.")
        return 1
    print(f"OK - {len(slugs)} cities' ring shares match their committed maps"
          + (f" ({reparsed} re-read: re-rendered, same points)" if reparsed else ""))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    return write() if args.write else check()


if __name__ == "__main__":
    sys.exit(main())
