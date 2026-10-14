"""Milan's tram stops, for step 1: which become stations, which are cut.

ATM's 17 tram routes (config.TRAM_LINES) stop every block or two, so they
take the sub-transit-line filters (docs/sub_transit_line_filters.md), on the
same four rules as Toronto's streetcars (pipeline/toronto/streetcars.py):

  1. a tram stop at a drawn metro station is that station;
  2. each line's two terminals are kept;
  3. a stop where the set of lines changes (a crossing or a junction) is kept;
  4. the rest are thinned to one per half mile along the line's own sequence.

The feed names a stop once for both directions, in lower case, and has no
parent_station: stops of one name are grouped first, then by distance.

Reads the cached feed only. Run alone it prints the result and writes
nothing:  python pipeline/milan/trams.py
"""

import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import stations as station_gates  # noqa: E402
from pipeline.milan import config  # noqa: E402

MILE_M = config.METERS_PER_MILE
# Words the feed's lower-case names keep small in Italian.
SMALL = {"di", "da", "de", "del", "della", "dei", "delle", "degli", "al",
         "alla", "e", "in", "per", "il"}
ABBREV_TAILS = {"za", "le", "so", "go", "ta"}
# A stop the feed names for its metro lines ("stazione centrale m2 m3").
METRO_SUFFIX = re.compile(r"\bm[1-5]\b")
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)


def line_name(key):
    return f"Tram {key}"


def display_name(raw):
    """The feed's "p.za ventiquattro maggio" as "P.za Ventiquattro Maggio".
    Every word takes a capital except the small Italian ones after the first;
    "m1 m3" and "fs" become "M1 M3" and "FS"."""
    text = str(raw).strip()

    def cap(m):
        w = m.group(0)
        before = text[max(0, m.start() - 2):m.start()]
        if w in ("fs", "fn"):
            return w.upper()
        # The second half of "p.za", "v.le", "c.so", "l.go", "p.ta", "p.le".
        if w in ABBREV_TAILS and len(before) == 2 and before[1] == "." and before[0].isalpha():
            return w
        # "d'ancona" is "d'Ancona" unless it opens the name.
        if (w in SMALL or (w == "d" and text[m.end():m.end() + 1] == "'")) and m.start() > 0:
            return w
        return w[0].upper() + w[1:]

    out = TOKEN.sub(cap, text)
    return re.sub(r"\b[md](\d)\b", lambda m: m.group(0).upper(), out)


def _read(z, name, **kw):
    return pd.read_csv(io.TextIOWrapper(z.open(name), encoding="utf-8-sig"), dtype=str, **kw)


def _minutes(hms):
    h, m, _s = hms.split(":")
    return int(h) * 60 + int(m)


def load_feed():
    """Tram trips, their stop times and the stops they use."""
    if not config.GTFS_ZIP.exists():
        sys.exit(f"missing {config.GTFS_ZIP}.\nRun: python pipeline/milan/fetch_sources.py")
    z = zipfile.ZipFile(config.GTFS_ZIP)
    routes = _read(z, "routes.txt")
    tram = routes[routes["route_type"] == "0"]
    feed = set(tram["route_short_name"])
    if feed != set(config.TRAM_LINES):
        sys.exit(f"ATM's tram routes changed.\n  feed only  : {sorted(feed - set(config.TRAM_LINES))}\n"
                 f"  config only: {sorted(set(config.TRAM_LINES) - feed)}\n"
                 f"A route added or withdrawn is a scope decision, not a config edit.")
    line_of = dict(zip(tram["route_id"], tram["route_short_name"]))
    trips = _read(z, "trips.txt", usecols=["route_id", "service_id", "trip_id", "trip_headsign",
                                           "direction_id", "shape_id"])
    trips = trips[trips["route_id"].isin(line_of)].copy()
    trips["line"] = trips["route_id"].map(line_of)
    ids, parts = set(trips["trip_id"]), []
    for chunk in pd.read_csv(io.TextIOWrapper(z.open("stop_times.txt"), encoding="utf-8-sig"),
                             dtype=str, chunksize=500_000,
                             usecols=["trip_id", "stop_id", "stop_sequence", "departure_time",
                                      "pickup_type", "drop_off_type"]):
        parts.append(chunk[chunk["trip_id"].isin(ids)])
    st = pd.concat(parts, ignore_index=True)
    st["seq"] = st["stop_sequence"].astype(int)
    stops = _read(z, "stops.txt").set_index("stop_id")
    cal_dates = _read(z, "calendar_dates.txt")
    info = _read(z, "feed_info.txt").iloc[0]
    span = (info["feed_start_date"], info["surface_end_date"])
    want = tuple(d.replace("-", "") for d in config.TRAM_TIMETABLE)
    if span != want:
        sys.exit(f"The feed's surface timetable runs {span}; config.TRAM_TIMETABLE records {want}. "
                 f"A new edition: re-read the routes on diversion and the 15-minute test "
                 f"(docs/recheck_calendar.md), then update the config and the page's dates.")
    return trips, st, stops, cal_dates


def midday_headways(trips, st, cal_dates):
    """{line: minutes between 10:00-15:00 departures, the busier direction}
    on config.TRAM_HEADWAY_DAY. The feed has no calendar.txt rows."""
    day = cal_dates[(cal_dates["date"] == config.TRAM_HEADWAY_DAY)
                    & (cal_dates["exception_type"] == "1")]
    on = set(day["service_id"])
    first = st.sort_values("seq").groupby("trip_id")["departure_time"].first().map(_minutes)
    t = trips[trips["service_id"].isin(on)].assign(dep=lambda d: d["trip_id"].map(first))
    t = t[(t["dep"] >= 10 * 60) & (t["dep"] < 15 * 60)]
    out = {}
    for line in config.TRAM_LINES:
        n = t[t["line"] == line].groupby("direction_id").size()
        out[line] = 300.0 / n.max() if len(n) else float("inf")
    return out


def group_places(ids, xy, serves, names):
    """stop_id -> place number. Nearest pairs first, same-named pairs before
    any other, and no merge that stretches a place past MAX_SPREAD."""
    n = len(ids)
    d = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1])
    group = {i: [i] for i in range(n)}
    of = list(range(n))
    pairs = sorted((float(d[i, j]), int(i), int(j))
                   for i, j in zip(*np.where(np.triu(d <= config.TRAM_PLACE_MAX_SPREAD_M, 1))))
    pairs.sort(key=lambda p: (names[p[1]] != names[p[2]], p[0]))
    for dist, i, j in pairs:
        a, b = of[i], of[j]
        if a == b:
            continue
        if names[i] != names[j] and (
                dist > config.TRAM_PLACE_CROSS_M
                or (dist > config.TRAM_PLACE_LINK_M and serves[ids[i]] & serves[ids[j]])):
            continue
        both = group[a] + group[b]
        if float(d[np.ix_(both, both)].max()) > config.TRAM_PLACE_MAX_SPREAD_M:
            continue
        group[a] = both
        for k in group.pop(b):
            of[k] = a
    order = {root: k for k, root in enumerate(sorted(group))}
    return {ids[i]: order[of[i]] for i in range(n)}


def build(metro, boundary_geom):
    """metro: the drawn metro stations (station, latitude, longitude).
    boundary_geom: the comune polygon in the projected CRS.

    Returns {"stations": DataFrame(station, latitude, longitude, linee),
    "excluded": [rows for excluded_stations.csv], "shapes": {line: [shape_id]},
    "attached": {metro station: [lines]}, "counts": {...}}."""
    from pyproj import Transformer
    from shapely.geometry import Point

    trips, st, stops, cal_dates = load_feed()
    boardable = station_gates.boardable_stop_ids(st)
    if boardable is not None:
        st = st[st["stop_id"].isin(boardable)]
    unnamed = sorted(s for s in set(st["stop_id"]) if not isinstance(stops.at[s, "stop_name"], str))
    if unnamed:
        # Depot and turning points the feed leaves unnamed are not stops a
        # reader can use.
        print(f"  tram stop ids with no name, left out: {len(unnamed)} {unnamed[:6]}")
        st = st[~st["stop_id"].isin(unnamed)]
    pat = st.sort_values(["trip_id", "seq"]).groupby("trip_id")["stop_id"].agg(tuple)
    trips = trips.assign(pattern=trips["trip_id"].map(pat)).dropna(subset=["pattern"])

    headway = midday_headways(trips, st, cal_dates)
    print(f"\nTrams: weekday midday headway on {config.TRAM_HEADWAY_DAY} (the 15-minute test):")
    slow = []
    for line, h in headway.items():
        mark = "" if h <= config.TRAM_MAX_HEADWAY_MIN else "   FAILS"
        print(f"  {line_name(line):<10}{h:>6.1f} min{mark}")
        if mark:
            slow.append(line)
    if slow:
        sys.exit(f"Tram lines failing the 15-minute test: {slow}. Not drawing one is a scope "
                 f"decision (docs/category_rules.md, station scope).")
    drawn = list(config.TRAM_LINES)

    # --- regular patterns per line -----------------------------------------
    regular = {}      # line -> [(pattern, direction, trips, shape_id)]
    for line in drawn:
        t = trips[trips["line"] == line]
        g = t.groupby(["pattern", "direction_id"]).agg(n=("trip_id", "size"),
                                                      shape=("shape_id", "first")).reset_index()
        keep = g[g["n"] >= config.TRAM_REGULAR_TRIP_SHARE * len(t)]
        regular[line] = [(r.pattern, r.direction_id, int(r.n), r.shape) for r in keep.itertuples()]
    serves = {}
    for line, pats in regular.items():
        for p, direction, _n, _s in pats:
            for sid in p:
                serves.setdefault(sid, set()).add((line, direction))

    # --- places --------------------------------------------------------------
    ids = sorted(serves)
    tr = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    x, y = tr.transform(stops.loc[ids, "stop_lon"].astype(float).values,
                        stops.loc[ids, "stop_lat"].astype(float).values)
    xy = np.column_stack([x, y])
    raw_names = list(stops.loc[ids, "stop_name"])
    lab = group_places(ids, xy, serves, raw_names)
    members = {}
    for i, sid in enumerate(ids):
        members.setdefault(lab[sid], []).append(i)
    mx, my = tr.transform(metro["longitude"].values, metro["latitude"].values)
    mxy = np.column_stack([mx, my])
    mnames = list(metro["station"])

    key_of, pxy, attached_to = {}, {}, {}
    for k, idx in sorted(members.items()):
        d = np.hypot(xy[idx][:, None, 0] - mxy[None, :, 0], xy[idx][:, None, 1] - mxy[None, :, 1])
        j = int(d.min(axis=0).argmin())
        near = float(d.min())
        names = [raw_names[i] for i in idx]
        # "duomo m1 m3" names DUOMO; the metro layer's names are upper case.
        named = any(re.search(rf"\b{re.escape(mnames[j].lower())}\b", nm) or METRO_SUFFIX.search(nm)
                    for nm in names)
        if near <= config.TRAM_ATTACH_M or (named and near <= config.TRAM_ATTACH_NAMED_M):
            key = mnames[j]
            pxy[key] = (float(mxy[j, 0]), float(mxy[j, 1]))
            attached_to[key] = True
        else:
            clean = sorted({display_name(nm) for nm in names}, key=lambda s: (len(s), s))
            key = next((c for c in clean if c not in pxy), None)
            if key is None:
                # A second place of one name (a long square's far side): the
                # name with the feed's stop code keeps the two apart.
                key = f"{clean[0]} ({stops.at[ids[idx[0]], 'stop_code'] or ids[idx[0]]})"
            pxy[key] = (float(xy[idx, 0].mean()), float(xy[idx, 1].mean()))
        for i in idx:
            key_of[ids[i]] = key
    places = set(key_of.values())
    inside = {p for p in places if Point(pxy[p]).within(boundary_geom)}
    lines_of = {p: set() for p in places}
    for sid, sv in serves.items():
        lines_of[key_of[sid]] |= {line for line, _d in sv}
    attached = {p for p in places if p in attached_to}
    print(f"\n  {len(ids)} stop ids on regular patterns -> {len(places)} places: "
          f"{len(attached)} are a drawn metro station, {len(places - inside)} outside the comune")

    # --- sequences: one direction per line, enough patterns to cover it -----
    def place_seq(pattern):
        out = []
        for sid in pattern:
            p = key_of[sid]
            if p in inside and (not out or out[-1] != p):
                out.append(p)
        return out

    chosen, shapes, leftover = {}, {}, {}
    for line, pats in regular.items():
        by_dir = {}
        for p, direction, n, shape in pats:
            by_dir.setdefault(direction, []).append((place_seq(p), n, shape))
        direction = max(by_dir, key=lambda d: max(len(set(s)) for s, _n, _sh in by_dir[d]))
        cand = sorted(by_dir[direction], key=lambda c: (-len(set(c[0])), -c[1]))
        seqs, covered, shp = [], set(), []
        for seq, _n, shape in cand:
            if set(seq) - covered:
                seqs.append(seq)
                covered |= set(seq)
                shp.append(shape)
        chosen[line], shapes[line] = seqs, shp
        every = set().union(*(set(s) for d in by_dir for s, _n, _sh in by_dir[d]))
        leftover[line] = every - covered

    # --- the interchange rule: a crossing or a junction ----------------------
    changes = set()
    for seqs in chosen.values():
        for seq in seqs:
            for i, p in enumerate(seq):
                around = [seq[j] for j in (i - 1, i + 1) if 0 <= j < len(seq)]
                # The stop that HAS a line its neighbour lacks.
                if any(lines_of[p] - lines_of[q] for q in around):
                    changes.add(p)
    spacing_m = config.TRAM_THIN_SPACING_MILES * MILE_M

    def gap_m(p, q):
        return float(np.hypot(pxy[q][0] - pxy[p][0], pxy[q][1] - pxy[p][1]))

    def run(interchange):
        kept, cuts = set(), []
        for line, seqs in chosen.items():
            k, c = station_gates.thin(seqs, pxy, spacing_m=spacing_m,
                                      keep_always=attached, interchange=interchange)
            kept |= k
            cuts += [{**q, "line": line} for q in c]
        # One-way stops the chosen direction never reaches: straight-line
        # spacing from what is already kept.
        for line in drawn:
            for p in sorted(leftover[line] - kept):
                near = min(kept, key=lambda q: gap_m(p, q))
                if gap_m(p, near) >= spacing_m:
                    kept.add(p)
                else:
                    cuts.append({"station": p, "nearest_kept": near, "metres_since_kept": gap_m(p, near),
                                 "line": line, "one_way": True})
        return kept, [c for c in cuts if c["station"] not in kept]

    shared = {p for p in inside if len(lines_of[p]) >= 2}
    kept_a, _ = run(shared)
    kept, cuts = run(changes)
    # Two kept stops closer than the attach distance are one station to a
    # reader: the one on fewer lines goes, then the later name.
    ranked = sorted(kept - attached, key=lambda p: (-len(lines_of[p]), p))
    for i, p in enumerate(ranked):
        for q in ranked[:i]:
            if q in kept and gap_m(p, q) < config.TRAM_ATTACH_M:
                kept.discard(p)
                cuts.append({"station": p, "nearest_kept": q, "metres_since_kept": gap_m(p, q),
                             "line": sorted(lines_of[p], key=int)[0], "one_way": True})
                break
    print(f"  one-way places off the chosen direction: {len(set().union(*leftover.values()))}")
    print(f"  kept if every stop shared by 2+ lines stays: {len(kept_a - attached)} new stations "
          f"({len(shared)} shared places)")
    print(f"  kept with the crossing-or-junction rule:     {len(kept - attached)} new stations "
          f"({len(changes)} crossings and junctions)  <- used")

    new = sorted(kept - attached)
    back = Transformer.from_crs(config.CRS_PROJECTED, config.CRS_GEOGRAPHIC, always_xy=True)
    lon, lat = back.transform([pxy[p][0] for p in new], [pxy[p][1] for p in new])

    def lines_text(p):
        return ", ".join(line_name(k) for k in sorted(lines_of[p], key=int))

    stations = pd.DataFrame({"station": new, "latitude": np.round(lat, 6), "longitude": np.round(lon, 6),
                             "linee": [lines_text(p) for p in new]})
    excluded, seen = [], set()
    for c in sorted(cuts, key=lambda c: (c["station"], int(c["line"]))):
        p = c["station"]
        if p in seen or p in attached:
            continue
        seen.add(p)
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        miles = round(c["metres_since_kept"] / MILE_M, 3)
        how = "from" if c.get("one_way") else "after"
        excluded.append({"station": p, "latitude": round(la, 6), "longitude": round(lo, 6),
                         "lines": lines_text(p),
                         # "spacing filter" is what app/station_scope.py reads.
                         "reason": f"spacing filter on {line_name(c['line'])}: {miles} mi {how} "
                                   f"{c['nearest_kept']}, under {config.TRAM_THIN_SPACING_MILES} mi"})
    outside = sorted(places - inside)
    for p in outside:
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        excluded.append({"station": p, "latitude": round(la, 6), "longitude": round(lo, 6),
                         "lines": lines_text(p),
                         "reason": "outside the Comune di Milano boundary"})

    print("\n  per line: places inside the comune, kept as stations (new or a metro station), cut")
    for line in drawn:
        mine = {p for p in inside if line in lines_of[p]}
        print(f"    {line_name(line):<10}{len(mine):>4}{len(mine & kept):>5}{len(mine - kept):>5}"
              f"   {len(chosen[line])} sequence(s), {len(shapes[line])} shape(s)")
    return {"stations": stations, "excluded": excluded, "shapes": shapes,
            "attached": {p: sorted(lines_of[p], key=int) for p in sorted(attached)},
            "counts": {"tram_places": len(places), "tram_stations_new": len(new),
                       "tram_places_at_metro_stations": len(attached),
                       "tram_stops_thinned": len(seen), "tram_places_outside": len(outside)}}


if __name__ == "__main__":
    import geopandas as gpd

    sys.stdout.reconfigure(encoding="utf-8")
    b = gpd.GeoDataFrame.from_features(
        json.loads(config.BOUNDARY_GEOJSON.read_text(encoding="utf-8"))["features"],
        crs=config.CRS_GEOGRAPHIC)
    # DRY RUN ONLY, AND STALE SINCE THE LANDING: stations.csv now holds the
    # tram stations too, so this feeds them back in as metro stations.
    # Step 1 passes the metro set itself and is the figure to trust.
    built = pd.read_csv(config.DATA_PROCESSED / "stations.csv")
    res = build(built, b.to_crs(config.CRS_PROJECTED).union_all())
    print(f"\n{res['counts']}\nattached: {res['attached']}")
    print(res["stations"].to_string())
    for row in res["excluded"][:12]:
        print(row["station"], "|", row["reason"])
