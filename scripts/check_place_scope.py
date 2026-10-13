"""Place search: every searched city's index covers the municipalities its
map covers and nothing wider, and says so in a form the map can draw.

    python scripts/check_place_scope.py              # exit 1 on any problem
    python scripts/check_place_scope.py --selftest

The scope rule (owner, 2026-10-12; pipeline/place_index.py, "THE SEARCHED
AREA"): an index covers the boundary the map's businesses are cut to and, on
a regional map, every municipality a drawn station sits in. Check H of
check_place_search.py is the floor (every station has an indexed place
nearby); this is the ceiling. Reads committed files only, never a cache:

  A. Every summary (outputs/<slug>/place_search.json) lists its "area": the
     municipalities, each with an OSM id, a name and the number of the map's
     stations inside it. A summary with no "area" was built before the rule:
     run the fetch and the index step again.
  B. No municipality is there without a reason: one with no station inside
     needs an entry in config.PLACE_AREA_KEPT, which the build copies into
     the summary as "kept" (the owner's word for a wider area, or the
     boundary the businesses are cut to on a map whose stations all sit
     elsewhere). A count of null means the build could not read the
     stations: said out loud, counted, not failed.
  C. The index carries the same municipalities' names and at least one
     outline ring of four points or more, every point inside the valid
     latitude and longitude ranges.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check_city(summary_path, root=ROOT):
    """(problems, notes) for one city's committed summary and index."""
    slug = summary_path.parent.name
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    area = summary.get("area")
    if not area:
        return [f"{slug}: A. the summary lists no area: run "
                f"pipeline/place_index_fetch.py {slug} and the index step again"], []
    problems, notes = [], []
    for m in area:
        if not m.get("osm") or not m.get("name"):
            problems.append(f"{slug}: A. a municipality with no OSM id or no name: {m}")
        elif m.get("stations") is None:
            notes.append(f"{slug}: {m['name']}: stations not counted at the build")
        elif m["stations"] == 0 and not m.get("kept"):
            problems.append(f"{slug}: B. {m['name']} ({m['osm']}) holds none of the map's stations and has "
                            f"no entry in config.PLACE_AREA_KEPT: take it out of PLACE_AREA, or record "
                            f"the owner's word for it there")
    index_path = root / summary.get("index", "")
    if not index_path.is_file():
        return problems + [f"{slug}: C. the index {summary.get('index')!r} is not there"], notes
    served = json.loads(index_path.read_text(encoding="utf-8")).get("area") or {}
    if served.get("names") != [m.get("name") for m in area]:
        problems.append(f"{slug}: C. the index names {served.get('names')}, the summary "
                        f"{[m.get('name') for m in area]}")
    rings = served.get("outline") or []
    if not rings:
        problems.append(f"{slug}: C. the index carries no outline")
    for ring in rings:
        if len(ring) < 8 or len(ring) % 2:
            problems.append(f"{slug}: C. an outline ring of {len(ring)} numbers is no ring")
        elif any(not -90 <= ring[i] <= 90 or not -180 <= ring[i + 1] <= 180 for i in range(0, len(ring), 2)):
            problems.append(f"{slug}: C. an outline point outside the latitude and longitude ranges")
    return problems, notes


def main(root=ROOT, out=print):
    summaries = sorted((root / "outputs").glob("*/place_search.json"))
    if not summaries:
        out("NOT CHECKED: no outputs/<slug>/place_search.json found")
        return 1
    problems, notes = [], []
    for path in summaries:
        p, n = check_city(path, root)
        problems += p
        notes += n
    for line in notes:
        out(f"  note  {line}")
    for line in problems:
        out(f"  FAIL  {line}")
    if problems:
        out(f"\n{len(problems)} problem(s) in {len(summaries)} searched cities.")
        return 1
    out(f"OK - {len(summaries)} searched cities, each index covering only municipalities with a "
        f"station or a recorded reason" + (f"; {len(notes)} not counted" if notes else "") + ".")
    return 0


def selftest():
    ring = [47.0, -122.0, 47.1, -122.0, 47.1, -122.1, 47.0, -122.0]
    good_area = [{"osm": "relation/1", "name": "Alpha", "stations": 3}]
    cases = [
        ("a city with a station in its one municipality passes", good_area,
         {"names": ["Alpha"], "outline": [ring]}, 0, "OK"),
        ("a summary with no area is refused", None, {"names": ["Alpha"], "outline": [ring]}, 1, "A."),
        ("a municipality with no station and no reason is refused",
         good_area + [{"osm": "relation/2", "name": "Beta", "stations": 0}],
         {"names": ["Alpha", "Beta"], "outline": [ring]}, 1, "B. Beta"),
        ("the same municipality with a recorded reason passes",
         good_area + [{"osm": "relation/2", "name": "Beta", "stations": 0, "kept": "owner, 2026-10-12"}],
         {"names": ["Alpha", "Beta"], "outline": [ring]}, 0, "OK"),
        ("stations not counted is said out loud and passes",
         [{"osm": "relation/1", "name": "Alpha", "stations": None}],
         {"names": ["Alpha"], "outline": [ring]}, 0, "not counted"),
        ("an index naming other municipalities is refused", good_area,
         {"names": ["Gamma"], "outline": [ring]}, 1, "C. the index names"),
        ("an index with no outline is refused", good_area, {"names": ["Alpha"], "outline": []}, 1,
         "no outline"),
        ("a ring of three points is refused", good_area, {"names": ["Alpha"], "outline": [ring[:6]]}, 1,
         "is no ring"),
        ("a point outside the ranges is refused", good_area,
         {"names": ["Alpha"], "outline": [[147.0, -122.0] + ring[2:]]}, 1, "outside the latitude"),
        ("a municipality with no name is refused", [{"osm": "relation/1", "name": "", "stations": 3}],
         {"names": [""], "outline": [ring]}, 1, "no OSM id or no name"),
    ]
    passed = 0
    for label, area, served, want_rc, want_text in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "outputs" / "x").mkdir(parents=True)
            (root / "app" / "static" / "places").mkdir(parents=True)
            summary = {"index": "app/static/places/x.json"}
            if area is not None:
                summary["area"] = area
            (root / "outputs" / "x" / "place_search.json").write_bytes(json.dumps(summary).encode("utf-8"))
            (root / "app" / "static" / "places" / "x.json").write_bytes(
                json.dumps({"area": served, "rows": []}).encode("utf-8"))
            lines = []
            rc = main(root, lines.append)
        ok = rc == want_rc and want_text in "\n".join(lines)
        passed += ok
        print(f"  {'ok ' if ok else 'BAD'} {label}")
    with tempfile.TemporaryDirectory() as tmp:
        lines = []
        rc = main(Path(tmp), lines.append)
        ok = rc == 1 and "NOT CHECKED" in lines[0]
        passed += ok
        print(f"  {'ok ' if ok else 'BAD'} a tree with no searched city is not a pass")
    total = len(cases) + 1
    print(f"{passed} of {total} cases behaved as intended.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
