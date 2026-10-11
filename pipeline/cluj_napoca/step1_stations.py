"""Cluj-Napoca step 1: CTP's tram stops, the two directions paired into
stations.

    python pipeline/cluj_napoca/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: the stop members of the six relations
of lines 100, 101 and 102 (102L's depot runs are in config.NOT_DRAWN), three
of them named from CTP's own stop maps (config.NAME_MEMBERS).

STATIONS ARE DIRECTION PAIRS, not names (the brief's call 11). CTP names each
direction's stop separately (UNIMET Nord and UNIMET Sud; Opera Maghiară Est
one way, Parcul Central the other), so a collapse on the name would draw 38
points a median 67 m apart. Line 102 runs the whole axis, and every stop of
100 and 101 is one of its stops, so its two relations give each stop its
direction; each stop is paired with the nearest stop of the other direction
within config.PAIR_MAX_M, nearest pairs first. A pair takes the name its two
stops share, or both names where they share none. No stop is thinned.
"""
import math
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.cluj_napoca import config  # noqa: E402

FETCH = "pipeline/cluj_napoca/fetch_sources.py"
# The direction words CTP adds to one stop's name: a pair whose names differ
# only by these shows the shared part.
DIRECTION_WORDS = re.compile(r"(\s+(Nord|Sud|Est|Vest|Tram|Noi|Vechi))+$")
# The two relations of line 102, which runs the whole axis: toward Disp.
# Bucium, and toward UNIMET.
AXIS = {"west": 5673735, "east": 5673736}


def base_name(name):
    return DIRECTION_WORDS.sub("", name).strip()


def station_name(a, b):
    """The name of a pair: the part both names share, else both, the
    westbound stop's first (the direction CTP's line 102 is listed in)."""
    if b is None or a == b:
        return base_name(a) if b is None else a
    return base_name(a) if base_name(a) == base_name(b) else f"{a} / {b}"


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    if not config.CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.CITY_BOUNDARY_GEOJSON}\nRun: python {FETCH}")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS, operator=config.OPERATOR,
                           not_drawn=config.NOT_DRAWN, name_members=config.NAME_MEMBERS)

    # Gate 3, per relation: the stop members OSM holds against CTP's own stop
    # maps (config.OPERATOR_COUNTS_SOURCE gives the one known difference).
    rels = {e["id"]: e for e in els if e["type"] == "relation"}
    print("\n  stop members per relation against CTP's stop maps:")
    for rid, want in config.STOP_MEMBERS_PER_RELATION.items():
        got = sum(1 for m in rels[rid]["members"] if m["type"] == "node" and m.get("role", "").startswith("stop"))
        print(f"    {rid} line {rels[rid]['tags'].get('ref')}: {got} (expected {want})")
        if got != want:
            sys.exit(f"gate 3: relation {rid} has {got} stop members, not {want} - re-read OSM against CTP's maps")
    print(f"    source: {config.OPERATOR_COUNTS_SOURCE}")

    def stop_nodes(rid):
        return [m["ref"] for m in rels[rid]["members"]
                if m["type"] == "node" and m.get("role", "").startswith("stop")]

    west, east = set(stop_nodes(AXIS["west"])), set(stop_nodes(AXIS["east"]))
    stray = set(q["node"]) - west - east
    if stray:
        sys.exit(f"stop node(s) {sorted(stray)} are on line 100 or 101 but not on 102: the pairing reads "
                 f"direction from 102's relations - re-read the network")

    platforms = q.drop_duplicates("node").set_index("node")
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"], platforms["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    xy = {n: (p.x, p.y) for n, p in g.geometry.items()}
    lines_of = q.groupby("node")["line"].agg(set).to_dict()

    both = west & east
    cross = sorted((math.dist(xy[a], xy[b]), a, b) for a in west - both for b in east - both)
    paired, pairs = set(), []
    for d, a, b in cross:
        if d > config.PAIR_MAX_M:
            break
        if a in paired or b in paired:
            continue
        paired |= {a, b}
        pairs.append((a, b, d))
    singles = sorted((west | east) - paired)
    print(f"\n  {len(west | east)} stop positions -> {len(pairs)} direction pairs "
          f"(furthest {max(d for _, _, d in pairs):.0f} m apart) and {len(singles)} single stops")

    rows = []
    order = list(config.LINE_REFS)
    for a, b, d in pairs:
        name = station_name(platforms.loc[a, "stop_name"], platforms.loc[b, "stop_name"])
        rows.append({"station": name, "x": (xy[a][0] + xy[b][0]) / 2, "y": (xy[a][1] + xy[b][1]) / 2,
                     "lines": lines_of[a] | lines_of[b], "pair_m": round(d),
                     "stops": f"{platforms.loc[a, 'stop_name']} | {platforms.loc[b, 'stop_name']}"})
    for n in singles:
        rows.append({"station": station_name(platforms.loc[n, "stop_name"], None), "x": xy[n][0], "y": xy[n][1],
                     "lines": lines_of[n], "pair_m": 0, "stops": platforms.loc[n, "stop_name"]})
    st = pd.DataFrame(rows)
    st["lines"] = st["lines"].map(lambda s: "/".join(sorted(s, key=order.index)))
    pts = gpd.GeoSeries(gpd.points_from_xy(st["x"], st["y"]), crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC)
    st["longitude"], st["latitude"] = pts.x, pts.y
    for r in st.sort_values("x").itertuples():
        print(f"    {r.station:42} {r.lines:12} {r.pair_m:>4} m   [{r.stops}]")
    if st["station"].duplicated().any():
        sys.exit(f"two stations share a name: {sorted(st.loc[st['station'].duplicated(), 'station'])}")
    if len(st) != config.STATIONS_EXPECTED:
        sys.exit(f"{len(st)} stations, not the brief's {config.STATIONS_EXPECTED} - re-read OSM")

    outside = st[~pts.within(city.union_all()).values]
    if len(outside):
        sys.exit(f"stations outside the municipality: {sorted(outside['station'])} - a scope question")
    print(f"\n  {len(st)} tram stations, all inside {config.CITY_LABEL}")

    # Gate 1 on the stations drawn, then the ring decision's own bounds.
    print()
    station_gates.verify_stations(
        city="Cluj-Napoca", platforms=q.drop_duplicates("node"),
        stations=st.rename(columns={"station": "stop_name"})[["stop_name", "latitude", "longitude", "lines"]],
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line={config.LINE_NAMES[k]: n for k, n in config.OPERATOR_STATION_COUNTS.items()},
        actual_per_line={config.LINE_NAMES[k]: int(st["lines"].str.split("/").apply(lambda ls: k in ls).sum())
                         for k in config.LINE_REFS})
    proj = gpd.GeoSeries(gpd.points_from_xy(st["x"], st["y"]))
    d = pd.Series([proj.drop(i).distance(p).min() for i, p in proj.items()])
    print(f"\n  spacing (nearest neighbour, m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m; the halved rings were chosen at 475 m - re-take the "
                 f"ring decision")

    # Every stop is in the city, so this is header-only; it stays written so a
    # stop that moves outside is recorded, not lost.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    keep = st[["station", "lines", "latitude", "longitude"]].sort_values("station")
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stop_positions_named_in_config", len(config.NAME_MEMBERS))
    emit("direction_pairs", len(pairs))
    emit("stations_in_scope", len(keep))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
