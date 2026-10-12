"""Place search: the watch file of stations OpenStreetMap draws as not yet
open (docs/place_search_unopened_stations.json) says what the indexes say.

    python scripts/check_place_unopened.py              # exit 1 on any problem
    python scripts/check_place_unopened.py --selftest

The index step skips a station OSM tags as under construction, proposed or
disused (pipeline/place_index.py, station_skipped_not_open), so a search does
not find it. The owner keeps those stations in an internal watch file, never
on a page (2026-10-11). This check holds the file to three things, reading
committed and cached files only (it never fetches):

  A. Every row is a station its city's last index build skipped: the city's
     committed summary (outputs/<slug>/place_search.json, "stations_not_open")
     lists the row's OSM id with the row's tag. A row the build no longer
     skips has opened in OSM: remove the row.
  B. No skipped station is unlisted: every id in a summary's
     "stations_not_open" has a row. A new unopened station cannot go unseen.
  C. The row agrees with the city's newest cached place data: the object is
     there and still carries the row's tag, and the row's
     "open_namesake_in_index" is what the committed index says. A city whose
     cache is not on disk (a fresh checkout: data/ is not committed) is
     skipped for C and counted; A and B need no cache.

A row's "line" may be null only with a "line_reason"; a line carries its
"line_source".
"""
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
WATCH = ROOT / "docs" / "place_search_unopened_stations.json"
ROW_KEYS = {"city", "line", "line_source", "line_reason", "name", "osm", "tag",
            "open_namesake_in_index", "cache", "noted"}
LINE_SOURCES = ("relation", "tag", "source")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def row_problems(row):
    """Problems of one row's own shape."""
    out = []
    extra = set(row) - ROW_KEYS
    if extra:
        out.append(f"unknown field(s) {sorted(extra)}")
    for k in ("city", "name", "osm", "tag", "noted"):
        if not row.get(k):
            out.append(f"no {k}")
    if row.get("line"):
        if not str(row.get("line_source") or "").startswith(LINE_SOURCES):
            out.append(f"a line needs a line_source starting with one of {LINE_SOURCES}")
    elif not row.get("line_reason"):
        out.append("line is null with no line_reason")
    return out


def compare(city, rows, skipped, cached=None, stations=None):
    """Problems for one city (its slug). `rows`: its watch-file rows. `skipped`: the
    summary's stations_not_open. `cached`: {osm id: tags} from its newest
    cache, or None when the cache is not on disk. `stations`: the station
    names in its committed index, or None."""
    out = []
    by_id = {r["osm"]: r for r in rows}
    skip = {s["osm"]: s for s in skipped}
    for osm, r in by_id.items():
        label = f"{city} {osm} ({r['name']})"
        for p in row_problems(r):
            out.append(f"{label}: {p}")
        if osm not in skip:
            out.append(f"A: {label}: the last index build did not skip it as not open "
                       f"(it has opened in OSM, or the id is wrong): remove the row")
        elif skip[osm]["tag"] != r["tag"]:
            out.append(f"A: {label}: the build skipped it as {skip[osm]['tag']}, the row says {r['tag']}")
        if cached is not None:
            tags = cached.get(osm)
            key, _, value = r["tag"].partition("=")
            if tags is None:
                out.append(f"C: {label}: not in the city's newest cache")
            elif tags.get(key) != value:
                out.append(f"C: {label}: the cache has {key}={tags.get(key)}, the row says {r['tag']}")
        if stations is not None and bool(r.get("open_namesake_in_index")) != (r["name"] in stations):
            out.append(f"C: {label}: open_namesake_in_index is {r.get('open_namesake_in_index')}, "
                       f"the committed index says {r['name'] in stations}")
    for osm, s in skip.items():
        if osm not in by_id:
            out.append(f"B: {city} {osm} ({s['name']}, {s['tag']}): skipped as not "
                       f"open by the index build and not in the watch file: add a row")
    return out


def main():
    from pipeline import place_index
    watch = json.loads(WATCH.read_text(encoding="utf-8"))["rows"]
    cities = sorted(p.parent.name for p in (ROOT / "pipeline").glob("*/step2b_place_index.py"))
    problems, no_cache = [], []
    for row in watch:
        if row.get("city") not in cities:
            problems.append(f"{row.get('city')} {row.get('osm')}: no searched city of that name")
    for city in cities:
        rows = [r for r in watch if r.get("city") == city]
        spath = place_index.summary_path(city)
        summary = json.loads(spath.read_text(encoding="utf-8")) if spath.exists() else {}
        if "stations_not_open" not in summary:
            problems.append(f"{city}: outputs/{city}/place_search.json has no stations_not_open "
                            f"(re-run its index step)")
            continue
        skipped = summary["stations_not_open"]
        if not rows and not skipped:
            continue
        cached = stations = None
        config = importlib.import_module(f"pipeline.{city}.config")
        paths = (config.PLACE_OSM_JSON, config.PLACE_OSM_EXTRA_JSON)
        if all(p.exists() for p in paths):
            want = {r["osm"] for r in rows}
            cached = {}
            for p in paths:
                for e in json.loads(p.read_text(encoding="utf-8"))["elements"]:
                    k = f"{e['type']}/{e['id']}"
                    if k in want:
                        cached[k] = e.get("tags") or {}
        else:
            no_cache.append(city)
        ipath = place_index.index_path(city)
        if ipath.exists():
            ix = json.loads(ipath.read_text(encoding="utf-8"))
            stations = {r[3] for r in ix["rows"] if ix["kinds"][r[0]] == "station"}
        problems += compare(city, rows, skipped, cached, stations)
    for p in problems:
        print(f"  FAIL {p}")
    note = (f"; {len(no_cache)} city cache(s) not on disk, their rows checked against the committed "
            f"summaries only ({', '.join(no_cache)})" if no_cache else "")
    if problems:
        print(f"\n{len(problems)} problem(s) in docs/place_search_unopened_stations.json.")
        return 1
    print(f"OK - {len(watch)} unopened station(s) in {len({r['city'] for r in watch})} cities, each one "
          f"skipped by its city's last index build and none unlisted{note}.")
    return 0


def selftest():
    row = {"city": "x", "line": "L9", "line_source": "relation 1", "name": "Camp Nou", "osm": "node/1",
           "tag": "railway=construction", "open_namesake_in_index": False, "cache": "2026-10-08",
           "noted": "2026-10-11"}
    skip = [{"osm": "node/1", "name": "Camp Nou", "tag": "railway=construction"}]
    tags = {"node/1": {"railway": "construction"}}

    def kinds(found):
        return sorted({p.split(":")[0] if p[1] == ":" else "shape" for p in found})

    cases = [
        ("a listed, skipped, unopened station passes", compare("x", [row], skip, tags, set()), []),
        ("no cache on disk still passes on the summary", compare("x", [row], skip, None, None), []),
        ("a station the build no longer skips", kinds(compare("x", [row], [], tags, set())), ["A"]),
        ("a skipped station with no row", kinds(compare("x", [row], skip + [
            {"osm": "node/2", "name": "Mandri", "tag": "railway=proposed"}], tags, set())), ["B"]),
        ("the cache says it has opened", kinds(compare("x", [row], skip, {"node/1": {"railway": "station"}}, set())), ["C"]),
        ("the object left the cache", kinds(compare("x", [row], skip, {}, set())), ["C"]),
        ("an open namesake the row does not record", kinds(compare("x", [row], skip, tags, {"Camp Nou"})), ["C"]),
        ("a null line needs a reason", kinds(compare("x", [dict(row, line=None, line_source=None)], skip, tags, set())),
         ["shape"]),
        ("a null line with a reason passes", compare("x",
            [dict(row, line=None, line_source=None, line_reason="no relation, no tag")], skip, tags, set()), []),
        ("a line needs its source", kinds(compare("x", [dict(row, line_source=None)], skip, tags, set())), ["shape"]),
    ]
    ok = 0
    for name, got, want in cases:
        good = got == want
        ok += good
        print(f"  {'ok ' if good else 'BAD'} {name}" + ("" if good else f": got {got!r}"))
    print(f"{ok} of {len(cases)} cases behaved as intended.")
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
