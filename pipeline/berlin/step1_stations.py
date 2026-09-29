"""Berlin step 1: the U-Bahn and S-Bahn stations inside the Land of Berlin.

    python pipeline/berlin/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. Copied from Oslo's shape
(one GTFS, several modes, stations collapsed by name with a spread check),
with Berlin's own:

  * **Lines are matched on (route_type, agency_id, route_short_name)**, never
    on route_id: VBB versions several route_ids per line, and each line's
    rail-replacement buses carry its short name under type 700.
  * **Names are normalised before collapsing**: "S+U Alexanderplatz Bhf
    (Berlin)" and "U Alexanderplatz (Berlin)" are one station, "Alexanderplatz".
    Every collapsed name's spread is printed, and a name wider than
    config.COLLAPSE_MAX_SPREAD_M stops the step.
  * **The scope is the Land**: the register is IHK Berlin's and stops at the
    border, so stations in Brandenburg are recorded as excluded, not drawn.
"""
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.berlin import config  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/berlin/fetch_sources.py")
    return path


def display_name(stop_name):
    name = stop_name.strip()
    for p in config.STATION_PREFIXES:
        if name.startswith(p):
            name = name[len(p):]
            break
    changed = True
    while changed:
        changed = False
        for s in config.STATION_SUFFIXES:
            if name.endswith(s):
                name, changed = name[: -len(s)].strip(), True
    return name


def line_key(name):
    return (name[0], int("".join(c for c in name[1:] if c.isdigit()) or 0), name)


def main():
    need(config.GTFS_ZIP, "the GTFS feed")
    need(config.CITY_BOUNDARY_GEOJSON, "the Land boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(config.GTFS_ZIP)
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    mode_of_route = {}
    for m, spec in config.MODES.items():
        sel = routes[(routes["route_type"] == spec["route_type"])
                     & (routes["agency_id"] == spec["agency_id"])]
        names = sorted(sel["route_short_name"].unique(), key=line_key)
        print(f"  {spec['label']:<24} {len(sel):>3} route_ids, {len(names):>2} lines: "
              f"{' '.join(names)}{'   <- drawn' if m in config.DRAWN_MODES else ''}")
        for rid in sel["route_id"]:
            mode_of_route[rid] = m
    rail = routes[routes["route_id"].isin(mode_of_route)].copy()
    rail["mode"] = rail["route_id"].map(mode_of_route)
    drawn = rail[rail["mode"].isin(config.DRAWN_MODES)]
    feed_lines = set(drawn["route_short_name"])
    if feed_lines != set(config.LINE_NAMES):
        sys.exit(f"the feed's drawn lines changed.\n"
                 f"  feed only  : {sorted(feed_lines - set(config.LINE_NAMES))}\n"
                 f"  config only: {sorted(set(config.LINE_NAMES) - feed_lines)}\n"
                 f"A line added or withdrawn is a scope decision, not a config edit.")
    line_of = dict(zip(drawn["route_id"], drawn["route_short_name"]))
    mode_of_line = dict(zip(drawn["route_short_name"], drawn["mode"]))

    trips = pd.read_csv(z.open("trips.txt"), dtype=str, usecols=["route_id", "trip_id"])
    trips = trips[trips["route_id"].isin(line_of)]
    head = pd.read_csv(z.open("stop_times.txt"), dtype=str, nrows=1)
    st_cols = ["trip_id", "stop_id"] + [c for c in ("pickup_type", "drop_off_type")
                                         if c in head.columns]
    wanted = set(trips["trip_id"])
    parts = []
    for chunk in pd.read_csv(z.open("stop_times.txt"), dtype=str, usecols=st_cols,
                             chunksize=2_000_000):
        parts.append(chunk[chunk["trip_id"].isin(wanted)])
    st = pd.concat(parts, ignore_index=True)
    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")

    boardable = station_gates.boardable_stop_ids(st)
    non_revenue = 0
    if boardable is not None:
        before = st["stop_id"].nunique()
        st = st[st["stop_id"].isin(boardable)]
        non_revenue = before - st["stop_id"].nunique()

    q = stops.loc[sorted(set(st["stop_id"]) & set(stops.index))].copy()
    q["latitude"] = q["stop_lat"].astype(float)
    q["longitude"] = q["stop_lon"].astype(float)
    q["station"] = q["stop_name"].map(display_name)
    variants = q.groupby("station")["stop_name"].agg(lambda s: sorted(set(s)))
    print(f"\n  {q['stop_name'].nunique()} stop names -> {len(variants)} stations; "
          f"names merged from more than one form, first 12:")
    for nm, forms in variants[variants.map(len) > 1].head(12).items():
        print(f"    {nm:<30} <- {' | '.join(forms)}")

    link = st.merge(q.reset_index()[["stop_id", "station"]], on="stop_id").merge(trips, on="trip_id")
    link["line"] = link["route_id"].map(line_of)
    lines_by = link.groupby("station")["line"].agg(
        lambda s: "/".join(sorted(set(s), key=line_key)))

    g = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q["longitude"], q["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("station")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print("\n  widest collapsed names:")
    for nm, d in spread.sort_values(ascending=False).head(8).items():
        print(f"    {nm:<30} {d:>5.0f} m")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"these names are more than {config.COLLAPSE_MAX_SPREAD_M} m across and "
                 f"would be averaged into one point: {too_far.round().to_dict()}")

    by = q.groupby("station").agg(latitude=("latitude", "mean"),
                                  longitude=("longitude", "mean"))
    by["lines"] = lines_by
    by = by.dropna(subset=["lines"])

    # Closed for works: must be UNSERVED, and must still be in stops.txt so the
    # excluded list can place them.
    reopened = sorted(set(config.CLOSED_FOR_WORKS) & set(by.index))
    if reopened:
        sys.exit(f"the feed serves {reopened} again - they were closed for works. "
                 f"Take them out of config.CLOSED_FOR_WORKS and re-run.")
    allstops = stops.assign(station=stops["stop_name"].map(display_name))
    closed = (allstops[allstops["station"].isin(config.CLOSED_FOR_WORKS)]
              .assign(latitude=lambda d: d["stop_lat"].astype(float),
                      longitude=lambda d: d["stop_lon"].astype(float))
              .groupby("station")[["latitude", "longitude"]].mean())
    missing = sorted(set(config.CLOSED_FOR_WORKS) - set(closed.index))
    if missing:
        sys.exit(f"closed-for-works station(s) {missing} are not in stops.txt by that name")
    print(f"\n  {len(closed)} station(s) closed for works, not served by the feed: "
          f"{', '.join(closed.index)}")

    actual, expected = {}, {}
    for m, key in (("U", "U-Bahn (network)"), ("S", "S-Bahn (network)")):
        if m in config.DRAWN_MODES:
            actual[key] = int(by["lines"].map(
                lambda v: any(mode_of_line.get(x) == m for x in v.split("/"))).sum())
            n_closed = len(closed) if m == "U" else 0
            expected[key] = config.OPERATOR_STATION_COUNTS[key] - n_closed
    print()
    station_gates.verify_stations(
        city="Berlin", platforms=q, stations=by.reset_index(),
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        spacing_min=config.SPACING_MIN_M, expected_per_line=expected,
        actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    land = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()
    gb = gpd.GeoDataFrame(by, geometry=gpd.points_from_xy(by["longitude"], by["latitude"]),
                          crs=config.CRS_GEOGRAPHIC)
    within = gb.within(land)
    inside, outside = gb[within].copy(), gb[~within].copy()
    print(f"\n  Land of Berlin: {len(gb)} stations -> {len(inside)} inside, "
          f"{len(outside)} in Brandenburg")

    print("\n  per line, inside the Land (of all its stations):")
    for ln in sorted(config.LINE_NAMES, key=line_key):
        n_in = int(sum(ln in v.split("/") for v in inside["lines"]))
        n_all = int(sum(ln in v.split("/") for v in gb["lines"]))
        print(f"    {ln:<5} {n_in:>3} of {n_all:>3}")
        if n_in == 0:
            sys.exit(f"{ln} has no station inside the Land - a scope decision")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-Land spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  max {d.max():,.0f}")

    out = (outside.reset_index()[["station", "lines", "latitude", "longitude"]]
           .assign(reason="in Brandenburg, outside the Land of Berlin (the register "
                          "stops at the Land border)"))
    shut = (closed.reset_index()
            .assign(lines="U6", reason=lambda d: d["station"].map(config.CLOSED_FOR_WORKS)))
    out = pd.concat([out, shut[out.columns]], ignore_index=True).sort_values(["reason", "station"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")

    keep = (inside.reset_index()[["station", "lines", "latitude", "longitude"]]
            .sort_values("station"))
    keep.insert(0, "stop_id", keep["station"])
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
