"""TEC's static GTFS, read once for Charleroi's light metro and Liege's tram.

The feed is LETEC's (the agency name in `agency.txt`), published through the
Belgian Mobility Company portal under its CC BY 4.0 terms (licence read
2026-10-04; docs/decisions_drafts/staging.md). One copy serves both cities:
`FEED_ZIP` in `data/belgium/raw/`, installed by a city's `fetch_sources.py`
from the copy the owner ratified (fetched 2026-10-03, Belgium build call 1).
A re-fetch after the portal's terms change goes back to the owner, so no
script here downloads it.

What the feed holds (measured 2026-10-04, feed_version 20261002):

* route_type 1: M2, M3 and M4 (Charleroi). **M1 is absent as a metro route**:
  `M1ab` is a bus (route_type 3), as are `M3ab` and `M4ab`.
* route_type 0: T1 (Liege), one route.
* `parent_station` is populated on every served platform, so stations
  collapse on it (the add-city skill's first and best mechanism).
* Stop names read "LOCALITY Name (M)" / "(Tram)": an upper-case locality
  (often a former commune), the stop's own name, a mode suffix, and at
  Charleroi's Gare Centrale a quay suffix. `display_name` keeps the stop's own
  name only.
* `feed_info.txt`'s two dates carry a leading space (" 20261225"):
  `feed_info` strips them.
* `stop_times.txt` is 502 MB: read in chunks (peak 0.72 GB measured
  2026-10-04 with the trips filter).
"""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from pipeline.countries.belgium import CRS_GEOGRAPHIC, CRS_PROJECTED, SHARED_RAW
from pipeline.stations import boardable_stop_ids

_ROOT = Path(__file__).parent.parent.parent
FEED_ZIP = SHARED_RAW / "tec_gtfs_static.zip"
FEED_META_JSON = SHARED_RAW / "tec_gtfs_static.zip.json"
# The ratified copy (fetched 2026-10-03 local, 2026-10-04 06:40 UTC) and its
# measured identity; `install_feed` copies it to FEED_ZIP.
RATIFIED_COPY = (_ROOT / "data" / "_brief_check" / "raw" /
                 "https___api-management-discovery-production.azure-api.net_api_gtfs_feed_tec_static.zip")
FEED_URL = "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static"
FEED_BYTES = 84926285
FEED_SHA256 = "6fce0898d83a51c7e78c62ce16d76fd8130ee46190ff764450515927868e091b"
FEED_FETCHED_UTC = "2026-10-04T06:40:22+00:00"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def feed_info(zip_path):
    """feed_info.txt as a dict, every value stripped (the leading-space trap)."""
    with zipfile.ZipFile(zip_path) as z, z.open("feed_info.txt") as f:
        fi = pd.read_csv(f, dtype=str, keep_default_na=False)
    return {k: str(v).strip() for k, v in fi.iloc[0].items()}


def install_feed():
    """Copy the ratified feed to FEED_ZIP after checking its sha256; write its
    meta JSON. Never downloads. Returns the provenance dict."""
    import json
    import shutil

    if not FEED_ZIP.exists() or sha256(FEED_ZIP) != FEED_SHA256:
        if not RATIFIED_COPY.exists():
            sys.exit(f"the ratified TEC feed is missing ({RATIFIED_COPY.name}); a new fetch "
                     f"is the owner's call (the portal counts access as accepting its terms)")
        got = sha256(RATIFIED_COPY)
        if got != FEED_SHA256:
            sys.exit(f"the ratified TEC feed's sha256 is {got}, not {FEED_SHA256}")
        FEED_ZIP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RATIFIED_COPY, FEED_ZIP)
    if sha256(FEED_ZIP) != FEED_SHA256:
        sys.exit(f"{FEED_ZIP.name} does not match the ratified copy")
    fi = feed_info(FEED_ZIP)
    with zipfile.ZipFile(FEED_ZIP) as z:
        built = max(i.date_time for i in z.infolist())
        with z.open("agency.txt") as f:
            agency = pd.read_csv(f, dtype=str).iloc[0]["agency_name"]
    meta = {
        "url": FEED_URL,
        "publisher": f"{agency} (TEC), via the Belgian Mobility Company portal",
        "fetched_utc": FEED_FETCHED_UTC,
        "bytes": FEED_BYTES,
        "sha256": FEED_SHA256,
        "feed_version": fi["feed_version"],
        "feed_start_date": fi["feed_start_date"],
        "feed_end_date": fi["feed_end_date"],
        "zip_entries_dated": "%04d-%02d-%02d %02d:%02d" % built[:5],
        "licence": "CC BY 4.0 (Belgian Mobility Company portal terms, art. 3)",
        "approved": "owner, 2026-10-03 (Belgium build call 1: the cached feeds ratified)",
    }
    FEED_META_JSON.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8", newline="\n")
    return meta


def _need_feed(fetch_script):
    if not FEED_ZIP.exists():
        sys.exit(f"{FEED_ZIP} missing: run python {fetch_script}")


def _read(z, name, **kw):
    with z.open(name) as f:
        return pd.read_csv(f, dtype=str, **kw)


def read_routes(fetch_script):
    _need_feed(fetch_script)
    with zipfile.ZipFile(FEED_ZIP) as z:
        return _read(z, "routes.txt")


def rail_tables(fetch_script, route_ids):
    """(trips, stop_times, stops) for `route_ids`: stop_times read in chunks."""
    _need_feed(fetch_script)
    with zipfile.ZipFile(FEED_ZIP) as z:
        trips = _read(z, "trips.txt")
        trips = trips[trips["route_id"].isin(route_ids)].copy()
        ids = set(trips["trip_id"])
        parts = []
        with z.open("stop_times.txt") as f:
            for ch in pd.read_csv(f, dtype=str, chunksize=2_000_000,
                                  usecols=["trip_id", "stop_id", "stop_sequence",
                                           "departure_time", "pickup_type", "drop_off_type"]):
                parts.append(ch[ch["trip_id"].isin(ids)])
        stop_times = pd.concat(parts, ignore_index=True)
        stops = _read(z, "stops.txt")
    return trips, stop_times, stops


def active_services(fetch_script, day):
    """service_ids running on `day` (YYYYMMDD), calendar plus its exceptions."""
    with zipfile.ZipFile(FEED_ZIP) as z:
        cal = _read(z, "calendar.txt")
        cd = _read(z, "calendar_dates.txt")
    weekday = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
               "sunday"][pd.Timestamp(day).dayofweek]
    on = set(cal.loc[(cal["start_date"] <= day) & (cal["end_date"] >= day)
                     & (cal[weekday] == "1"), "service_id"])
    on -= set(cd.loc[(cd["date"] == day) & (cd["exception_type"] == "2"), "service_id"])
    on |= set(cd.loc[(cd["date"] == day) & (cd["exception_type"] == "1"), "service_id"])
    return on


_LOCALITY = re.compile(r"^(?:[A-ZÀ-Þ'\-]+\s+)+?(?=[A-ZÀ-Þ][a-zß-ÿ']|[a-zß-ÿ])")
_SUFFIX = re.compile(r"\s*(?:-\s*Quai\s*\d+\s*)?\((?:M|Tram|tram)\)\s*$|\s*-\s*Quai\s*\d+\s*$")


def display_name(feed_name):
    """The stop's own name from TEC's "LOCALITY Name (M)" form: the upper-case
    locality prefix, the quay suffix and the mode suffix dropped.
    "CHARLEROI Gare Centrale - Quai 01 (M)" -> "Gare Centrale"."""
    s = _SUFFIX.sub("", feed_name.strip())
    s = _SUFFIX.sub("", s)
    m = _LOCALITY.match(s)
    out = s[m.end():] if m else s
    if not out or out == out.upper():
        sys.exit(f"stop name {feed_name!r} does not read as 'LOCALITY Name': "
                 f"re-read display_name before collapsing")
    return out.strip()


def locality(feed_name):
    m = _LOCALITY.match(feed_name.strip())
    return m.group(0).strip() if m else ""


def collapse(trips, stop_times, stops, line_of_route, name_aliases, merged_names,
             max_spread_m, spread_allowed=None):
    """Platforms -> stations: collapse on parent_station, then on the display
    name (with `name_aliases` applied), each name's coordinates the mean of
    its boardable served platforms.

    `merged_names`: the display names that may gather more than one parent
    (owner-approved merges); any other name that does stops the step, as does
    a name whose platforms spread over `max_spread_m` (or its own figure in
    `spread_allowed`, {name: metres}, for a measured exception).

    Returns (platforms, stations, report): platforms one row per boardable
    served stop; stations with station, lines, latitude, longitude, parents,
    feed_names.
    """
    import geopandas as gpd

    spread_allowed = spread_allowed or {}
    st = stop_times.merge(trips[["trip_id", "route_id"]], on="trip_id")
    st["line"] = st["route_id"].map(line_of_route)
    served = stops[stops["stop_id"].isin(set(st["stop_id"]))].copy()
    if served["parent_station"].isna().any() or (served["parent_station"] == "").any():
        sys.exit(f"parent_station blank on {int(served['parent_station'].isna().sum())} "
                 f"served stop(s): it was populated on all of them on 2026-10-04")
    ok = boardable_stop_ids(st)
    non_rev = served[~served["stop_id"].isin(ok)] if ok is not None else served.iloc[0:0]
    served = served[served["stop_id"].isin(ok)] if ok is not None else served
    served["latitude"] = served["stop_lat"].astype(float)
    served["longitude"] = served["stop_lon"].astype(float)
    served["name"] = served["stop_name"].map(display_name).map(
        lambda n: name_aliases.get(n, n))
    lines_of_stop = st.groupby("stop_id")["line"].apply(lambda s: set(s))
    served["lines"] = served["stop_id"].map(lines_of_stop)

    pts = gpd.GeoSeries(gpd.points_from_xy(served["longitude"], served["latitude"]),
                        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    served["_x"], served["_y"] = pts.x.values, pts.y.values
    rows, report = [], []
    for name, g in served.groupby("name", sort=True):
        parents = sorted(set(g["parent_station"]))
        spread = float(max(np.hypot(g["_x"] - g["_x"].mean(), g["_y"] - g["_y"].mean())) * 2)
        if len(parents) > 1:
            report.append((name, parents, sorted(set(g["stop_name"])), spread))
            if name not in merged_names:
                sys.exit(f"{name!r} gathers {len(parents)} parent stations {parents} - a merge "
                         f"of differently named stops is the owner's (tram-city section 2); "
                         f"add it to config only with that call")
        limit = spread_allowed.get(name, max_spread_m)
        if spread > limit:
            sys.exit(f"{name!r}: its platforms spread {spread:.0f} m, over {limit:.0f} m")
        lines = sorted(set().union(*g["lines"]))
        rows.append({"station": name, "lines": "/".join(lines),
                     "latitude": round(float(g["latitude"].mean()), 7),
                     "longitude": round(float(g["longitude"].mean()), 7),
                     "parents": len(parents), "platforms": len(g),
                     "feed_names": " | ".join(sorted(set(g["stop_name"])))})
    unused = sorted(set(merged_names) - {r[0] for r in report})
    if unused:
        sys.exit(f"config names merges the feed no longer needs: {unused} - re-read them")
    stations = pd.DataFrame(rows)
    platforms = served.drop(columns=["_x", "_y"])
    return platforms, stations, {"merges": report, "non_revenue": non_rev}


def stations_per_line(stations, lines):
    return {ln: int(stations["lines"].str.split("/").apply(lambda ls: ln in ls).sum())
            for ln in lines}


def headways(trips, stop_times, stops, line_of_route, day_services, start="09:00", end="16:00"):
    """{line: {direction: (departures, median gap, max gap)}} between `start`
    and `end` on the day whose services are `day_services`, measured at the
    stop most of the line's trips call at."""
    t = trips[trips["service_id"].isin(day_services)]
    st = stop_times[stop_times["trip_id"].isin(set(t["trip_id"]))].merge(
        t[["trip_id", "route_id", "direction_id"]], on="trip_id")
    st["line"] = st["route_id"].map(line_of_route)
    st["parent"] = st["stop_id"].map(stops.set_index("stop_id")["parent_station"])
    h0 = int(start[:2]) * 60 + int(start[3:])
    h1 = int(end[:2]) * 60 + int(end[3:])
    out = {}
    for line, g in st.groupby("line"):
        top = g.groupby("parent")["trip_id"].nunique().idxmax()
        x = g[g["parent"] == top].copy()
        x["min"] = x["departure_time"].str.split(":").map(lambda p: int(p[0]) * 60 + int(p[1]))
        out[line] = {}
        for d, gd in x.groupby("direction_id"):
            day = gd[(gd["min"] >= h0) & (gd["min"] < h1)].sort_values("min")
            gaps = day["min"].diff().dropna()
            out[line][d] = (len(day), float(gaps.median()), float(gaps.max()))
    return out


def line_shapes(trips, stop_times, stops, line_of_route, name_aliases):
    """{line: (shape_id, ...)}: shapes ranked by trips (ties by shape_id), a
    shape added only if it reaches a station the picked ones miss, until every
    station of the line is on a drawn shape - France's rule
    (pipeline/countries/france_tram.py). One shape where the line runs one
    alignment; more where it forks or splits into one-way streets."""
    st = stop_times.merge(trips[["trip_id", "route_id", "shape_id"]], on="trip_id")
    st["line"] = st["route_id"].map(line_of_route)
    names = stops[stops["stop_id"].isin(set(st["stop_id"]))].set_index("stop_id")[
        "stop_name"].map(display_name).map(lambda n: name_aliases.get(n, n))
    st["name"] = st["stop_id"].map(names)
    out = {}
    for line, g in st.groupby("line"):
        all_names = set(g["name"])
        trips_per = g.groupby("shape_id")["trip_id"].nunique()
        reach = g.groupby("shape_id")["name"].apply(set)
        ranked = sorted(trips_per.index, key=lambda s: (-trips_per[s], s))
        picked, covered = [], set()
        for s in ranked:
            if picked and not (reach[s] - covered):
                continue
            picked.append(s)
            covered |= reach[s]
            if covered >= all_names:
                break
        out[line] = (tuple(picked), {s: int(trips_per[s]) for s in picked},
                     len(covered), len(all_names))
    return out


def build_stations(cfg):
    """Step 1 for a Walloon city: TEC's lines in `cfg.LINES`, every stop,
    collapsed, gated, split by commune. Writes cfg.STATIONS_CSV (the stations
    in the commune) and cfg.EXCLUDED_STATIONS_CSV (the rest, with the commune
    each lies in). Reads the cache only."""
    import geopandas as gpd

    from pipeline import stations as station_gates
    from pipeline.baseline import emit
    from pipeline.countries.belgium import commune_polygons

    cfg.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)

    # --- routes: matched on route_short_name and route_type ----------------
    routes = read_routes(cfg.FETCH)
    rail = routes[routes["route_type"].isin(["0", "1"])]
    print("TEC's rail routes (route_type 0 and 1), and the buses that share a line's name:")
    lookalike = routes[routes["route_short_name"].fillna("").str.match(r"^[MT]\d")]
    for r in pd.concat([rail, lookalike]).drop_duplicates("route_id").sort_values(
            "route_short_name").itertuples():
        kept = "DRAWN" if (r.route_type == cfg.ROUTE_TYPE and r.route_short_name in cfg.LINES) \
            else "not drawn"
        print(f"  {r.route_short_name:<6} type {r.route_type}  {r.route_id:<22} "
              f"#{r.route_color}  {kept}: {r.route_long_name}")
    mine = rail[rail["route_type"] == cfg.ROUTE_TYPE]
    got = sorted(mine["route_short_name"])
    if got != sorted(cfg.LINES):
        sys.exit(f"route_type {cfg.ROUTE_TYPE} routes are {got}, config draws "
                 f"{sorted(cfg.LINES)}: TEC's network changed - re-read the lines")
    colours = set(mine["route_color"].str.upper())
    if colours != {cfg.FEED_ROUTE_COLOR}:
        sys.exit(f"the feed's route_color is now {sorted(colours)}, config recorded "
                 f"{cfg.FEED_ROUTE_COLOR}: re-take the colour call")
    line_of_route = dict(zip(mine["route_id"], mine["route_short_name"]))

    # --- platforms -> stations -----------------------------------------------
    trips, stop_times, stops = rail_tables(cfg.FETCH, set(line_of_route))
    platforms, st, rep = collapse(trips, stop_times, stops, line_of_route,
                                  cfg.NAME_ALIASES, cfg.MERGED_NAMES,
                                  cfg.COLLAPSE_MAX_SPREAD_M,
                                  getattr(cfg, "COLLAPSE_SPREAD_ALLOWED", None))
    print(f"\n{len(platforms)} boardable served platforms, "
          f"{platforms['parent_station'].nunique()} parent stations -> {len(st)} stations")
    if len(rep["non_revenue"]):
        print(f"  {len(rep['non_revenue'])} served stop(s) with no boardable stop_time dropped")
    for name, parents, feed_names, spread in rep["merges"]:
        print(f"  merged (owner): {name!r} from {len(parents)} parents {parents}, "
              f"feed names {feed_names}, platforms within {spread:.0f} m")
    dup = st["station"].duplicated()
    if dup.any():
        sys.exit(f"duplicate station names after the collapse: {sorted(st.loc[dup, 'station'])}")

    per_line = stations_per_line(st, cfg.LINES)
    print()
    res = station_gates.verify_stations(
        city=cfg.NAME, platforms=platforms, stations=st,
        crs_projected=cfg.CRS_PROJECTED, spacing_min=cfg.SPACING_MIN_M,
        expected_per_line=cfg.OPERATOR_STATION_COUNTS, actual_per_line=per_line)
    if cfg.OPERATOR_STATION_COUNTS is None:
        print(f"    GATE 3 GAP (config.OPERATOR_COUNTS_GAP): {cfg.OPERATOR_COUNTS_GAP}")
    # Gate 3 stops a tram step 1 (the tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the operator's counts - " + "; ".join(
            f"{ln}: build {b}, operator {o}" for ln, (b, o) in res["per_line_mismatches"].items()))

    # --- frequency -----------------------------------------------------------
    hw = headways(trips, stop_times, stops, line_of_route,
                  active_services(cfg.FETCH, cfg.HEADWAY_DAY))
    print(f"\nDaytime headways (09-16) on {cfg.HEADWAY_DAY}, minutes:")
    for line in cfg.LINES:
        for d, (n, med, mx) in sorted(hw.get(line, {}).items()):
            print(f"  {line} direction {d}: {n} departures, median gap {med:g}, longest {mx:g}")
            if cfg.HEADWAY_MAX_MIN is not None and med > cfg.HEADWAY_MAX_MIN:
                sys.exit(f"{line} runs every {med:g} minutes by day, under the light-rail "
                         f"15-minute test (docs/category_rules.md): its stops go to "
                         f"excluded_stations.csv as infrequent - the owner's call first")

    # --- drawn shapes ----------------------------------------------------------
    shapes = line_shapes(trips, stop_times, stops, line_of_route, cfg.NAME_ALIASES)
    print("\nDrawn shapes (by trips; a shape added only where it reaches stations "
          "the others miss):")
    for line in cfg.LINES:
        picked, n_trips, covered, total = shapes[line]
        print(f"  {line}: {', '.join(f'{s} ({n_trips[s]} trips)' for s in picked)}; "
              f"{covered}/{total} stations on a drawn shape")
        if picked != tuple(cfg.LINE_SHAPES[line]):
            sys.exit(f"{line}: the pick is now {picked}, config draws "
                     f"{cfg.LINE_SHAPES[line]} - update LINE_SHAPES")
        if covered != total:
            sys.exit(f"{line}: {total - covered} station(s) on no shape")

    # --- the commune split ---------------------------------------------------
    print("\nCommunes (OpenStreetMap, cache):")
    com = commune_polygons(cfg.OSM_COMMUNES_JSON, cfg.FETCH, cfg.NIS, cfg.COMMUNE_AREA_KM2,
                           cfg.NAME)
    gst = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                           crs=CRS_GEOGRAPHIC)
    j = gpd.sjoin(gst, com[["nis", "name", "geometry"]], how="left", predicate="within")
    if j.index.duplicated().any():
        sys.exit("a station falls in two communes: the polygons overlap")
    if j["nis"].isna().any():
        sys.exit(f"stations in no commune of the cache: {sorted(j.loc[j['nis'].isna(), 'station'])}"
                 f" - widen COMMUNE_BBOX (an Overpass query is the lead's)")
    inside = j[j["nis"] == cfg.NIS].copy()
    outside = j[j["nis"] != cfg.NIS].copy()
    print(f"  {len(st)} stations -> {len(inside)} in the commune, {len(outside)} outside"
          + (": " + ", ".join(f"{k} {v}" for k, v in outside["name"].value_counts().items())
             if len(outside) else ""))
    print("  per line, stations inside / all:")
    for line in cfg.LINES:
        on = st["lines"].str.split("/").apply(lambda ls: line in ls)
        k = int(inside["lines"].str.split("/").apply(lambda ls: line in ls).sum())
        print(f"    {line:<4} {k:>3} / {int(on.sum()):<3} ({k / int(on.sum()):.0%})")
        if k == 0:
            sys.exit(f"{line} has no station in the commune - a stub question for the owner")

    # --- spacing and the rings -----------------------------------------------
    for label, frame in (("in the commune", inside), ("all drawn", st)):
        d = station_gates.nearest_neighbour_m(frame["longitude"], frame["latitude"],
                                              cfg.CRS_PROJECTED)
        q = np.percentile(d, [0, 25, 50, 75, 100])
        print(f"  nearest-neighbour gap, {label} ({len(frame)}): min {q[0]:.0f}  p25 {q[1]:.0f}  "
              f"median {q[2]:.0f}  mean {d.mean():.0f}  p75 {q[3]:.0f}  max {q[4]:.0f} m")
        if label == "in the commune":
            median_in = float(q[2])
    lo, hi = cfg.MEDIAN_GAP_BOUNDS_M
    if not lo <= median_in <= hi:
        sys.exit(f"the in-commune median gap is {median_in:.0f} m, outside {lo:.0f}-{hi:.0f}: "
                 f"re-take the ring decision (docs/ring_rules.md)")
    print(f"  rings: {cfg.RING_LABELS} (the spacing rule: halved at about 550 m or less)")

    # --- outputs ----------------------------------------------------------------
    out = pd.DataFrame({
        "station": outside["station"], "lines": outside["lines"],
        "reason": [f"in {n} (NIS {c}), outside the Ville de {cfg.NAME}"
                   for n, c in zip(outside["name"], outside["nis"])],
        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(cfg.EXCLUDED_STATIONS_CSV, index=False,
                                                  encoding="utf-8", lineterminator="\n")
    keep = inside[["station", "lines", "latitude", "longitude"]].sort_values("station")
    keep.to_csv(cfg.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(keep)} stations -> {cfg.STATIONS_CSV.relative_to(cfg.ROOT)}")
    print(f"  {len(out)} excluded -> {cfg.EXCLUDED_STATIONS_CSV.relative_to(cfg.ROOT)}")

    emit("platforms", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))
    emit("median_gap_m", round(median_in))
    for line in cfg.LINES:
        emit(f"stations_{line}", per_line[line])
