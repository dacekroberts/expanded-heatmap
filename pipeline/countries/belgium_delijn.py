"""De Lijn's static GTFS, read for the Flemish tram cities (Antwerp, Ghent).

One feed serves both cities, cached once at `data/belgium/raw/delijn_gtfs.zip`
with its meta JSON (`pipeline/countries/belgium_fetch.py`, `adopt_delijn_feed`,
called by each city's `fetch_sources.py`). This module only reads it.

WHAT THE FEED IS (measured 2026-10-04 on the copy fetched 2026-10-03, feed
version 20261003_20261130_003000):

  * 1,864 routes, 42 of them `route_type` 0 (trams): Antwerp's 1, 2, 4, 6, 7,
    8, 10, 11, 12, 24, A3 and A9 (two route_ids each, one per direction),
    Ghent's T1 (6), T2 (4) and T4 (4), and the Kusttram KT (4). Lines are
    matched on `route_short_name`, never `route_id` (add-city Step 4).
  * NO `parent_station`: a station's platforms are separate stops, told apart
    by a platform marker in the name ("perron 1", "Metro Perron A", "Metro").
    The cities merge them into one station by name (owner, 2026-10-03).
  * `stop_times.txt` is 1.79 GB: it is read in 2,000,000-row chunks, filtered
    to the city's tram trips, through `scripts/heavy_job.py`, and the filtered
    rows are cached per city in `data/<city>/processed/` keyed on the feed
    version, so a re-run reads the cache (the brief measured 0.88 GB peak).
  * `shapes.txt` is 404 MB: step 1 writes the drawn lines' shapes to a small
    zip in `data/<city>/processed/` for step 3.

A LINE'S STOPS are its regular route over the feed's window
(`pipeline/countries/belgium_tram.py`). The REFERENCE DATE, the first Tuesday
at least seven days after the feed's start date (2026-10-13 for this feed, the
date both briefs measured), is used only to check every line runs and to read
daytime headways. A single date is not used for the stops: on 2026-10-13
Ghent's Bijlokehof sat in a closure that ends two days later (measured
2026-10-04).
"""
import json
import re
import sys
import unicodedata
import zipfile
from datetime import date, timedelta

import pandas as pd

from pipeline.countries.belgium import SHARED_RAW

FEED_URL = "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/delijn/static"
FEED_ZIP = SHARED_RAW / "delijn_gtfs.zip"
FEED_META = SHARED_RAW / "delijn_gtfs.zip.json"

TRAM = "0"
# Every tram network in the feed, by route_short_name. A short name in none of
# them stops step 1: a new tram line is a scope decision, not a config edit.
TRAM_NETWORKS = {
    "antwerp": ("1", "2", "4", "6", "7", "8", "10", "11", "12", "24", "A3", "A9"),
    "ghent": ("T1", "T2", "T4"),
    "kusttram": ("KT",),
}

CHUNK_ROWS = 2_000_000
STOP_TIME_COLS = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence",
                  "pickup_type", "drop_off_type"]


def need_feed(fetch_script):
    if not FEED_ZIP.exists() or not FEED_META.exists():
        sys.exit(f"missing De Lijn's feed {FEED_ZIP} (or its meta JSON): run python {fetch_script}")
    return zipfile.ZipFile(FEED_ZIP), json.loads(FEED_META.read_text(encoding="utf-8"))


def feed_info(z):
    """{'start': date, 'end': date, 'version': str} from feed_info.txt.

    The dates carry a leading space in this feed (as TEC's do), so they are
    stripped before parsing."""
    fi = pd.read_csv(z.open("feed_info.txt"), dtype=str, keep_default_na=False).iloc[0]

    def d(s):
        s = s.strip()
        return date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    return {"start": d(fi["feed_start_date"]), "end": d(fi["feed_end_date"]),
            "version": fi["feed_version"].strip()}


def reference_date(info):
    """The first Tuesday at least seven days after the feed's start date."""
    d = info["start"] + timedelta(days=7)
    while d.weekday() != 1:
        d += timedelta(days=1)
    if d > info["end"]:
        sys.exit(f"the feed ends {info['end']}, before its reference Tuesday {d}")
    return d


def tram_routes(z, city):
    """The city's tram routes, after printing every tram route in the feed.

    Stops if a configured line is missing, or if the feed carries a tram short
    name that belongs to no network in TRAM_NETWORKS."""
    routes = pd.read_csv(z.open("routes.txt"), dtype=str, keep_default_na=False)
    trams = routes[routes["route_type"] == TRAM].sort_values(["route_short_name", "route_id"])
    print(f"  {len(routes):,} routes in the feed, {len(trams)} of them route_type {TRAM} (tram):")
    for _, r in trams.iterrows():
        print(f"    {r['route_short_name']:<4} {r['route_id']:<18} #{r['route_color']} "
              f"(text #{r['route_text_color']})  {r['route_long_name']}")
    known = set().union(*TRAM_NETWORKS.values())
    unknown = sorted(set(trams["route_short_name"]) - known)
    if unknown:
        sys.exit(f"tram short name(s) {unknown} belong to no network in TRAM_NETWORKS - a new "
                 f"line is a scope decision: read it before adding it")
    lines = TRAM_NETWORKS[city]
    mine = trams[trams["route_short_name"].isin(lines)].copy()
    missing = sorted(set(lines) - set(mine["route_short_name"]))
    if missing:
        sys.exit(f"line(s) {missing} are not tram routes in this feed - the network moved; "
                 f"re-read it before step 1")
    return mine, trams


def colours(routes):
    """{line: (route_color, route_text_color)}, both '#RRGGBB'; one colour per line."""
    out = {}
    for line, g in routes.groupby("route_short_name"):
        pairs = set(zip(g["route_color"].str.upper(), g["route_text_color"].str.upper()))
        if len(pairs) != 1:
            sys.exit(f"line {line} carries {len(pairs)} colours across its route_ids: {pairs}")
        c, t = pairs.pop()
        out[line] = (f"#{c}", f"#{t}")
    return out


def active_services(z, day):
    """service_ids running on `day`, from calendar.txt and calendar_dates.txt."""
    ymd = day.strftime("%Y%m%d")
    on = set()
    names = set(z.namelist())
    if "calendar.txt" in names:
        cal = pd.read_csv(z.open("calendar.txt"), dtype=str, keep_default_na=False)
        wd = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
              "sunday"][day.weekday()]
        live = cal[(cal["start_date"].str.strip() <= ymd) & (cal["end_date"].str.strip() >= ymd)
                   & (cal[wd] == "1")]
        on |= set(live["service_id"])
    if "calendar_dates.txt" in names:
        cd = pd.read_csv(z.open("calendar_dates.txt"), dtype=str, keep_default_na=False)
        cd = cd[cd["date"].str.strip() == ymd]
        on |= set(cd.loc[cd["exception_type"] == "1", "service_id"])
        on -= set(cd.loc[cd["exception_type"] == "2", "service_id"])
    return on


def service_days(z, start, end):
    """{service_id: set of 'YYYYMMDD'} between `start` and `end` (dates),
    from calendar.txt's ranges and calendar_dates.txt's exceptions."""
    lo, hi = start.strftime("%Y%m%d"), end.strftime("%Y%m%d")
    days = {}
    names = set(z.namelist())
    if "calendar.txt" in names:
        cal = pd.read_csv(z.open("calendar.txt"), dtype=str, keep_default_na=False)
        wd = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for _, r in cal.iterrows():
            a = date(int(r["start_date"][:4]), int(r["start_date"][4:6]), int(r["start_date"][6:8]))
            b = date(int(r["end_date"][:4]), int(r["end_date"][4:6]), int(r["end_date"][6:8]))
            d = max(a, start)
            while d <= min(b, end):
                if r[wd[d.weekday()]] == "1":
                    days.setdefault(r["service_id"], set()).add(d.strftime("%Y%m%d"))
                d += timedelta(days=1)
    if "calendar_dates.txt" in names:
        cd = pd.read_csv(z.open("calendar_dates.txt"), dtype=str, keep_default_na=False)
        cd = cd[(cd["date"] >= lo) & (cd["date"] <= hi)]
        for sid, dt, ex in zip(cd["service_id"], cd["date"], cd["exception_type"]):
            if ex == "1":
                days.setdefault(sid, set()).add(dt)
            elif ex == "2":
                days.get(sid, set()).discard(dt)
    return days


def tram_trips(z, routes):
    trips = pd.read_csv(z.open("trips.txt"), dtype=str, keep_default_na=False,
                        usecols=["route_id", "service_id", "trip_id", "direction_id", "shape_id",
                                 "trip_headsign"])
    trips = trips[trips["route_id"].isin(set(routes["route_id"]))].copy()
    trips["line"] = trips["route_id"].map(dict(zip(routes["route_id"], routes["route_short_name"])))
    return trips


def tram_stop_times(z, trips, cache_csv, version):
    """(the city's tram stop_times, every stop_id any trip of any mode serves),
    from the cache when it matches the feed.

    The second is what tells a stop the feed still lists but no trip serves
    (a station closed for works). The cache's sidecar JSON records the feed
    version and the trip count; any difference re-reads stop_times.txt."""
    side = cache_csv.with_suffix(".json")
    served_txt = cache_csv.with_name(cache_csv.stem + "_served_stop_ids.txt")
    want = {"feed_version": version, "trips": int(trips["trip_id"].nunique())}
    if cache_csv.exists() and side.exists() and served_txt.exists():
        if json.loads(side.read_text(encoding="utf-8")) == want:
            st = pd.read_csv(cache_csv, dtype=str, keep_default_na=False)
            served = set(served_txt.read_text(encoding="utf-8").split())
            print(f"  tram stop_times from the cache: {len(st):,} rows "
                  f"({cache_csv.name}, feed {version})")
            return st, served
        print("  the cached tram stop_times are for another feed or trip set: re-reading")
    ids = set(trips["trip_id"])
    parts, seen, served = [], 0, set()
    for chunk in pd.read_csv(z.open("stop_times.txt"), dtype=str, keep_default_na=False,
                             usecols=STOP_TIME_COLS, chunksize=CHUNK_ROWS):
        seen += len(chunk)
        served |= set(chunk["stop_id"])
        parts.append(chunk[chunk["trip_id"].isin(ids)])
        print(f"    read {seen:,} stop_times rows", flush=True)
    st = pd.concat(parts, ignore_index=True)
    cache_csv.parent.mkdir(parents=True, exist_ok=True)
    st.to_csv(cache_csv, index=False, encoding="utf-8")
    served_txt.write_text("\n".join(sorted(served)) + "\n", encoding="utf-8")
    side.write_text(json.dumps(want, indent=1), encoding="utf-8")
    print(f"  tram stop_times: {len(st):,} of {seen:,} rows -> {cache_csv.name}; "
          f"{len(served):,} stop_ids served by some trip")
    return st, served


def norm(s):
    """NFC, dashes to hyphens, whitespace collapsed: the form names are compared in."""
    s = unicodedata.normalize("NFC", str(s))
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def collapse_name(name, marker, case_fold=True):
    """A stop name with its platform marker removed, or None if it has none.

    `marker` is a compiled regex matching the trailing platform marker."""
    n = norm(name)
    m = marker.search(n)
    if not m:
        return None
    base = n[:m.start()].strip(" -,")
    return base


def headways(trips, st, services, start="09:00:00", end="16:00:00"):
    """{line: minutes} - the mean gap between trips leaving their first stop
    between `start` and `end` on the reference date, averaged over directions."""
    t = trips[trips["service_id"].isin(services)]
    s = st[st["trip_id"].isin(set(t["trip_id"]))].copy()
    s["seq"] = s["stop_sequence"].astype(int)
    first = s.sort_values("seq").groupby("trip_id").first()
    first = first.join(t.set_index("trip_id")[["line", "direction_id"]])
    first = first[(first["departure_time"] >= start) & (first["departure_time"] < end)]
    span = (int(end[:2]) - int(start[:2])) * 60
    out = {}
    for line, g in first.groupby("line"):
        per_dir = g.groupby("direction_id").size()
        out[line] = round(span / per_dir.mean(), 1) if len(per_dir) else None
    return out


def write_shapes(z, shape_ids, out_zip):
    """The chosen shapes only, as a one-file GTFS zip for step 3."""
    want, parts = set(shape_ids), []
    for chunk in pd.read_csv(z.open("shapes.txt"), dtype=str, keep_default_na=False,
                             chunksize=CHUNK_ROWS):
        parts.append(chunk[chunk["shape_id"].isin(want)])
    shp = pd.concat(parts, ignore_index=True)
    missing = want - set(shp["shape_id"])
    if missing:
        sys.exit(f"shape(s) {sorted(missing)} not in shapes.txt")
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as out:
        out.writestr("shapes.txt", shp.to_csv(index=False))
    return len(shp)


def shape_lines(z, shape_ids, crs_projected):
    """{shape_id: LineString in `crs_projected`} for the given shapes."""
    import geopandas as gpd
    from shapely.geometry import LineString
    want, parts = set(shape_ids), []
    for chunk in pd.read_csv(z.open("shapes.txt"), dtype=str, keep_default_na=False,
                             chunksize=CHUNK_ROWS):
        parts.append(chunk[chunk["shape_id"].isin(want)])
    shp = pd.concat(parts, ignore_index=True)
    shp["seq"] = shp["shape_pt_sequence"].astype(int)
    out = {}
    for sid, g in shp.sort_values("seq").groupby("shape_id"):
        line = LineString(list(zip(g["shape_pt_lon"].astype(float), g["shape_pt_lat"].astype(float))))
        out[sid] = gpd.GeoSeries([line], crs="EPSG:4326").to_crs(crs_projected).iloc[0]
    return out


def cover_shapes(trips, stations_xy, shapes, tolerance_m):
    """{line: [shape_id, ...]} - each line's most-used shape on the reference
    date first, then, while any of the line's stations is further than
    `tolerance_m` from every chosen shape, the shape that reaches the most of
    them (ties: more trips, then shape_id). A line is often several patterns
    (Antwerp's 7 and 8 each run two; a short working can be the most used),
    and one shape alone left whole stretches undrawn (measured 2026-10-04).

    `stations_xy` is {line: [(name, Point), ...]} in the projected CRS;
    `shapes` is shape_lines()'s output for every candidate."""
    out = {}
    for line, g in trips[trips["shape_id"] != ""].groupby("line"):
        counts = g.groupby("shape_id").size()
        ranked = sorted(counts.index, key=lambda s: (-counts[s], s))
        chosen = [ranked[0]]

        def missing():
            return [n for n, p in stations_xy[line]
                    if min(shapes[s].distance(p) for s in chosen) > tolerance_m]
        todo = missing()
        while todo:
            gain = {s: sum(1 for n, p in stations_xy[line]
                           if n in todo and shapes[s].distance(p) <= tolerance_m)
                    for s in ranked if s not in chosen}
            best = max(gain, key=lambda s: (gain[s], counts[s], s)) if gain else None
            if best is None or gain[best] == 0:
                sys.exit(f"line {line}: no shape reaches {todo} within {tolerance_m:.0f} m")
            chosen.append(best)
            todo = missing()
        out[line] = chosen
    return out


def load_meta():
    return json.loads(FEED_META.read_text(encoding="utf-8")) if FEED_META.exists() else {}
