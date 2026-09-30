"""Brno step 1: tram stops of the 11 regular lines, from KORDIS JMK's own GTFS.

    python pipeline/brno/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 WHAT IT IS:

  * **Stations are the feed's own `parent_station` rows**, Prague's shape: every
    tram platform has a parent with its own id, name and position (all 329 on
    2026-09-30), so there is no name collapse and no mean. A platform without a
    parent, or two parents sharing a name, stops the step.
  * **Selected by `route_type` 0 AND `route_short_name`**: the 11 regular
    lines. H4 and P1 are left out (owner); any other tram route the feed grows
    stops the step, because a line added is a scope decision.
  * **Gate 3 is OSM's**: the route relations' stop names per line, which the
    feed did not make. The line GEOMETRY is OSM's too (step 3), since the feed
    has no shapes.txt, so every drawn ref must have a relation.
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
from pipeline.brno import config  # noqa: E402
from pipeline.countries.czechia_boundary import city_polygon  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/brno/fetch_sources.py")
    return path


def osm_per_line():
    """Distinct stop names per ref across the operator's route=tram relations,
    and a check that every drawn line has one."""
    els = json.loads(need(config.OSM_TRAM_JSON, "OSM tram relations")
                     .read_text(encoding="utf-8"))["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    per, other = {}, []
    for r in (e for e in els if e["type"] == "relation"):
        t = r.get("tags", {})
        if t.get("operator") != config.OSM_TRAM_OPERATOR:
            other.append((r["id"], t.get("operator"), t.get("name")))
            continue
        names = {nodes[m["ref"]].get("tags", {}).get("name") for m in r["members"]
                 if m["type"] == "node" and m.get("role", "").startswith("stop")
                 and m["ref"] in nodes}
        per.setdefault(t.get("ref"), set()).update(n for n in names if n)
    missing = [k for k in config.LINE_ORDER if k not in per]
    if missing:
        sys.exit(f"OSM has no {config.OSM_TRAM_OPERATOR} relation for line(s) {missing}: "
                 f"step 3 could not draw them")
    extra = sorted(k for k in per if k not in config.LINE_ORDER)
    if extra:
        print(f"  OSM relations not drawn: refs {extra}")
    if other:
        print(f"  OSM tram relations of another operator in the box: {other}")
    return {config.LINE_NAMES[k]: len(per[k]) for k in config.LINE_ORDER}


def main():
    need(config.GTFS_ZIP, "KORDIS JMK's GTFS")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(config.GTFS_ZIP)

    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    tram = routes[routes["route_type"] == config.ROUTE_TYPE_TRAM]
    known = set(config.LINE_ORDER) | set(config.NOT_DRAWN_ROUTES)
    new = sorted(set(tram["route_short_name"]) - known)
    gone = sorted(set(config.LINE_ORDER) - set(tram["route_short_name"]))
    if new or gone:
        sys.exit(f"the feed's tram routes changed: new {new}, gone {gone} - a line "
                 f"added or withdrawn is a scope decision")
    kept = tram[tram["route_short_name"].isin(config.LINE_ORDER)]
    if kept["route_short_name"].duplicated().any():
        sys.exit(f"two route_ids share a line: {kept.to_dict('records')}")
    line_of = dict(zip(kept["route_id"], kept["route_short_name"]))
    for _, r in kept.iterrows():
        want = config.LINE_COLOURS[r["route_short_name"]].lstrip("#").upper()
        if str(r["route_color"]).upper() != want:
            print(f"  NOTE: line {r['route_short_name']}'s feed colour is now "
                  f"{r['route_color']}, the config has {want}")
    print(f"  tram routes kept: {', '.join(config.LINE_ORDER)}; left out: "
          f"{', '.join(f'{k} ({v})' for k, v in config.NOT_DRAWN_ROUTES.items())}")

    trips = pd.read_csv(z.open("trips.txt"), dtype=str,
                        usecols=["route_id", "trip_id", "direction_id"])
    trips = trips[trips["route_id"].isin(line_of)]
    wanted = set(trips["trip_id"])
    parts = [ch[ch["trip_id"].isin(wanted)]
             for ch in pd.read_csv(z.open("stop_times.txt"), dtype=str, chunksize=1_000_000,
                                   usecols=["trip_id", "stop_id", "pickup_type",
                                            "drop_off_type"])]
    st = pd.concat(parts, ignore_index=True)
    # REQUEST STOPS ARE STOPS: KORDIS codes every request stop (na znamení)
    # pickup/drop_off 3, "coordinate with the driver" - boardable under GTFS.
    # The shared default ("0" only) dropped 25 of the 149 stations.
    boardable = station_gates.boardable_stop_ids(st, boardable=("0", "2", "3"))
    before = st["stop_id"].nunique()
    st = st[st["stop_id"].isin(boardable)]
    non_revenue = before - st["stop_id"].nunique()

    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")
    link = st.merge(trips, on="trip_id")
    link["line"] = link["route_id"].map(line_of)
    link["station_id"] = link["stop_id"].map(stops["parent_station"])
    if link["station_id"].isna().any():
        sys.exit(f"tram platforms with no parent_station: "
                 f"{sorted(link.loc[link['station_id'].isna(), 'stop_id'].unique())[:10]}")

    # A LINE SERVES A STATION when it calls there on at least STOP_MIN_SHARE of
    # its trips in one direction. The feed runs ~2.5 months of timetable, and
    # the union of every trip adds depot runs and one-off workings: line 4
    # reached 54 stations where its public route has 24. Riga's 10% threshold
    # (PATTERN_MIN_SHARE), taken per STATION rather than per exact pattern,
    # because Brno's line 10 splits its Liseň branch over patterns each under
    # 10% (the branch holds 8% of the line's trips, and other lines serve it).
    dirs = trips.set_index("trip_id")["direction_id"]
    link["direction_id"] = link["trip_id"].map(dirs)
    calls = link.drop_duplicates(["trip_id", "station_id"])
    n = (calls.groupby(["line", "direction_id"])["trip_id"].nunique()
         .rename("trips").reset_index())
    share = (calls.groupby(["line", "direction_id", "station_id"])["trip_id"].nunique()
             .rename("calls").reset_index().merge(n, on=["line", "direction_id"]))
    share["share"] = share["calls"] / share["trips"]
    served = share.loc[share["share"] >= config.STOP_MIN_SHARE, ["line", "station_id"]]
    rare = sorted(set(link["station_id"]) - set(served["station_id"]))
    print(f"  {len(rare)} station(s) reached only below {config.STOP_MIN_SHARE:.0%} of "
          f"every line's trips (depot runs): "
          f"{[stops.loc[s, 'stop_name'] for s in rare]}")
    link = link.merge(served.drop_duplicates(), on=["line", "station_id"])
    lines = link.groupby("station_id")["line"].agg(
        lambda s: "/".join(sorted(set(s), key=config.LINE_ORDER.index)))

    platforms = stops.loc[sorted(set(link["stop_id"]))].copy()
    platforms["latitude"] = platforms["stop_lat"].astype(float)
    platforms["longitude"] = platforms["stop_lon"].astype(float)
    st_rows = stops.loc[lines.index, ["stop_name", "stop_lat", "stop_lon"]].copy()
    st_rows["latitude"] = st_rows["stop_lat"].astype(float)
    st_rows["longitude"] = st_rows["stop_lon"].astype(float)
    st_rows["lines"] = lines
    if st_rows["stop_name"].duplicated().any():
        sys.exit(f"two parent stations share a name: "
                 f"{sorted(st_rows.loc[st_rows['stop_name'].duplicated(), 'stop_name'])}")

    def count(frame):
        return {ln: int(sum(1 for v in frame["lines"] if ln in v.split("/")))
                for ln in config.LINE_ORDER}

    per_line = count(st_rows)
    print(f"\n  {len(platforms)} platforms -> {len(st_rows)} stations; per line {per_line}")
    osm = osm_per_line()
    print()
    station_gates.verify_stations(
        city="Brno", platforms=platforms, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, non_revenue=non_revenue,
        spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS or osm,
        actual_per_line={config.LINE_NAMES[k]: v for k, v in per_line.items()})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE or 'OSM route relations, distinct stop names per ref (build day)'}")

    poly = city_polygon(config)
    g = gpd.GeoDataFrame(st_rows, geometry=gpd.points_from_xy(st_rows["longitude"],
                                                              st_rows["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    mask = g.within(poly)
    inside, outside = g[mask].copy(), g[~mask].copy()
    inside_per_line = count(inside)
    print(f"\n  {len(g)} stations -> {len(inside)} inside obec 582786, {len(outside)} "
          f"outside; per line inside {inside_per_line}")
    if config.EXPECTED_INSIDE_PER_LINE and inside_per_line != config.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the obec keeps a different set than recorded.\n"
                 f"  measured: {inside_per_line}\n"
                 f"  config  : {config.EXPECTED_INSIDE_PER_LINE}")
    if not config.EXPECTED_INSIDE_PER_LINE:
        sys.exit("EXPECTED_INSIDE_PER_LINE is empty: record the measured set above in "
                 "config.py (a decision re-taken if it ever changes), then re-run")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")

    cols = ["station", "lines", "reason", "latitude", "longitude"]
    pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                  "reason": "outside obec 582786 (Brno)",
                  "latitude": outside["latitude"], "longitude": outside["longitude"]},
                 columns=cols).to_csv(config.EXCLUDED_STATIONS_CSV, index=False,
                                      encoding="utf-8")
    keep = (inside.rename_axis("stop_id").reset_index()
            .rename(columns={"stop_name": "station"})
            [["stop_id", "station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(outside)} excluded")
    emit("platforms", len(platforms))
    emit("stations", len(st_rows))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(outside))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
