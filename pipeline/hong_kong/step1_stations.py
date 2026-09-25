"""Hong Kong step 1: MTR's eight urban lines and the Light Rail, from OpenStreetMap.

Stations come from ROUTE-RELATION MEMBERSHIP (osm-rail), never a node tag
filter: the stop nodes of the relations whose network and ref are MTR's,
collapsed by English name. Gate 3 is MTR's own station lists, per line.

Each drawn line is written to processed/rail_lines.json as ONE relation for
step 3: the line's longest relation plus only the track another relation adds
(a branch). The Light Rail's twelve routes become one line, as the owner asked.

Every MTR station is kept; the Light Rail's stops are thinned with the
sub-transit-line filters (terminals, interchanges and MTR stations kept, the
rest one per half mile along each route).

Reads the cache and NEVER fetches.

    python pipeline/hong_kong/step1_stations.py
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.hong_kong import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
BILINGUAL = re.compile(r"^[^A-Za-z]*[㐀-鿿][^A-Za-z]*\s([A-Za-z][A-Za-z0-9 '’().,&-]*)$")
FROM_BILINGUAL = set()


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/hong_kong/fetch_sources.py files")
    return path


def haversine_miles(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    h = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2)
    return 2 * 3958.7613 * math.asin(math.sqrt(h))


def load_osm():
    els = json.loads(need(config.RAIL_OSM_JSON, "OSM rail relations").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    if not rels:
        sys.exit("the rail file holds no relations - an empty result is not an empty city")
    return rels, nodes


def stop_seq(rel, nodes):
    """The relation's stop nodes in order: [(name, lat, lon)]."""
    out = []
    for m in rel.get("members", []):
        if m["type"] != "node" or not m.get("role", "").startswith("stop"):
            continue
        n = nodes.get(m["ref"])
        if n is None:
            continue
        t = n.get("tags", {})
        name = (t.get("name:en") or "").strip()
        if not name:
            # Hong Kong's OSM convention writes both languages in `name`
            # ("荃灣 Tsuen Wan"): the English is the Latin tail after the CJK.
            m2 = BILINGUAL.match(t.get("name") or "")
            if not m2:
                sys.exit(f"stop node {m['ref']} on {rel['tags'].get('name')} has no name:en and "
                         f"no bilingual name ({t.get('name')!r}) - name it rather than guess")
            name = m2.group(1).strip()
            FROM_BILINGUAL.add(name)
        name = config.NAME_ALIASES.get(name, name)
        out.append((name, n["lat"], n["lon"]))
    return out


def ways_of(rel):
    return [(m["ref"], [(p["lat"], p["lon"]) for p in m["geometry"]])
            for m in rel.get("members", []) if m["type"] == "way" and m.get("geometry")]


def line_geometry(rels, nodes):
    """The longest relation, plus only the ways other relations add away from it."""
    rels = sorted(rels, key=lambda r: sum(len(g) for _, g in ways_of(r)), reverse=True)
    chosen, seen, covered = [], set(), set()
    drawn_m = None
    added_branch = 0
    for i, r in enumerate(rels):
        names = {s[0] for s in stop_seq(r, nodes)}
        if i and not (names - covered):
            continue
        for wid, g in ways_of(r):
            if wid in seen or len(g) < 2:
                continue
            if drawn_m is not None:
                mid = g[len(g) // 2]
                if drawn_m.distance(Point(TO_M.transform(mid[1], mid[0]))) <= config.BRANCH_MIN_M:
                    continue
                added_branch += 1
            chosen.append(g)
            seen.add(wid)
        covered |= names
        drawn_m = unary_union([LineString([TO_M.transform(lo, la) for la, lo in g]) for g in chosen])
    return chosen, added_branch


def boundary_polygon():
    els = json.loads(need(config.BOUNDARY_OSM_JSON, "SAR boundary").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"
            and e.get("tags", {}).get("ISO3166-1") == config.BOUNDARY_ISO]
    if len(rels) != 1:
        sys.exit(f"expected exactly one relation tagged ISO3166-1={config.BOUNDARY_ISO}, got {len(rels)}")
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rels[0]["members"]
             if m["type"] == "way" and m.get("role") == "outer" and m.get("geometry")]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    area = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    print(f"  boundary: relation {rels[0]['id']} ({rels[0]['tags'].get('name:en')}), {area:,.0f} km2")
    if not lo <= area <= hi:
        sys.exit(f"boundary area {area:,.0f} km2 outside {lo}-{hi} - the wrong relation, or its "
                 f"sea area; re-read it before changing the gate")
    return poly


def mtr_lists():
    per = {}
    with need(config.MTR_STATIONS_CSV, "MTR stations").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            per.setdefault(r["Line Code"], set()).add(r["English Name"].strip())
    with need(config.MTR_LIGHT_RAIL_CSV, "Light Rail stops").open(encoding="utf-8-sig") as f:
        per["LR"] = {r["English Name"].strip() for r in csv.DictReader(f)}
    return per


def thin(seqs, keep_always, coords):
    """The sub-transit-line filters on each Light Rail route's stop order."""
    kept, cut = set(), []
    for seq in seqs:
        if not seq:
            continue
        mark = [n in keep_always for n in seq]
        mark[0] = mark[-1] = True
        since, last = 0.0, seq[0]
        for i in range(1, len(seq)):
            since += haversine_miles(coords[seq[i - 1]], coords[seq[i]])
            if mark[i]:
                since, last = 0.0, seq[i]
            elif since >= config.THIN_SPACING_MILES:
                mark[i], since, last = True, 0.0, seq[i]
            else:
                cut.append({"station": seq[i], "nearest_kept": last,
                            "miles_since_kept": round(since, 3)})
        kept |= {n for n, m in zip(seq, mark) if m}
    return kept, [c for c in cut if c["station"] not in kept]


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    rels, nodes = load_osm()

    groups = {k: [] for k in config.LINE_ORDER}
    not_drawn = {k: [] for k in config.NOT_DRAWN}
    for r in rels:
        t = r.get("tags", {})
        if t.get("network") == config.MTR_NETWORK:
            ref = t.get("ref")
            if ref in groups:
                groups[ref].append(r)
            elif ref in not_drawn:
                not_drawn[ref].append(r)
            else:
                sys.exit(f"an MTR relation with an unplaced ref {ref!r}: {t.get('name')}")
        elif t.get("network") == config.LIGHT_RAIL_NETWORK:
            groups["LR"].append(r)
    print("Relations matched (network + ref on the RELATION):")
    for k in config.LINE_ORDER:
        print(f"  {k:<4} {config.LINE_NAMES[k]:<20} {len(groups[k]):>3} relations")
        if not groups[k]:
            sys.exit(f"no relation for {config.LINE_NAMES[k]}")
    for k, v in not_drawn.items():
        print(f"  {k:<4} {config.NOT_DRAWN[k]:<20} {len(v):>3} relations - NOT drawn (owner)")

    # --- stations -------------------------------------------------------------
    plat, line_names, lr_seqs = [], {k: set() for k in config.LINE_ORDER}, []
    event_only = {}
    for k in config.LINE_ORDER:
        for r in groups[k]:
            seq = [s for s in stop_seq(r, nodes)]
            for name, la, lo in seq:
                if name in config.EVENT_ONLY:
                    event_only.setdefault(name, (k, la, lo))
            seq = [s for s in seq if s[0] not in config.EVENT_ONLY]
            if k == "LR":
                lr_seqs.append([s[0] for s in seq])
            for name, la, lo in seq:
                plat.append({"station": name, "latitude": la, "longitude": lo, "line": k})
                line_names[k].add(name)
    missing_event = set(config.EVENT_ONLY) - set(event_only)
    if missing_event:
        sys.exit(f"EVENT_ONLY names no longer in the relations: {missing_event} - re-read them")
    platforms = pd.DataFrame(plat).drop_duplicates()
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms.longitude, platforms.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("station")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop nodes under {spread.size} English names "
          f"({len(FROM_BILINGUAL)} read from a bilingual `name` for want of name:en); widest spreads:")
    for nm in spread.sort_values(ascending=False).head(5).index:
        print(f"    {nm:<32} {spread[nm]:>5.0f} m")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M:.0f} m would be averaged into one "
                 f"point: {too_far.round().to_dict()}")
    stations = (platforms.groupby("station", as_index=False)
                .agg(latitude=("latitude", "mean"), longitude=("longitude", "mean")))
    lines_of = {n: [k for k in config.LINE_ORDER if n in line_names[k]] for n in stations.station}
    stations["lines"] = [" ".join(lines_of[n]) for n in stations.station]

    # --- gate 3: MTR's own lists ---------------------------------------------
    lists = mtr_lists()
    expected = {config.LINE_NAMES[k]: len(lists[k]) for k in config.LINE_ORDER}
    actual = {config.LINE_NAMES[k]: len(line_names[k]) for k in config.LINE_ORDER}
    print("\n  names against MTR's lists (a spelling difference shows as one each side):")
    for k in config.LINE_ORDER:
        a, b = lists[k] - line_names[k], line_names[k] - lists[k]
        if a or b:
            print(f"    {config.LINE_NAMES[k]:<20} MTR only {sorted(a)}  OSM only {sorted(b)}")
    station_gates.verify_stations(
        city="Hong Kong", platforms=platforms, stations=stations,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=expected, actual_per_line=actual)
    emit("stop_nodes", len(platforms))
    emit("station_names", len(stations))

    # --- the SAR --------------------------------------------------------------
    poly = boundary_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(stations.longitude, stations.latitude), crs=config.CRS_GEOGRAPHIC)
    outside = stations[~pts.within(poly).values]
    if len(outside):
        sys.exit(f"MTR stations outside the SAR polygon: {list(outside.station)}")

    # --- thinning the Light Rail ----------------------------------------------
    coords = {r.station: (r.latitude, r.longitude) for r in stations.itertuples()}
    mtr_names = set().union(*(line_names[k] for k in config.LINE_ORDER if k != "LR"))
    lr_only = line_names["LR"] - mtr_names
    kept_lr, cuts = thin(lr_seqs, mtr_names, coords)
    keep = mtr_names | kept_lr
    print(f"\n  Light Rail: {len(line_names['LR'])} stops ({len(line_names['LR'] & mtr_names)} are MTR "
          f"stations) -> {len(kept_lr & lr_only)} of {len(lr_only)} Light-Rail-only stops kept, "
          f"one per {config.THIN_SPACING_MILES} mi")
    emit("stations_kept", len(keep))
    emit("light_rail_thinned", len(lr_only - kept_lr))

    # Stations of lines NOT drawn, and the race-day station, are printed and
    # disclosed in prose (the page, excluded_categories.md) but not written to
    # excluded_stations.csv - that file records stations of DRAWN lines cut by a
    # boundary or the spacing filter, as in every other city.
    drawn_names = set(stations.station)
    off_map = {n: f"{config.EVENT_ONLY[n]}" for n in event_only}
    for k, rs in not_drawn.items():
        for r in rs:
            for name, la, lo in stop_seq(r, nodes):
                if name not in drawn_names:
                    off_map.setdefault(name, f"{config.NOT_DRAWN[k]} not drawn (owner's call)")
    print(f"\n  off the map, disclosed in prose: " + "; ".join(f"{n} ({why})" for n, why in sorted(off_map.items())))
    emit("stations_off_map", len(off_map))
    excluded = []
    seen = set()
    for c in sorted(cuts, key=lambda c: c["station"]):
        if c["station"] in seen:
            continue
        seen.add(c["station"])
        la, lo = coords[c["station"]]
        excluded.append({"station": c["station"], "lines": "LR",
                         # "spacing filter" is the phrase app/station_scope.py reads.
                         "reason": f"spacing filter on the Light Rail: {c['miles_since_kept']} mi after "
                                   f"{c['nearest_kept']}, under {config.THIN_SPACING_MILES} mi",
                         "latitude": la, "longitude": lo})
    out = pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} thinned -> {config.EXCLUDED_STATIONS_CSV.name}")

    kept = stations[stations.station.isin(keep)].sort_values("station").reset_index(drop=True)
    kept.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(kept)} stations")

    # --- the drawn lines -------------------------------------------------------
    elements = []
    print("\n  line geometry (longest relation + branch track the others add):")
    for k in config.LINE_ORDER:
        ways, branch = line_geometry(groups[k], nodes)
        colours = {r["tags"].get("colour") for r in groups[k]} - {None}
        colour = config.LIGHT_RAIL_COLOUR if k == "LR" else (colours.pop() if len(colours) == 1 else None)
        if colour is None:
            sys.exit(f"{config.LINE_NAMES[k]}: relations disagree on colour {colours}")
        elements.append({"type": "relation", "id": len(elements) + 1,
                         "tags": {"ref": k, "name": config.LINE_NAMES[k], "colour": colour},
                         "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                                     for g in ways]})
        print(f"    {config.LINE_NAMES[k]:<20} {colour}  {len(ways):>4} ways ({branch} branch)")
    config.RAIL_LINES_JSON.write_text(json.dumps({"elements": elements}), encoding="utf-8")
    emit("lines_drawn", len(elements))


if __name__ == "__main__":
    main()
