"""Marseille step 1: RTM's métro and tram stations inside the commune.

    python pipeline/marseille/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT FROM PARIS'S:

  * **The feed is the whole Métropole**, 766 routes across five modes, of which
    five are Marseille's own. Selecting by mode is not enough here - a sixth
    `route_type 0` route is **Aubagne's tram**, a different city's network - so
    the route_ids are matched exactly and the odd one out is named.
  * **Nothing is lost to the boundary.** Measured 2026-09-23: all five of
    Marseille's lines are 100% inside commune 13055. Paris lost 76 of 321. So
    `excluded_stations.csv` here records what was excluded BY NETWORK rather
    than by geography - which is the more useful record for this city, and the
    one a reader would otherwise have no way to check.
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
from pipeline.marseille import config


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\n"
                 f"Run: python pipeline/marseille/fetch_sources.py")
    return path


def main():
    need(config.GTFS_ZIP, "the GTFS feed")
    need(config.CITY_BOUNDARY_GEOJSON, "the commune boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(config.GTFS_ZIP)
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    print("routes by mode (route_type):")
    for rt, n in routes["route_type"].value_counts().items():
        mark = "  <- rail" if rt in config.ROUTE_TYPES_RAIL else ""
        print(f"    {rt}: {n:>5}{mark}")

    rail = routes[routes["route_type"].isin(config.ROUTE_TYPES_RAIL)].copy()
    kept = rail[rail["route_id"].isin(config.ROUTE_IDS)]
    dropped = rail[~rail["route_id"].isin(config.ROUTE_IDS)]

    if sorted(kept["route_id"]) != sorted(config.ROUTE_IDS):
        sys.exit(f"the feed's rail route_ids changed.\n"
                 f"  feed  : {sorted(rail['route_id'])}\n"
                 f"  config: {sorted(config.ROUTE_IDS)}\n"
                 f"A line added or withdrawn is a scope decision, not a config "
                 f"edit - see docs/build_briefs/marseille.md.")
    for _, r in dropped.iterrows():
        why = config.EXCLUDED_RAIL_ROUTE_IDS.get(r["route_id"], "not in scope")
        print(f"  DROPPED rail route {r['route_id']} "
              f"({r.get('route_short_name')}): {why}")

    short_of = dict(zip(rail["route_id"], rail["route_short_name"]))
    missing = sorted(set(kept["route_short_name"]) - set(config.LINE_NAMES))
    if missing:
        sys.exit(f"no public name for line(s) {missing}")
    print(f"\n  {len(kept)} lines: "
          f"{', '.join(config.LINE_NAMES[s] for s in sorted(kept['route_short_name']))}")

    trips = pd.read_csv(z.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id"])
    st_cols = ["trip_id", "stop_id"]
    head = pd.read_csv(z.open("stop_times.txt"), dtype=str, nrows=1)
    for c in ("pickup_type", "drop_off_type"):
        if c in head.columns:
            st_cols.append(c)
    st = pd.read_csv(z.open("stop_times.txt"), dtype=str, usecols=st_cols)
    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")

    def station_set(route_ids):
        """Stations for a set of routes, via route membership then collapse."""
        mt = trips[trips["route_id"].isin(set(route_ids))]
        ms = st[st["trip_id"].isin(set(mt["trip_id"]))].copy()
        boardable = station_gates.boardable_stop_ids(ms)
        dropped_n = 0
        if boardable is not None:
            before = ms["stop_id"].nunique()
            ms = ms[ms["stop_id"].isin(boardable)]
            dropped_n = before - ms["stop_id"].nunique()
        ids = [s for s in sorted(set(ms["stop_id"])) if s in stops.index]
        q = stops.loc[ids].copy()
        # verify_stations measures BOTH frames, so the platforms need the
        # coordinate columns too - not only the collapsed stations.
        q["latitude"] = q["stop_lat"].astype(float)
        q["longitude"] = q["stop_lon"].astype(float)
        parent = q.get("parent_station", pd.Series(dtype=str))
        q["station_id"] = parent.where(
            parent.notna() & (parent != ""), pd.Series(q.index, index=q.index))
        sids = sorted(set(q["station_id"]))
        rows = stops.loc[[s for s in sids if s in stops.index]].copy()
        rows["latitude"] = rows["stop_lat"].astype(float)
        rows["longitude"] = rows["stop_lon"].astype(float)
        link = (ms.merge(q.reset_index()[["stop_id", "station_id"]], on="stop_id")
                  .merge(mt, on="trip_id"))
        link["line"] = link["route_id"].map(short_of)
        rows["lines"] = rows.index.map(
            link.groupby("station_id")["line"].agg(lambda s: "/".join(sorted(set(s)))))
        return q, rows, dropped_n

    quays, st_rows, non_revenue = station_set(config.ROUTE_IDS)
    print()
    station_gates.verify_stations(
        city="Marseille", platforms=quays, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        # SECOND CITY TO FAIL THE SPACING GATE HONESTLY, at 341 m against the
        # shared 400 m floor - and MORE tightly packed than Paris's 399 m,
        # which is not what a city a quarter of Paris's density suggests.
        #
        # Tested before the threshold was touched, because Paris's answer is
        # not evidence for Marseille:
        #
        #   all 150 quays carry a parent_station   collapse is complete
        #   duplicate names after collapse: 0      Calgary's failure mode
        #   uncollapsed platform median: 9 m       a broken collapse reads ~9
        #   pairs under 50 m: 0                    no platform spike
        #   p1 54 | p10 213 | p50 341 | p90 641
        #
        # THE MECHANISM IS DIFFERENT FROM PARIS'S. Paris is uniformly dense
        # metro; here the TRAM RUNS PAST THE METRO down the Canebière, so the
        # two networks interleave in the centre - Noailles and Canebiere
        # Garibaldi are 54 m apart and are genuinely different stops on
        # different modes. Metro Jules Guesde and Metro Colbert, 137 m, are two
        # real metro stations.
        #
        # 200.0, the same value Paris took, and deliberately not a third
        # bespoke number: it still catches a platform-spaced set by 22x.
        spacing_min=200.0,
        # GATE 3 NOT RUN - no operator-published per-line count has been
        # sourced for RTM. Paris's came from IDFM's own GIS layer, which is
        # what osm-rail says to look for first; the equivalent for Marseille
        # has not been found. Owed, and recorded in PLAN.md rather than
        # quietly skipped.
        expected_per_line=None, actual_per_line=None)

    commune = shape(json.loads(
        config.CITY_BOUNDARY_GEOJSON.read_bytes())["geometry"])
    g = gpd.GeoDataFrame(
        st_rows,
        geometry=gpd.points_from_xy(st_rows["longitude"], st_rows["latitude"]),
        crs=config.CRS_GEOGRAPHIC)
    area = gpd.GeoSeries([commune], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).area.iloc[0] / 1e6
    within = g.within(commune)
    inside, outside = g[within].copy(), g[~within].copy()
    print(f"\n  commune {config.BOUNDARY_COMMUNE_CODE}: {area:.1f} km2")
    print(f"  stations: {len(g)} total -> {len(inside)} inside, "
          f"{len(outside)} outside")

    kept_lines = sorted({l for v in inside["lines"] for l in v.split("/")})
    all_lines = sorted({l for v in g["lines"] for l in v.split("/")})
    if set(kept_lines) != set(all_lines):
        lost = sorted(set(all_lines) - set(kept_lines))
        sys.exit(f"commune-only scope drops {lost} entirely. The scope decision "
                 f"rests on every line surviving the boundary; if that has "
                 f"stopped being true the decision needs re-taking.")
    print(f"  lines with at least one station inside: "
          f"{len(kept_lines)} of {len(all_lines)}  (all survive)")

    # THE EXCLUDED RECORD. For Marseille this is mostly about NETWORK, not
    # geography - the opposite of every other city here, and the reason it is
    # written even though the boundary excludes nothing.
    excluded = []
    for stop_id, r in outside.iterrows():
        excluded.append({"stop_id": stop_id, "station": r["stop_name"],
                         "lines": r["lines"], "reason": "outside commune 13055",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    if dropped.shape[0]:
        _q2, other, _n = station_set(list(dropped["route_id"]))
        for stop_id, r in other.iterrows():
            rid = dropped.iloc[0]["route_id"]
            excluded.append({
                "stop_id": stop_id, "station": r["stop_name"],
                "lines": r["lines"],
                "reason": config.EXCLUDED_RAIL_ROUTE_IDS.get(rid, "not in scope"),
                "latitude": r["latitude"], "longitude": r["longitude"]})
    out = pd.DataFrame(excluded, columns=["stop_id", "station", "lines",
                                          "reason", "latitude", "longitude"])
    out.sort_values(["reason", "station"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for reason, n in out["reason"].value_counts().items():
        print(f"    {n:>3}  {reason}")

    keep = (inside.reset_index()
            .rename(columns={"index": "stop_id", "stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> "
          f"{config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
