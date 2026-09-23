"""Rennes step 1: STAR's métro stations inside the commune.

    python pipeline/rennes/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT FROM TOULOUSE'S, which it is copied
from:

  * **Two lines and one mode.** STAR runs métro lines a and b and nothing else
    on rails, so there is no mode decision in this file.
  * **The boundary costs one line its ends.** Line b loses 4 of its 15 stations,
    both termini among them, to Cesson-Sévigné and Saint-Jacques-de-la-Lande.
    The per-line survival assertion below is what makes that scope decision
    checkable rather than merely written down.
  * **Each excluded station's commune is NAMED, from Rennes Métropole's own
    commune contours** rather than printed as "outside 35238" - the rule Los
    Angeles set, that the municipality an excluded station is in is worth
    naming.
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
from pipeline.rennes import config


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\n"
                 f"Run: python pipeline/rennes/fetch_sources.py")
    return path


def main():
    need(config.GTFS_ZIP, "the GTFS feed")
    need(config.CITY_BOUNDARY_GEOJSON, "the commune boundary")
    need(config.METRO_COMMUNES_GEOJSON, "Rennes Métropole's commune contours")
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

    if (sorted(kept["route_id"]) != sorted(config.ROUTE_IDS)
            or sorted(rail["route_id"]) != sorted(config.ROUTE_IDS)):
        sys.exit(f"the feed's rail route_ids changed.\n"
                 f"  feed  : {sorted(rail['route_id'])}\n"
                 f"  config: {sorted(config.ROUTE_IDS)}\n"
                 f"A line added or withdrawn is a scope decision, not a config "
                 f"edit - see docs/build_briefs/rennes.md.")

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

    # ⚠ THIS COLLAPSE IS BY parent_station. Where a feed does not set one,
    # each direction's stop survives as its own "station" and the count
    # doubles - Guadalajara's exact failure. The name-level reconciliation
    # below catches it before the gates run.
    by_name = st_rows.groupby("stop_name").size()
    if (by_name > 1).any():
        dupes = by_name[by_name > 1]
        print(f"\n  collapsing {len(dupes)} name(s) still split across "
              f"{int(dupes.sum())} rows (no parent_station):")
        for nm, n in dupes.items():
            print(f"    {nm}  x{n}")
        agg = {"latitude": "mean", "longitude": "mean",
               "lines": lambda s: "/".join(sorted({l for v in s
                                                   for l in str(v).split("/")}))}
        st_rows = (st_rows.reset_index()
                   .groupby("stop_name", as_index=False)
                   .agg({**agg, "stop_id": "first"})
                   .set_index("stop_id"))

    # GATE 3's own side, PER LINE: distinct stations served by each line,
    # network-wide and BEFORE the boundary filter, because the independent
    # figures are for the whole line and not for its in-commune stretch.
    actual = {}
    for line in config.OPERATOR_STATION_COUNTS:
        actual[line] = int(sum(1 for v in st_rows["lines"]
                               if line in str(v).split("/")))

    print()
    station_gates.verify_stations(
        city="Rennes", platforms=quays, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

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

    # ⚠ SURVIVING IS NOT ENOUGH. Line b keeps 11 of its 15 stations and loses
    # both ends, so "every line has at least one station inside" is a weak
    # test a halved line would still pass. The recorded per-line figures are
    # asserted instead.
    inside_per_line = {line: int(sum(1 for v in inside["lines"]
                                     if line in str(v).split("/")))
                       for line in config.EXPECTED_INSIDE_PER_LINE}
    print("\n  per line, inside the commune:")
    for line, n in sorted(inside_per_line.items()):
        exp = config.EXPECTED_INSIDE_PER_LINE[line]
        total = config.OPERATOR_STATION_COUNTS[line]
        flag = "" if n == exp else f"   <- EXPECTED {exp}"
        print(f"    {config.LINE_NAMES[line]:<12} {n:>3} of {total:>3}{flag}")
    if inside_per_line != config.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the commune boundary now keeps a different set.\n"
                 f"  measured: {inside_per_line}\n"
                 f"  config  : {config.EXPECTED_INSIDE_PER_LINE}\n"
                 f"Scope is a decision, not a side effect - see this city's "
                 f"config and DECISIONS.md before changing the numbers.")

    # Nearest-neighbour spacing among the KEPT stations, in metres - the
    # figure config's ring-edge note records.
    proj = inside.to_crs(config.CRS_PROJECTED)
    nn = [proj.geometry.drop(i).distance(pt).min()
          for i, pt in proj.geometry.items()]
    nn = pd.Series(nn)
    print(f"\n  in-commune spacing (nearest neighbour, m): min {nn.min():,.0f}  "
          f"median {nn.median():,.0f}  mean {nn.mean():,.0f}  max {nn.max():,.0f}")

    # THE EXCLUDED RECORD, each station placed in its own commune from Rennes
    # Métropole's contours. A station outside every one of them would mean the
    # métro has left the métropole, which it does not - so that is an error,
    # not an "unknown" row.
    communes = gpd.read_file(config.METRO_COMMUNES_GEOJSON).to_crs(
        config.CRS_GEOGRAPHIC)
    excluded = []
    for stop_id, r in outside.iterrows():
        hit = communes[communes.contains(r.geometry)]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} lies in {len(hit)} of Rennes "
                     f"Métropole's communes, not exactly one")
        excluded.append({"stop_id": stop_id, "station": r["stop_name"],
                         "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['nom']} "
                                   f"({hit.iloc[0]['code']}), outside commune "
                                   f"{config.BOUNDARY_COMMUNE_CODE}",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    out = pd.DataFrame(excluded, columns=["stop_id", "station", "lines",
                                          "reason", "latitude", "longitude"])
    out.sort_values(["reason", "station"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for _, r in out.sort_values(["reason", "station"]).iterrows():
        print(f"    {r['station']:<28} {r['lines']:<4} {r['reason']}")

    keep = (inside.reset_index()
            .rename(columns={"index": "stop_id", "stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> "
          f"{config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
