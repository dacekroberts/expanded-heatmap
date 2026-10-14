"""Place search: every searched city's index covers the municipalities its
map covers and nothing wider, and says so in a form the map can draw.

    python scripts/check_place_scope.py              # exit 1 on any problem
    python scripts/check_place_scope.py --selftest
    python scripts/check_place_scope.py --reach      # D's figure for every city

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
  D. No index row lies more than REACH_MAX_KM past the map's stations: the
     great-circle distance from each row (the index's and its intersections
     file's) to the nearest station the committed map draws
     (outputs/<slug>/heatmap.html). A city whose map does reach that far
     records why in config.PLACE_SCOPE_REACH_REASON, a dated string, and
     passes with the reason printed; a reason on a city under the limit
     fails, so the reasons only shrink. A map with no station marker is a
     problem, never a pass.

WHY D (owner, 2026-10-13). B counts stations per NAMED AREA and asks nothing
about the area's size. Mendoza's config named relation 153540, the province,
where the department (2204157) was meant: one area, all 7 stations inside
it, so A, B and C passed an index of 12,470 rows, 5,693 of them more than
25 km out and the farthest 522.2 km from the nearest station (search-rollout
at b2e671b2, the commit before f04f9939; 7.9 km once corrected). Any area
that is too large but still holds a station passes B the same way.
"""
import ast
import json
import math
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# D's limit, in kilometres (owner, 2026-10-13). Measured on 2026-10-13 over
# the searched cities of five branches (data/_search_rollout/scope_reach.md):
# 237 cities, median 10.4 km, 75th percentile 19.8, 90th 30.9; 202 cities at
# or under the limit (the 19 of this branch among them, Sao Paulo the
# farthest at 24.2 and Hong Kong at 24.0) and 35 over it, from Dallas at 25.3
# to Naha at 267.1. Most of the 35 are a municipality's own far corner (a
# mountain, an island); which of them carry a reason is the owner's call.
# Re-measure with --reach before moving it, and after any change to how an
# index's area is chosen.
REACH_MAX_KM = 25.0
# The stroke colour of a station marker, pipeline/theme.py's LIGHT["station"]:
# what the search script itself reads the map's stations by (map_common.py,
# ownItems). If the theme's value changes, D reads no station and every city
# fails until this follows it.
STATION_COLOR = "#1a5490"
_MARKER = re.compile(r'L\.circleMarker\(\s*\[(-?[0-9.]+),\s*(-?[0-9.]+)\],\s*\{[^{}]*"color":\s*"'
                     + STATION_COLOR + '"')
_DATED = re.compile(r"\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b")
EARTH_KM = 6371.0088
# The grid both searches below use, in degrees, and the rings of cells a
# search looks through before it measures every station. Only speed depends
# on either: the 19 cities took 30 s at 0.05 and every ring, 2026-10-13.
_CELL = 0.01
_RINGS = 4


def map_stations(html):
    """[(lat, lon)] of the station markers in a committed map's text."""
    return sorted({(float(a), float(b)) for a, b in _MARKER.findall(html)})


def haversine_km(a, b):
    """Great-circle kilometres between two (lat, lon) points in degrees.
    Never a difference of degrees: at 60 N a degree of longitude is half a
    degree of latitude."""
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    h = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[1] - a[1]) / 2) ** 2)
    return 2 * EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def _cell(p):
    return math.floor(p[0] / _CELL), math.floor(p[1] / _CELL)


def _nearest_km(p, grid, stations):
    """Kilometres from p to its nearest station: the cells around p first
    (`grid`, {cell: [station]}), every station when those do not settle it."""
    i0, j0 = _cell(p)
    best = math.inf
    for k in range(_RINGS + 1):
        for i in range(i0 - k, i0 + k + 1):
            edge = abs(i - i0) == k
            for j in (range(j0 - k, j0 + k + 1) if edge else (j0 - k, j0 + k)):
                for s in grid.get((i, j), ()):
                    best = min(best, haversine_km(p, s))
        # Every station not yet seen is at least k cells away: k cells of
        # latitude, or k cells of longitude at the ring's highest latitude.
        top = min(89.9, abs(p[0]) + (k + 1) * _CELL)
        if best <= k * _CELL * math.radians(1) * EARTH_KM * math.cos(math.radians(top)):
            return best
    return min(haversine_km(p, s) for s in stations)


def farthest_reach(points, stations):
    """(km, point) for the point of `points` farthest from its nearest
    station, exact; (0.0, None) with no points. Points and stations are
    (lat, lon), and a point may carry more after its two numbers.

    Two steps keep it light on an index of 300,000 rows: the points' grid
    cells are measured first, by their centres, and only the points of cells
    that could hold the farthest are measured one by one (a point is within
    half a cell's diagonal of its cell's centre, and the distance to the
    nearest station changes no faster than the point moves)."""
    if not points or not stations:
        return 0.0, None
    grid = {}
    for s in stations:
        grid.setdefault(_cell(s), []).append(s)
    cells = {}
    for p in points:
        cells.setdefault(_cell(p), []).append(p)
    half = haversine_km((0.0, 0.0), (_CELL / 2, _CELL / 2)) * 1.01
    centre = {c: _nearest_km(((c[0] + 0.5) * _CELL, (c[1] + 0.5) * _CELL), grid, stations) for c in cells}
    floor = max(centre.values()) - 2 * half
    best, where = -1.0, None
    for c, pts in cells.items():
        if centre[c] < floor:
            continue
        for p in pts:
            d = _nearest_km(p, grid, stations)
            if d > best:
                best, where = d, p
    return best, where


def reach_reason(slug, root=ROOT):
    """config.PLACE_SCOPE_REACH_REASON of a city, read from the file's text
    (no import: a config pulls in nothing here), or None. A value that is
    not a plain string comes back as it is written, for D to refuse."""
    path = root / "pipeline" / slug / "config.py"
    if not path.is_file():
        return None
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "PLACE_SCOPE_REACH_REASON" for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return ast.unparse(node.value)
    return None


def index_points(index, index_path):
    """[(lat, lon, name)] for an index's rows and its intersections file's."""
    points = [(r[1], r[2], r[3]) for r in index.get("rows", [])]
    cross = index_path.parent / "crossings" / index_path.name
    if cross.is_file():
        points += [(r[0], r[1], "an intersection")
                   for r in json.loads(cross.read_text(encoding="utf-8")).get("rows", [])]
    return points


def measure_reach(slug, index, index_path, root=ROOT):
    """(km, point, number of stations) for one city, from committed files;
    km is None when the map or its station markers are not there."""
    html = root / "outputs" / slug / "heatmap.html"
    stations = map_stations(html.read_text(encoding="utf-8")) if html.is_file() else []
    if not stations:
        return None, None, 0
    km, where = farthest_reach(index_points(index, index_path), stations)
    return km, where, len(stations)


def check_reach(slug, index, index_path, root=ROOT):
    """D for one city: (problems, notes)."""
    km, where, _ = measure_reach(slug, index, index_path, root)
    if km is None:
        return [f"{slug}: D. no station marker read from outputs/{slug}/heatmap.html, so the "
                f"index's reach is not measured: render the map, or see STATION_COLOR"], []
    reason = reach_reason(slug, root)
    if reason is not None and (not isinstance(reason, str) or not _DATED.search(reason)):
        return [f"{slug}: D. config.PLACE_SCOPE_REACH_REASON is not a dated string "
                f"(a date as 2026-10-13, then why): {reason!r}"], []
    if km <= REACH_MAX_KM:
        if reason is not None:
            return [f"{slug}: D. config.PLACE_SCOPE_REACH_REASON is recorded and the index reaches "
                    f"{km:.1f} km, within the {REACH_MAX_KM:g} km limit: remove it"], []
        return [], []
    far = f"{where[2]!r} at {where[0]}, {where[1]}"
    if reason is not None:
        return [], [f"{slug}: reaches {km:.1f} km past its stations ({far}), kept: {reason}"]
    return [f"{slug}: D. the index reaches {km:.1f} km past the map's nearest station ({far}), over "
            f"the {REACH_MAX_KM:g} km limit: config.PLACE_AREA names an area wider than the map "
            f"(a province for a city?). Correct the area and rebuild, or record the owner's reason "
            f"in config.PLACE_SCOPE_REACH_REASON"], []


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
    index = json.loads(index_path.read_text(encoding="utf-8"))
    served = index.get("area") or {}
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
    p, n = check_reach(slug, index, index_path, root)
    return problems + p, notes + n


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
    kept = sum(1 for line in notes if ", kept: " in line)
    counted = len(notes) - kept
    out(f"OK - {len(summaries)} searched cities, each index covering only municipalities with a "
        f"station or a recorded reason, and none reaching more than {REACH_MAX_KM:g} km past its "
        f"stations" + (f" without a recorded reason ({kept} with one)" if kept else "")
        + (f"; {counted} not counted" if counted else "") + ".")
    return 0


def reach_table(root=ROOT, out=print):
    """D's figure for every searched city, farthest first. A report: exit 0."""
    rows = []
    for path in sorted((root / "outputs").glob("*/place_search.json")):
        slug = path.parent.name
        index_path = root / json.loads(path.read_text(encoding="utf-8")).get("index", "")
        if not index_path.is_file():
            continue
        km, where, n = measure_reach(slug, json.loads(index_path.read_text(encoding="utf-8")), index_path, root)
        rows.append((-1.0 if km is None else km, slug, n, where))
    for km, slug, n, where in sorted(rows, reverse=True):
        out(f"  {slug:<24} " + ("no station marker read" if km < 0 else
                                f"{km:6.1f} km  {n:4d} stations  {where[2] if where else ''}"))
    return 0


def _marker(lat, lon, color=STATION_COLOR):
    return ("var circle_marker_x = L.circleMarker(\n [%s, %s],\n"
            ' {"bubblingMouseEvents": true, "color": "%s", "radius": 5}\n).addTo(g);\n' % (lat, lon, color))


def selftest():
    ring = [47.0, -122.0, 47.1, -122.0, 47.1, -122.1, 47.0, -122.0]
    good_area = [{"osm": "relation/1", "name": "Alpha", "stations": 3}]
    good = {"names": ["Alpha"], "outline": [ring]}
    here = [[2, 47.05, -122.05, "Park", "", 0]]
    cases = [
        ("a city with a station in its one municipality passes", good_area, good, 0, "OK"),
        ("a summary with no area is refused", None, good, 1, "A."),
        ("a municipality with no station and no reason is refused",
         good_area + [{"osm": "relation/2", "name": "Beta", "stations": 0}],
         {"names": ["Alpha", "Beta"], "outline": [ring]}, 1, "B. Beta"),
        ("the same municipality with a recorded reason passes",
         good_area + [{"osm": "relation/2", "name": "Beta", "stations": 0, "kept": "owner, 2026-10-12"}],
         {"names": ["Alpha", "Beta"], "outline": [ring]}, 0, "OK"),
        ("stations not counted is said out loud and passes",
         [{"osm": "relation/1", "name": "Alpha", "stations": None}], good, 0, "not counted"),
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
    # D: (label, station markers, index rows, intersection rows, the config's
    # text or None, exit code, text). One degree of latitude is 111.2 km.
    north = [(60.0, 10.0)]
    reason = 'PLACE_SCOPE_REACH_REASON = "2026-10-13 (owner): the airport line ends 31 km out"\n'
    # Mendoza as it stood on search-rollout before f04f9939: the map's seven
    # station markers, and the index's farthest row and one of its nearest.
    # Its summary's area was one entry holding all seven, which A to C pass.
    mendoza = [(-32.896801, -68.851854), (-32.890363, -68.850145), (-32.882818, -68.848189),
               (-32.87936, -68.847238), (-32.8764, -68.846472), (-32.870048, -68.844776),
               (-32.866425, -68.843815)]
    reach_cases = [
        ("Mendoza built on its province is refused (the fault of 2026-10-13)", mendoza,
         [[4, -37.5608, -68.1807, "Ruta Provincial 20", "", 0], [4, -32.8636, -68.9293, "Acceso Cerro Arco", "", 0]],
         [], None, 1, "D. the index reaches 522.2 km"),
        ("Mendoza built on its department passes", mendoza,
         [[4, -32.8636, -68.9293, "Acceso Cerro Arco", "", 0]], [], None, 0, "OK"),
        ("a row 20 km from the one station passes", [(47.05, -122.05)], [[2, 47.23, -122.05, "Far", "", 0]],
         [], None, 0, "OK"),
        ("a row 30 km from the one station is refused", [(47.05, -122.05)], [[2, 47.32, -122.05, "Far", "", 0]],
         [], None, 1, "D. the index reaches 30.0 km"),
        ("a row 30 km from one station and beside another passes", [(47.05, -122.05), (47.32, -122.06)],
         [[2, 47.32, -122.05, "Far", "", 0]], [], None, 0, "OK"),
        ("an intersection 30 km out is refused as a row is", [(47.05, -122.05)], here,
         [[47.32, -122.05, 0, 0]], None, 1, "'an intersection'"),
        ("the reach is in kilometres, not degrees: 0.4 of longitude at 60 N is 22 km and passes", north,
         [[2, 60.0, 10.4, "East", "", 0]], [], None, 0, "OK"),
        ("and 0.4 of latitude there is 44 km and is refused", north,
         [[2, 60.4, 10.0, "North", "", 0]], [], None, 1, "D. the index reaches 44.5 km"),
        ("a city over the limit with a dated reason passes, the reason printed", [(47.05, -122.05)],
         [[2, 47.32, -122.05, "Far", "", 0]], [], reason, 0, "kept: 2026-10-13 (owner): the airport line"),
        ("a reason with no date is refused", [(47.05, -122.05)], [[2, 47.32, -122.05, "Far", "", 0]],
         [], 'PLACE_SCOPE_REACH_REASON = "the airport line"\n', 1, "not a dated string"),
        ("a reason that is no string is refused", [(47.05, -122.05)], [[2, 47.32, -122.05, "Far", "", 0]],
         [], "PLACE_SCOPE_REACH_REASON = True\n", 1, "not a dated string"),
        ("a reason on a city within the limit is refused", [(47.05, -122.05)], here, [], reason, 1,
         "remove it"),
        ("a map with no station marker is refused, not passed", [], here, [], None, 1,
         "D. no station marker"),
        ("a marker of another colour is no station", "other", here, [], None, 1, "D. no station marker"),
        ("no map at all is refused", None, here, [], None, 1, "D. no station marker"),
    ]
    passed = 0
    runs = [(label, area, served, [(47.05, -122.05)], here, [], None, want_rc, want_text)
            for label, area, served, want_rc, want_text in cases]
    runs += [(label, good_area, good, stations, rows, cross, config, want_rc, want_text)
             for label, stations, rows, cross, config, want_rc, want_text in reach_cases]
    for label, area, served, stations, rows, cross, config, want_rc, want_text in runs:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "outputs" / "x").mkdir(parents=True)
            (root / "app" / "static" / "places" / "crossings").mkdir(parents=True)
            summary = {"index": "app/static/places/x.json"}
            if area is not None:
                summary["area"] = area
            (root / "outputs" / "x" / "place_search.json").write_bytes(json.dumps(summary).encode("utf-8"))
            (root / "app" / "static" / "places" / "x.json").write_bytes(
                json.dumps({"area": served, "rows": rows}).encode("utf-8"))
            (root / "app" / "static" / "places" / "crossings" / "x.json").write_bytes(
                json.dumps({"rows": cross}).encode("utf-8"))
            if stations is not None:
                html = (_marker(47.05, -122.05, "#000000") if stations == "other"
                        else "".join(_marker(lat, lon) for lat, lon in stations))
                (root / "outputs" / "x" / "heatmap.html").write_bytes(html.encode("utf-8"))
            if config is not None:
                (root / "pipeline" / "x").mkdir(parents=True)
                (root / "pipeline" / "x" / "config.py").write_bytes(config.encode("utf-8"))
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
    # The two-step search against every point measured against every station.
    import random
    rng = random.Random(7)
    exact = True
    for lat0 in (0.0, 35.0, -41.0, 64.0):
        stations = [(lat0 + rng.uniform(-0.2, 0.2), 20 + rng.uniform(-0.3, 0.3)) for _ in range(40)]
        points = [(lat0 + rng.uniform(-1.5, 1.5), 20 + rng.uniform(-2.5, 2.5)) for _ in range(400)]
        want = max(min(haversine_km(p, s) for s in stations) for p in points)
        exact = exact and abs(farthest_reach(points, stations)[0] - want) < 1e-9
    passed += exact
    print(f"  {'ok ' if exact else 'BAD'} the grid search finds the farthest point a full search finds")
    total = len(runs) + 2
    print(f"{passed} of {total} cases behaved as intended.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv
             else reach_table() if "--reach" in sys.argv else main())
