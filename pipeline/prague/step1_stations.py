"""Prague step 1: metro A, B and C stations, from PID's own GTFS.

    python pipeline/prague/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **Stations come from the feed's own `parent_station`**, so no name
    collapse is needed: every metro platform (`U...Z101P`) belongs to a parent
    (`U...S1`) with its own name and position.
  * **Flora is added although no trip serves it** - line A's station, closed
    for reconstruction since 1 February 2026 - located from stops.txt, owner's
    call. The build STOPS the day the feed serves Flora again, so the override
    cannot outlive the closure.
  * **OSM's route relations are the cross-check** (osm-rail's order: agency
    GTFS first), and they omit Flora too.
"""
import json
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.prague import config  # noqa: E402
from pipeline.prague.boundary import city_polygon  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/prague/fetch_sources.py")
    return path


def osm_cross_check():
    els = json.loads(config.OSM_RAIL_JSON.read_text(encoding="utf-8"))["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    per = {}
    for r in (e for e in els if e["type"] == "relation"):
        ref = r.get("tags", {}).get("ref")
        if ref not in config.LINE_NAMES:
            continue
        names = {nodes[m["ref"]].get("tags", {}).get("name") for m in r["members"]
                 if m["type"] == "node" and m.get("role", "").startswith("stop")
                 and m["ref"] in nodes}
        per.setdefault(ref, set()).update(n for n in names if n)
    return {ref: len(v) for ref, v in per.items()}


def main():
    need(config.GTFS_ZIP, "PID's GTFS")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(config.GTFS_ZIP)

    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    metro = routes[routes["route_type"] == config.ROUTE_TYPE_METRO]
    got = sorted(metro["route_short_name"])
    if got != sorted(config.LINE_NAMES):
        sys.exit(f"the feed's metro lines are {got}, not {sorted(config.LINE_NAMES)} - "
                 f"a line added or withdrawn is a scope decision")
    line_of = dict(zip(metro["route_id"], metro["route_short_name"]))
    print("  metro routes: " + ", ".join(
        f"{r['route_short_name']} {r['route_id']} #{r['route_color']}"
        for _, r in metro.iterrows()) + " (config lightens A; see LINE_COLOURS)")

    trips = pd.read_csv(z.open("trips.txt"), dtype=str, usecols=["route_id", "trip_id"])
    trips = trips[trips["route_id"].isin(line_of)]
    parts = []
    for ch in pd.read_csv(z.open("stop_times.txt"), dtype=str, chunksize=1_000_000,
                          usecols=["trip_id", "stop_id", "pickup_type", "drop_off_type"]):
        parts.append(ch[ch["trip_id"].isin(set(trips["trip_id"]))])
    st = pd.concat(parts, ignore_index=True)
    boardable = station_gates.boardable_stop_ids(st)
    before = st["stop_id"].nunique()
    st = st[st["stop_id"].isin(boardable)]
    non_revenue = before - st["stop_id"].nunique()

    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")
    link = st.merge(trips, on="trip_id")
    link["line"] = link["route_id"].map(line_of)
    link["station_id"] = link["stop_id"].map(stops["parent_station"])
    if link["station_id"].isna().any():
        sys.exit(f"metro platforms with no parent_station: "
                 f"{sorted(link.loc[link['station_id'].isna(), 'stop_id'].unique())[:10]}")
    lines = link.groupby("station_id")["line"].agg(lambda s: "/".join(sorted(set(s))))

    # FLORA: closed, so absent from every trip. Guard first, then add.
    if config.FLORA_PARENT in lines.index:
        sys.exit(f"{config.FLORA_NAME} is SERVED by the feed again - the closure is over. "
                 f"Remove the Flora override from config and this step; the station "
                 f"now comes from the trips like every other.")
    if stops.loc[config.FLORA_PARENT, "stop_name"] != config.FLORA_NAME:
        sys.exit(f"{config.FLORA_PARENT} is not {config.FLORA_NAME} in stops.txt")
    lines.loc[config.FLORA_PARENT] = config.FLORA_LINE
    print(f"  {config.FLORA_NAME} added from stops.txt ({config.FLORA_PARENT}): closed for "
          f"reconstruction, no trip serves it - owner's call, disclosed on the page")

    platforms = stops.loc[stops.index.isin(set(link["stop_id"])) |
                          (stops["parent_station"] == config.FLORA_PARENT)
                          & (stops["location_type"].fillna("0") == "0")].copy()
    platforms["latitude"] = platforms["stop_lat"].astype(float)
    platforms["longitude"] = platforms["stop_lon"].astype(float)
    st_rows = stops.loc[lines.index, ["stop_name", "stop_lat", "stop_lon"]].copy()
    st_rows["latitude"] = st_rows["stop_lat"].astype(float)
    st_rows["longitude"] = st_rows["stop_lon"].astype(float)
    st_rows["lines"] = lines
    if st_rows["stop_name"].duplicated().any():
        sys.exit(f"two parent stations share a name: "
                 f"{sorted(st_rows.loc[st_rows['stop_name'].duplicated(), 'stop_name'])}")

    per_line = {ln: int(sum(1 for v in st_rows["lines"] if ln in v.split("/")))
                for ln in config.LINE_NAMES}
    print(f"\n  {len(platforms)} platforms -> {len(st_rows)} stations; per line {per_line}")
    osm = osm_cross_check()
    print(f"  OSM cross-check (route-relation stop names): {osm} - OSM omits Flora too")
    print()
    station_gates.verify_stations(
        city="Prague", platforms=platforms, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        expected_per_line=config.OPERATOR_STATION_COUNTS or None,
        actual_per_line={config.LINE_NAMES[k]: v for k, v in per_line.items()}
        | {"Metro (network)": len(st_rows)})
    if config.OPERATOR_COUNTS_SOURCE:
        print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    poly = city_polygon()
    g = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                              st_rows["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    inside_mask = g.within(poly)
    inside, outside = g[inside_mask].copy(), g[~inside_mask].copy()
    inside_per_line = {ln: int(sum(1 for v in inside["lines"] if ln in v.split("/")))
                       for ln in config.LINE_NAMES}
    print(f"\n  {len(g)} stations -> {len(inside)} inside obec {config.OBEC}, "
          f"{len(outside)} outside; per line inside {inside_per_line}")
    if inside_per_line != config.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the obec keeps a different set than recorded.\n"
                 f"  measured: {inside_per_line}\n"
                 f"  config  : {config.EXPECTED_INSIDE_PER_LINE}")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": f"outside obec {config.OBEC} (Praha)",
                        "latitude": outside["latitude"], "longitude": outside["longitude"]},
                       columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename_axis("stop_id").reset_index()
            .rename(columns={"stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(out)} excluded")
    emit("platforms", len(platforms))
    emit("stations", len(st_rows))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
