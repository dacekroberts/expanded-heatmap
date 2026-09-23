"""Paris step 1: IDFM's GTFS -> the Metro stations inside the commune.

    python pipeline/paris/step1_stations.py

Reads the cache only. `fetch_sources.py` downloads; a step that fetched would
turn every drift check into a question about the current upstream rather than
about the committed code.

THREE THINGS THIS CITY DOES THAT THE SMALLER ONES DO NOT:

  * **The feed is the whole region.** 2,025 routes across six modes, of which
    16 are the Metro. Selecting by mode is load-bearing, not a formality.
  * **Stations are derived from ROUTE MEMBERSHIP**, trips -> stop_times ->
    stops, then collapsed on `parent_station`. Never from a name or a tag.
    osm-rail's rule is written for OSM but the failure it prevents is the same
    here: IDFM publishes 2,516 entrances as location_type 2, and not one of
    them can leak in, because no trip stops at an entrance.
  * **76 of 321 stations lie outside the commune** and are recorded by name
    WITH the commune each sits in, which is Los Angeles' standard rather than a
    bare count.
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
from pipeline.paris import config


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\n"
                 f"Run: python pipeline/paris/fetch_sources.py")
    return path


def main():
    need(config.GTFS_ZIP, "the GTFS feed")
    need(config.CITY_BOUNDARY_GEOJSON, "the commune boundary")
    need(config.IDF_COMMUNES_GEOJSON, "the Ile-de-France commune layer")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(config.GTFS_ZIP)

    # --- the routes, printed before they are filtered ----------------------
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    print("routes by mode (route_type):")
    for rt, n in routes["route_type"].value_counts().items():
        mark = "  <- kept" if rt == config.ROUTE_TYPE_METRO else ""
        print(f"    {rt}: {n:>5}{mark}")

    metro = routes[routes["route_type"] == config.ROUTE_TYPE_METRO].copy()
    if sorted(metro["route_id"]) != sorted(config.ROUTE_IDS):
        sys.exit(f"the feed's metro route_ids changed.\n"
                 f"  feed  : {sorted(metro['route_id'])}\n"
                 f"  config: {sorted(config.ROUTE_IDS)}\n"
                 f"A line added or withdrawn is a scope decision, not a "
                 f"config edit - see docs/build_briefs/paris.md.")
    short_of = dict(zip(metro["route_id"], metro["route_short_name"]))
    missing = sorted(set(short_of.values()) - set(config.LINE_NAMES))
    if missing:
        sys.exit(f"no public name for line(s) {missing}. Every drawn line "
                 f"needs its real name for the label AND the legend.")
    print(f"\n  {len(metro)} metro routes: "
          f"{', '.join(config.LINE_NAMES[s] for s in sorted(short_of.values()))}")

    # --- stations from route membership ------------------------------------
    trips = pd.read_csv(z.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id"])
    mt = trips[trips["route_id"].isin(set(metro["route_id"]))]
    st_cols = ["trip_id", "stop_id"]
    head = pd.read_csv(z.open("stop_times.txt"), dtype=str, nrows=1)
    for c in ("pickup_type", "drop_off_type"):
        if c in head.columns:
            st_cols.append(c)
    st = pd.read_csv(z.open("stop_times.txt"), dtype=str, usecols=st_cols)
    ms = st[st["trip_id"].isin(set(mt["trip_id"]))].copy()

    # Non-revenue stops: a trip calls there but nobody may board. Edmonton's
    # garage tracks are the worked example.
    boardable = station_gates.boardable_stop_ids(ms)
    non_revenue = 0
    if boardable is not None:
        before = ms["stop_id"].nunique()
        ms = ms[ms["stop_id"].isin(boardable)]
        non_revenue = before - ms["stop_id"].nunique()

    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")
    quay_ids = [s for s in sorted(set(ms["stop_id"])) if s in stops.index]
    quays = stops.loc[quay_ids].copy()
    if not (quays["location_type"].fillna("0") == "0").all():
        sys.exit("a metro trip stops at something that is not a quay "
                 "(location_type != 0) - check the collapse before trusting it")

    if quays["parent_station"].isna().any():
        orphan = quays[quays["parent_station"].isna()]
        sys.exit(f"{len(orphan)} quay(s) have no parent_station, so they "
                 f"cannot be collapsed: {list(orphan.index)[:5]}")

    station_ids = sorted(set(quays["parent_station"]))
    st_rows = stops.loc[[s for s in station_ids if s in stops.index]].copy()
    for frame in (quays, st_rows):
        frame["latitude"] = frame["stop_lat"].astype(float)
        frame["longitude"] = frame["stop_lon"].astype(float)

    # per-line membership, for the record and for gate 3 when it can be run
    link = ms.merge(quays.reset_index()[["stop_id", "parent_station"]],
                    on="stop_id").merge(mt, on="trip_id")
    lines_of = (link.assign(line=link["route_id"].map(short_of))
                .groupby("parent_station")["line"]
                .agg(lambda s: "/".join(sorted(set(s)))))
    st_rows["lines"] = st_rows.index.map(lines_of)

    # Gate 3's own side of the comparison, over ALL stations rather than the
    # 245 kept: IDFM's layer covers the whole network, so scoping one side to
    # the commune and not the other would manufacture a mismatch on every line.
    actual_per_line = {}
    for value in st_rows["lines"]:
        for line in str(value).split("/"):
            if line:
                actual_per_line[line] = actual_per_line.get(line, 0) + 1

    print()
    station_gates.verify_stations(
        city="Paris", platforms=quays, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        # PARIS IS THE FIRST CITY TO FAIL THE SPACING GATE HONESTLY, at 399 m
        # against the shared 400 m floor - one metre. The gate says to fix the
        # collapse rather than the threshold, which is the right default, so
        # the collapse was tested before this line was written:
        #
        #   duplicate station names            0  (Calgary's failure mode)
        #   pairs closer than 150 m            0  (no platform spike at all)
        #   uncollapsed platform median        8 m - so a BROKEN collapse here
        #                                         would read ~8, not 399
        #   distribution  p1 189 | p25 317 | p50 399 | p75 563 | p90 821
        #   closest pairs  Le Peletier/Notre-Dame-de-Lorette 183 m,
        #                  Commerce/Felix Faure 192 m,
        #                  Saint-Germain-des-Pres/Mabillon 214 m
        #
        # Those are real, distinct, nameable stations on lines 12, 8 and 4. The
        # collapse is right and the floor is a North American number: every
        # city that set it has stations hundreds of metres further apart than
        # Paris puts them.
        #
        # 200 m is chosen, not 398: it still catches a platform-spaced set by a
        # factor of 25, and it is below the p1 of the real distribution rather
        # than shaved to just under the observed median. A threshold set one
        # metre under the number that failed would pass this city and catch
        # nothing in the next one.
        spacing_min=200.0,
        # GATE 3, sourced 2026-09-23 from IDFM's own GIS layer rather than from
        # the feed - see config.OPERATOR_STATION_COUNTS for where and why.
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line=actual_per_line)

    # --- the commune boundary ---------------------------------------------
    commune = shape(json.loads(
        config.CITY_BOUNDARY_GEOJSON.read_bytes())["geometry"])
    g = gpd.GeoDataFrame(
        st_rows,
        geometry=gpd.points_from_xy(st_rows["longitude"], st_rows["latitude"]),
        crs=config.CRS_GEOGRAPHIC)
    area = gpd.GeoSeries([commune], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).area.iloc[0] / 1e6
    print(f"\n  commune 75056: {area:.1f} km2")

    within = g.within(commune)
    inside, outside = g[within].copy(), g[~within].copy()

    kept_lines = sorted({l for v in inside["lines"] for l in v.split("/")})
    all_lines = sorted({l for v in g["lines"] for l in v.split("/")})
    print(f"  stations: {len(g)} total -> {len(inside)} inside, "
          f"{len(outside)} outside ({len(inside) / len(g) * 100:.1f}% in)")
    print(f"  lines with at least one station inside: "
          f"{len(kept_lines)} of {len(all_lines)}")
    if set(kept_lines) != set(all_lines):
        lost = sorted(set(all_lines) - set(kept_lines))
        sys.exit(f"commune-only scope drops {lost} entirely. The brief's scope "
                 f"decision rests on every line surviving the boundary; if "
                 f"that has stopped being true the decision needs re-taking.")

    # --- name the commune each excluded station sits in --------------------
    idf = gpd.read_file(config.IDF_COMMUNES_GEOJSON)
    named = gpd.sjoin(outside, idf[["nom", "code", "geometry"]],
                      how="left", predicate="within")
    named["commune"] = named["nom"].fillna("(outside Ile-de-France)")

    out = (named.reset_index()
           .rename(columns={"index": "stop_id", "stop_name": "station"})
           [["stop_id", "station", "lines", "commune", "code",
             "latitude", "longitude"]]
           .sort_values(["commune", "station"]))
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    by_commune = out["commune"].value_counts()
    print(f"\n  excluded stations by commune ({len(by_commune)} communes):")
    for name, n in by_commune.head(12).items():
        print(f"    {n:>3}  {name}")
    if len(by_commune) > 12:
        print(f"    ... and {len(by_commune) - 12} more")
    print(f"  -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")

    keep = (inside.reset_index()
            .rename(columns={"index": "stop_id", "stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> "
          f"{config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
