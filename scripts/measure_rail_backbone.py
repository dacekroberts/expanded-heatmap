"""Measure a suburban or diesel line against the DART / S-tog test - the two
parts a file can answer. Read-only; reads cached OSM, fetches nothing.

    python scripts/measure_rail_backbone.py --osm data/rio_de_janeiro/raw/osm_rail.json \\
        --relation 1234567 --municipios data/rio_de_janeiro/raw/osm_municipios.json \\
        --codes 3304557 --stations data/rio_de_janeiro/processed/stations.csv \\
        --crs EPSG:32723

THE TEST (docs/commuter_rail_list.md; the owner's calls on Dublin, Copenhagen,
Rome and São Paulo): commuter rail is drawn where, INSIDE THE SCOPE, it runs
like a metro - (1) station SPACING near metro spacing, (2) FREQUENCY near
metro frequency, (3) COVERAGE: it reaches districts no drawn line does. This
prints (1) and (3). Frequency is not in OSM or any file here - read it from the
operator or a cited secondary source, and quote it where the decision is
recorded. Precedents, all measured the same way:

    line                     median gap   frequency       no drawn station <800 m   verdict
    Dublin DART              ~1 km        -               -                          drawn
    Copenhagen S-tog         1,227 m      10 min          16 of 31                   drawn
    Rome Roma-Viterbo urb.   895 m        10-15 min       14 of 15                   drawn
    São Paulo CPTM Line 9    1,778 m      4.5-7 min       16 of 19                   drawn (frequency)
    Rome Metromare           2,171 m      15-20 min       11 of 14                   out
    São Paulo CPTM 7/8/10-12 2.1-3.4 km   -               -                          out

Gaps are STRAIGHT-LINE between consecutive stops, in route order, counting
only pairs where both stops are in scope. Stops are the relation's `stop*`
members, collapsed by name (both directions' positions), so a two-direction
relation counts each station once.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from pyproj import Transformer
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from pipeline.countries.brazil_boundary import scope_polygon  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--osm", required=True, help="cached Overpass JSON with the relation, `out geom; node(r); out tags center;`")
    ap.add_argument("--relation", type=int, required=True, help="one direction's route relation id")
    ap.add_argument("--municipios", required=True, help="cached admin_level-8 relations (brazil_boundary)")
    ap.add_argument("--codes", required=True, help="comma-separated IBGE codes forming the scope")
    ap.add_argument("--stations", help="the city's stations.csv - the DRAWN network, for coverage")
    ap.add_argument("--exclude-line", help="a line key in stations.csv's `lines` to leave out of "
                    "coverage - the line under test, once it is drawn (interchanges stay)")
    ap.add_argument("--crs", required=True, help="the city's projected CRS, e.g. EPSG:32723")
    a = ap.parse_args()

    els = json.loads(Path(a.osm).read_text(encoding="utf-8"))["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rel = next((e for e in els if e["type"] == "relation" and e["id"] == a.relation), None)
    if rel is None:
        sys.exit(f"relation {a.relation} is not in {a.osm}")
    scope = scope_polygon(Path(a.municipios), a.codes.split(","), (0, 1e9), a.crs, "scope")
    tr = Transformer.from_crs("EPSG:4326", a.crs, always_xy=True)

    stops, seen = [], set()
    for m in rel["members"]:
        if m["type"] != "node" or not m.get("role", "").startswith("stop"):
            continue
        n = nodes.get(m["ref"])
        name = (n or {}).get("tags", {}).get("name")
        if not n or not name:
            sys.exit(f"stop member {m['ref']} has no named node - fetch with `node(r); out tags center;`")
        if name in seen:
            continue
        seen.add(name)
        x, y = tr.transform(n["lon"], n["lat"])
        stops.append((name, scope.contains(Point(n["lon"], n["lat"])), x, y))

    drawn = []
    if a.stations:
        st = pd.read_csv(a.stations, dtype={"lines": str})
        if a.exclude_line:
            st = st[st["lines"].str.split().map(lambda ls: ls != [a.exclude_line])]
        drawn = [tr.transform(lo, la) for la, lo in zip(st["latitude"], st["longitude"])]

    print(f"{rel['tags'].get('name', a.relation)}  ({rel['tags'].get('route')}, "
          f"ref {rel['tags'].get('ref')})")
    gaps, prev = [], None
    for name, inside, x, y in stops:
        gap = ((x - prev[1]) ** 2 + (y - prev[2]) ** 2) ** 0.5 if prev else None
        if prev and inside and prev[0]:
            gaps.append(gap)
        near = min((((x - p) ** 2 + (y - q) ** 2) ** 0.5 for p, q in drawn), default=None)
        print(f"  {name:<40} {'in ' if inside else 'OUT'}  gap {'' if gap is None else round(gap):>6}"
              f"  nearest drawn station {'-' if near is None else round(near)}")
        prev = (inside, x, y)
    ins = [s for s in stops if s[1]]
    g = sorted(gaps)
    print(f"\n  stations in scope: {len(ins)} of {len(stops)}")
    if g:
        print(f"  (1) spacing in scope: median {round(g[len(g) // 2]):,} m, "
              f"min {round(g[0]):,}, max {round(g[-1]):,}")
    if drawn:
        def far(s, d):
            return min(((s[2] - p) ** 2 + (s[3] - q) ** 2) ** 0.5 for p, q in drawn) > d
        print(f"  (3) coverage: {sum(far(s, 400) for s in ins)} of {len(ins)} with no drawn "
              f"station within 400 m, {sum(far(s, 800) for s in ins)} within 800 m")
    print("  (2) frequency: read it from the operator, cite it, and record all three.")


if __name__ == "__main__":
    main()
