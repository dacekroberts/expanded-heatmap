"""Oslo step 1: Ruter's T-bane and tram stations inside the kommune.

    python pipeline/oslo/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT, copied from Rennes':

  * **Extended route types only** (`401` T-bane, `902` tram) - a basic-type
    reader sees no rail at all in this feed.
  * **Two modes share five station names** (Majorstuen, Jernbanetorget,
    Nationaltheatret, Carl Berners plass, Storo): the T-bane station and the
    tram stop are different stop places metres apart. They collapse to one
    station by name, and the spread of every collapsed name is printed, so a
    merge of two genuinely different places cannot pass silently.
  * **Gate 3 is network-level** - no per-line figure exists outside the feed.
  * **Excluded stations are named with their kommune**, from Kartverket's own
    boundary of each neighbour that holds one.
"""
import json
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates
from pipeline.oslo import config

# A collapsed name whose stops are further apart than this is two places, not
# one station with two platforms - and step 1 stops rather than average them.
COLLAPSE_MAX_SPREAD_M = 400


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/oslo/fetch_sources.py")
    return path


def main():
    need(config.GTFS_ZIP, "the GTFS feed")
    need(config.CITY_BOUNDARY_GEOJSON, "the kommune boundary")
    need(config.NEIGHBOURS_GEOJSON, "the neighbouring kommunes")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(config.GTFS_ZIP)
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    print("routes by mode (route_type):")
    for rt, n in routes["route_type"].value_counts().items():
        mark = "  <- drawn" if rt in config.ROUTE_TYPES_RAIL else ""
        print(f"    {rt:>5}: {n:>5}{mark}")

    rail = routes[routes["route_type"].isin(config.ROUTE_TYPES_RAIL)].copy()
    if sorted(rail["route_id"]) != sorted(config.ROUTE_IDS):
        sys.exit(f"the feed's T-bane/tram route_ids changed.\n"
                 f"  feed  : {sorted(rail['route_id'])}\n"
                 f"  config: {sorted(config.ROUTE_IDS)}\n"
                 f"A line added or withdrawn is a scope decision, not a config edit.")
    short_of = dict(zip(rail["route_id"], rail["route_short_name"]))
    mode_of = dict(zip(rail["route_short_name"], rail["route_type"]))
    missing = sorted(set(short_of.values()) - set(config.LINE_NAMES))
    if missing:
        sys.exit(f"no public name for line(s) {missing}")

    trips = pd.read_csv(z.open("trips.txt"), dtype=str, usecols=["route_id", "trip_id"])
    trips = trips[trips["route_id"].isin(config.ROUTE_IDS)]
    st_cols = ["trip_id", "stop_id"]
    head = pd.read_csv(z.open("stop_times.txt"), dtype=str, nrows=1)
    st_cols += [c for c in ("pickup_type", "drop_off_type") if c in head.columns]
    st = pd.read_csv(z.open("stop_times.txt"), dtype=str, usecols=st_cols)
    st = st[st["trip_id"].isin(set(trips["trip_id"]))]
    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")

    boardable = station_gates.boardable_stop_ids(st)
    non_revenue = 0
    if boardable is not None:
        before = st["stop_id"].nunique()
        st = st[st["stop_id"].isin(boardable)]
        non_revenue = before - st["stop_id"].nunique()

    q = stops.loc[[s for s in sorted(set(st["stop_id"])) if s in stops.index]].copy()
    # One station under two names, merged only where config names the pair.
    aliased = q["stop_name"].isin(config.STATION_NAME_ALIASES)
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    if aliased.any():
        print(f"\n  {int(aliased.sum())} stop(s) renamed by config.STATION_NAME_ALIASES")
    q["latitude"] = q["stop_lat"].astype(float)
    q["longitude"] = q["stop_lon"].astype(float)
    parent = q.get("parent_station", pd.Series(dtype=str))
    q["station_id"] = parent.where(parent.notna() & (parent != ""),
                                   pd.Series(q.index, index=q.index))

    link = (st.merge(q.reset_index()[["stop_id", "station_id", "stop_name"]], on="stop_id")
              .merge(trips, on="trip_id"))
    link["line"] = link["route_id"].map(short_of)
    lines_by_name = link.groupby("stop_name")["line"].agg(
        lambda s: "/".join(sorted(set(s), key=lambda x: (len(x), x))))

    # One station per NAME: the platforms of every stop place carrying it.
    by_name = q.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                         longitude=("longitude", "mean"),
                                         stop_id=("station_id", "first"),
                                         places=("station_id", "nunique"))
    # The spread check, in metres, before any average is trusted.
    g = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q["longitude"], q["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    multi = by_name[by_name["places"] > 1].index
    print(f"\n  {len(multi)} name(s) span more than one stop place; widest spreads:")
    for nm in spread.loc[multi].sort_values(ascending=False).head(8).index:
        print(f"    {nm:<26} {int(by_name.loc[nm, 'places'])} places, {spread[nm]:>5.0f} m apart")
    too_far = spread[spread > COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"these names are more than {COLLAPSE_MAX_SPREAD_M} m across and would be "
                 f"averaged into one point: {too_far.round().to_dict()}")
    st_rows = by_name.reset_index().set_index("stop_id")
    st_rows["lines"] = st_rows["stop_name"].map(lines_by_name)

    # GATE 3, network-level: distinct T-bane stations in the feed against the
    # published 101.
    metro_lines = {s for s, m in mode_of.items() if m == "401"}
    metro_names = {nm for nm, ls in lines_by_name.items()
                   if set(ls.split("/")) & metro_lines}
    actual = {"T-bane (network)": len(metro_names)}

    print()
    station_gates.verify_stations(
        city="Oslo", platforms=q, stations=st_rows, crs_projected=config.CRS_PROJECTED,
        non_revenue=non_revenue, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    kommune = shape(json.loads(config.CITY_BOUNDARY_GEOJSON.read_bytes())["geometry"])
    g = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                              st_rows["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    within = g.within(kommune)
    inside, outside = g[within].copy(), g[~within].copy()
    print(f"\n  kommune {config.KOMMUNE_NUMBER}: {len(g)} stations -> {len(inside)} inside, "
          f"{len(outside)} outside")

    all_lines = sorted(config.LINE_NAMES, key=lambda x: (len(x), x))
    inside_per_line = {ln: int(sum(1 for v in inside["lines"] if ln in v.split("/")))
                       for ln in all_lines}
    total_per_line = {ln: int(sum(1 for v in g["lines"] if ln in v.split("/")))
                      for ln in all_lines}
    print("\n  per line, inside the kommune:")
    for ln in all_lines:
        exp = config.EXPECTED_INSIDE_PER_LINE.get(ln)
        flag = "" if exp is None or exp == inside_per_line[ln] else f"   <- EXPECTED {exp}"
        print(f"    {config.LINE_NAMES[ln]:<10} {inside_per_line[ln]:>3} of "
              f"{total_per_line[ln]:>3}{flag}")
    if 0 in inside_per_line.values():
        sys.exit("kommune-only scope drops a whole line; the scope decision needs re-taking")
    if inside_per_line != config.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the kommune boundary keeps a different set than recorded.\n"
                 f"  measured: {inside_per_line}\n"
                 f"  config  : {config.EXPECTED_INSIDE_PER_LINE}\n"
                 f"Scope is a decision, not a side effect - see config and DECISIONS.md.")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-kommune spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")

    neighbours = gpd.read_file(config.NEIGHBOURS_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    excluded = []
    for stop_id, r in outside.iterrows():
        hit = neighbours[neighbours.contains(r.geometry)]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} is outside Oslo and in {len(hit)} recorded "
                     f"neighbour(s) - add its kommune to config.NEIGHBOUR_KOMMUNER")
        excluded.append({"stop_id": stop_id, "station": r["stop_name"], "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['kommunenavn']} "
                                   f"({hit.iloc[0]['kommunenummer']}), outside kommune "
                                   f"{config.KOMMUNE_NUMBER}",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    out = pd.DataFrame(excluded, columns=["stop_id", "station", "lines", "reason",
                                          "latitude", "longitude"])
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for _, r in out.sort_values(["reason", "station"]).iterrows():
        print(f"    {r['station']:<16} {r['lines']:<6} {r['reason']}")

    keep = (inside.reset_index()
            .rename(columns={"index": "stop_id", "stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
