"""Toronto's streetcar stops, for step 1: which become stations, which are cut.

The TTC's day streetcar routes (config.STREETCAR_LINES) stop every block or
two, so they take the sub-transit-line filters
(docs/sub_transit_line_filters.md), as Amsterdam's trams do:

  1. a streetcar stop at a drawn rapid-transit station is that station;
  2. each line's two terminals are kept;
  3. a stop where the set of lines changes (a crossing or a junction) is kept;
  4. the rest are thinned to one per half mile along the line's own sequence.

Filter 3 is narrower than "shared by two or more lines": 503, 504 and 508
share King Street for kilometres, and keeping every shared stop there would
thin nothing (build() prints both counts).

The feed names stops per direction and has no parent_station, so stops are
grouped into places by distance first (config, "Streetcars").

Reads the cached feed only. Run alone it prints the result and writes
nothing:  python pipeline/toronto/streetcars.py
"""

import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import stations as station_gates  # noqa: E402
from pipeline.toronto import config  # noqa: E402

MILE_M = config.METERS_PER_MILE
SIDE = re.compile(r"\s+(East|West|North|South) Side\b")


def _read(z, name, **kw):
    with z.open(name) as f:
        return pd.read_csv(f, dtype=str, **kw)


def _minutes(hms):
    h, m, _s = hms.split(":")
    return int(h) * 60 + int(m)


def load_feed():
    """Day streetcar trips, their stop times and the stops they use."""
    z = zipfile.ZipFile(config.GTFS_ZIP)
    routes = _read(z, "routes.txt")
    sc = routes[(routes["route_type"] == config.LRT_ROUTE_TYPE)
                & ~routes["route_long_name"].fillna("").str.match(config.LRT_NAME_REGEX)]
    feed = set(sc["route_short_name"])
    want = set(config.STREETCAR_LINES) | set(config.STREETCAR_NIGHT_NOT_DRAWN)
    if feed != want:
        sys.exit(f"The TTC's streetcar routes changed.\n  feed only  : {sorted(feed - want)}\n"
                 f"  config only: {sorted(want - feed)}\n"
                 f"A route added or withdrawn is a scope decision, not a config edit.")
    day = sc[sc["route_short_name"].isin(config.STREETCAR_LINES)]
    line_of = dict(zip(day["route_id"], day["route_short_name"]))
    trips = _read(z, "trips.txt", usecols=["route_id", "service_id", "trip_id", "trip_headsign",
                                           "direction_id", "shape_id"])
    trips = trips[trips["route_id"].isin(line_of)].copy()
    trips["line"] = trips["route_id"].map(line_of)
    # The feed files replacement BUS trips under the streetcar's route id
    # ("506B Carlton Replacement Bus", 1,010 of 506's 2,025 trips on
    # 2026-10-13), on streets the streetcar does not run. Not the line.
    bus = trips["trip_headsign"].fillna("").str.contains(config.STREETCAR_BUS_HEADSIGN)
    if bus.any():
        print("  replacement bus trips left out: "
              + ", ".join(f"{k} {n}" for k, n in trips[bus].groupby("line").size().items()))
    trips = trips.assign(bus=bus)
    ids, parts = set(trips["trip_id"]), []
    with z.open("stop_times.txt") as f:
        for chunk in pd.read_csv(f, dtype=str, chunksize=1_000_000,
                                 usecols=["trip_id", "stop_id", "stop_sequence", "departure_time",
                                          "pickup_type", "drop_off_type"]):
            parts.append(chunk[chunk["trip_id"].isin(ids)])
    st = pd.concat(parts, ignore_index=True)
    st["seq"] = st["stop_sequence"].astype(int)
    stops = _read(z, "stops.txt").set_index("stop_id")
    cal = _read(z, "calendar.txt")
    cal_dates = _read(z, "calendar_dates.txt")
    return trips, st, stops, cal, cal_dates


def midday_headways(trips, st, cal, cal_dates):
    """{line: minutes between weekday 09:00-15:00 departures, the busier
    direction} on the first Wednesday a full week into the feed."""
    start = pd.to_datetime(cal["start_date"]).min() + pd.Timedelta(days=7)
    day = start + pd.Timedelta(days=(2 - start.weekday()) % 7)
    stamp = day.strftime("%Y%m%d")
    on = set(cal.loc[(cal["wednesday"] == "1") & (cal["start_date"] <= stamp)
                     & (cal["end_date"] >= stamp), "service_id"])
    ex = cal_dates[cal_dates["date"] == stamp]
    on |= set(ex.loc[ex["exception_type"] == "1", "service_id"])
    on -= set(ex.loc[ex["exception_type"] == "2", "service_id"])
    first = st.sort_values("seq").groupby("trip_id")["departure_time"].first().map(_minutes)
    t = trips[trips["service_id"].isin(on)].assign(dep=lambda d: d["trip_id"].map(first))
    t = t[(t["dep"] >= 9 * 60) & (t["dep"] < 15 * 60)]
    out = {}
    for line in sorted(set(trips["line"])):
        n = t[t["line"] == line].groupby("direction_id").size()
        out[line] = 360.0 / n.max() if len(n) else float("inf")
    return stamp, out


def group_places(ids, xy, serves, names):
    """stop_id -> place number. Single linkage: within PLACE_LINK_M, or within
    PLACE_CROSS_M when the two stops share no line-and-direction."""
    n = len(ids)
    d = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1])
    group = {i: [i] for i in range(n)}
    of = list(range(n))
    pairs = sorted((float(d[i, j]), int(i), int(j))
                   for i, j in zip(*np.where(np.triu(d <= config.STREETCAR_PLACE_MAX_SPREAD_M, 1))))
    # Nearest pairs first, and a merge that would stretch a place past the
    # cap is refused: plain single linkage chained three intersections along
    # Queens Quay into one place 355 m across.
    # Same-named pairs first, so a neighbour cannot take one platform away.
    pairs.sort(key=lambda p: (names[p[1]] != names[p[2]], p[0]))
    for dist, i, j in pairs:
        a, b = of[i], of[j]
        if a == b:
            continue
        # Two stops of one name are one place whatever serves them (the two
        # platforms of Exhibition Loop, 145 m apart).
        if names[i] != names[j] and (
                dist > config.STREETCAR_PLACE_CROSS_M
                or (dist > config.STREETCAR_PLACE_LINK_M and serves[ids[i]] & serves[ids[j]])):
            continue
        both = group[a] + group[b]
        if float(d[np.ix_(both, both)].max()) > config.STREETCAR_PLACE_MAX_SPREAD_M:
            continue
        group[a] = both
        for k in group.pop(b):
            of[k] = a
    order = {root: k for k, root in enumerate(sorted(group))}
    return {ids[i]: order[of[i]] for i in range(n)}


def build(rapid, boundary_geom, crs_geographic=None):
    """rapid: the drawn rapid-transit stations (station, latitude, longitude).
    boundary_geom: the city polygon in the projected CRS.

    Returns {"stations": DataFrame(station, latitude, longitude, lines),
    "excluded": [rows for excluded_stations.csv], "shapes": {line: [shape_id]},
    "attached": {rapid station: [lines]}, "counts": {...}}."""
    from pyproj import Transformer
    from shapely.geometry import Point

    all_trips, st, stops, cal, cal_dates = load_feed()
    boardable = station_gates.boardable_stop_ids(st)
    if boardable is not None:
        st = st[st["stop_id"].isin(boardable)]
    pat = st.sort_values(["trip_id", "seq"]).groupby("trip_id")["stop_id"].agg(tuple)
    all_trips = all_trips.assign(pattern=all_trips["trip_id"].map(pat)).dropna(subset=["pattern"])
    trips, bus_trips = all_trips[~all_trips["bus"]], all_trips[all_trips["bus"]]
    feed_end = cal["end_date"].max()
    feed_end = f"{feed_end[:4]}-{feed_end[4:6]}-{feed_end[6:]}"

    # --- which lines run as streetcars, and often enough ---------------------
    # Both sets are the owner's (2026-10-13) and are compared with the feed,
    # so a line that comes back, or stops, stops the build until config
    # follows it.
    closed = set(config.STREETCAR_LINES) - set(trips["line"])
    if closed != set(config.STREETCAR_CLOSED_FOR_WORKS):
        sys.exit(f"Streetcar lines with no streetcar trip in this feed: {sorted(closed)}; config "
                 f"records {sorted(config.STREETCAR_CLOSED_FOR_WORKS)} as closed for works. "
                 f"A line returning or closing is a scope decision.")
    stamp, headway = midday_headways(trips, st, cal, cal_dates)
    print(f"\nStreetcars: weekday midday headway on {stamp} (the 15-minute test):")
    slow = set()
    for line, h in headway.items():
        mark = "" if h <= config.STREETCAR_MAX_HEADWAY_MIN else "   FAILS"
        print(f"  {config.STREETCAR_LEGEND_NAMES[line]:<28}{h:>6.1f} min{mark}")
        if mark:
            slow.add(line)
    for line in sorted(closed):
        print(f"  {config.STREETCAR_LEGEND_NAMES[line]:<28}replacement buses only, to {feed_end}")
    if slow != set(config.STREETCAR_INFREQUENT):
        sys.exit(f"Streetcar lines failing the 15-minute test: {sorted(slow)}; config records "
                 f"{sorted(config.STREETCAR_INFREQUENT)}. A scope decision.")
    drawn = [k for k in config.STREETCAR_LINES if k not in closed and k not in slow]

    # --- regular patterns per line -----------------------------------------
    def regular_patterns(t):
        g = t.groupby(["pattern", "direction_id"]).agg(n=("trip_id", "size"),
                                                      shape=("shape_id", "first")).reset_index()
        return g[g["n"] >= config.STREETCAR_REGULAR_TRIP_SHARE * len(t)]

    regular = {}      # line -> [(pattern, direction, trips, shape_id)]
    for line in drawn:
        t = trips[trips["line"] == line]
        keep = regular_patterns(t)
        regular[line] =[(r.pattern, r.direction_id, int(r.n), r.shape) for r in keep.itertuples()]
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
    lab = group_places(ids, xy, serves, list(stops.loc[ids, "stop_name"]))
    members = {}
    for i, sid in enumerate(ids):
        members.setdefault(lab[sid], []).append(i)
    rx, ry = tr.transform(rapid["longitude"].values, rapid["latitude"].values)
    rxy = np.column_stack([rx, ry])
    rnames = list(rapid["station"])

    key_of, pxy, attached_to = {}, {}, {}
    for k, idx in members.items():
        d = np.hypot(xy[idx][:, None, 0] - rxy[None, :, 0], xy[idx][:, None, 1] - rxy[None, :, 1])
        j = int(d.min(axis=0).argmin())
        near = float(d.min())
        names = [stops.at[ids[i], "stop_name"] for i in idx]
        named = any(rnames[j] in nm for nm in names)
        if near <= config.STREETCAR_ATTACH_M or (named and near <= config.STREETCAR_ATTACH_NAMED_M):
            key = rnames[j]
            pxy[key] = (float(rxy[j, 0]), float(rxy[j, 1]))
            attached_to[key] = True
        else:
            clean = sorted({SIDE.sub("", nm).strip() for nm in names}, key=lambda s: (len(s), s))
            key = clean[0]
            # Two places with one cleaned name: take the next name not in use.
            # the feed's own side-of-street name last.
            key = next((c for c in clean + sorted(names) if c not in pxy), None)
            if key is None:
                sys.exit(f"streetcar places share every name: {clean}")
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
          f"{len(attached)} are a drawn rapid-transit station, "
          f"{len(places - inside)} outside the city")

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

    # --- the interchange rule, both ways, so the choice is measured ---------
    shared = {p for p in inside if len(lines_of[p]) >= 2}
    changes = set()
    for seqs in chosen.values():
        for seq in seqs:
            for i, p in enumerate(seq):
                around = [seq[j] for j in (i - 1, i + 1) if 0 <= j < len(seq)]
                # The stop that HAS a line its neighbour lacks: the crossing
                # itself, or the last shared stop before two lines part.
                if any(lines_of[p] - lines_of[q] for q in around):
                    changes.add(p)

    def run(interchange):
        kept, cuts = set(), []
        for line, seqs in chosen.items():
            k, c = station_gates.thin(seqs, pxy, spacing_m=config.STREETCAR_THIN_SPACING_MILES * MILE_M,
                                      keep_always=attached, interchange=interchange)
            kept |= k
            cuts += [{**q, "line": line} for q in c]
        # One-way stops the chosen direction never reaches: straight-line
        # spacing from what is already kept.
        for line in drawn:
            for p in sorted(leftover[line] - kept):
                near = min(kept, key=lambda q: np.hypot(pxy[q][0] - pxy[p][0], pxy[q][1] - pxy[p][1]))
                gap = float(np.hypot(pxy[near][0] - pxy[p][0], pxy[near][1] - pxy[p][1]))
                if gap >= config.STREETCAR_THIN_SPACING_MILES * MILE_M:
                    kept.add(p)
                else:
                    cuts.append({"station": p, "nearest_kept": near, "metres_since_kept": gap,
                                 "line": line, "one_way": True})
        return kept, [c for c in cuts if c["station"] not in kept]

    kept_a, _ = run(shared)
    kept, cuts = run(changes)
    # Two kept stops closer than the attach distance are one station to a
    # reader (Dufferin Gate Loop and the stop 68 m outside it, one the end of
    # each 504 pattern): the one on fewer lines goes, then the later name.
    ranked = sorted(kept - attached, key=lambda p: (-len(lines_of[p]), p))
    for i, p in enumerate(ranked):
        for q in ranked[:i]:
            gap = float(np.hypot(pxy[q][0] - pxy[p][0], pxy[q][1] - pxy[p][1]))
            if q in kept and gap < config.STREETCAR_ATTACH_M:
                kept.discard(p)
                cuts.append({"station": p, "nearest_kept": q, "metres_since_kept": gap,
                             "line": sorted(lines_of[p])[0], "one_way": True})
                break
    n_left = len(set().union(*leftover.values()))
    print(f"  one-way places off the chosen direction: {n_left}")
    print(f"  kept if every stop shared by 2+ lines stays: {len(kept_a - attached)} new stations "
          f"({len(shared)} shared places)")
    print(f"  kept with the crossing-or-junction rule:     {len(kept - attached)} new stations "
          f"({len(changes)} crossings and junctions)  <- used")

    new = sorted(kept - attached)
    back = Transformer.from_crs(config.CRS_PROJECTED, config.CRS_GEOGRAPHIC, always_xy=True)
    lon, lat = back.transform([pxy[p][0] for p in new], [pxy[p][1] for p in new])

    def lines_text(p):
        return ", ".join(config.STREETCAR_LINE_NAMES[k] for k in sorted(lines_of[p]))

    stations = pd.DataFrame({"station": new, "latitude": np.round(lat, 6), "longitude": np.round(lon, 6),
                             "lines": [lines_text(p) for p in new]})
    excluded, seen = [], set()
    for c in sorted(cuts, key=lambda c: (c["station"], c["line"])):
        p = c["station"]
        if p in seen:
            continue
        seen.add(p)
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        miles = round(c["metres_since_kept"] / MILE_M, 3)
        how = "from" if c.get("one_way") else "after"
        excluded.append({"station": p, "latitude": round(la, 6), "longitude": round(lo, 6),
                         "lines": lines_text(p),
                         # "spacing filter" is what app/station_scope.py reads.
                         "reason": f"spacing filter on {config.STREETCAR_LINE_NAMES[c['line']]}: "
                                   f"{miles} mi {how} {c['nearest_kept']}, under "
                                   f"{config.STREETCAR_THIN_SPACING_MILES} mi"})
    for p in sorted(places - inside):
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        excluded.append({"station": p, "latitude": round(la, 6), "longitude": round(lo, 6),
                         "lines": lines_text(p),
                         "reason": f"outside the City of Toronto, "
                                   f"{round(Point(pxy[p]).distance(boundary_geom))} m beyond the boundary"})

    # --- stops of the lines and stretches not drawn ---------------------------
    # A stop within NOT_DRAWN_NEAR_M of a drawn line's stop is that line's
    # stop too and gets no row. The closed stretches are read from the
    # replacement bus trips, kept to the streets the streetcar runs.
    used = xy

    def rows_for(t, line, reason, streets=None):
        out, got = [], set()
        for r in regular_patterns(t).itertuples():
            for sid in r.pattern:
                name = SIDE.sub("", stops.at[sid, "stop_name"]).strip()
                if name in got or (streets and not name.startswith(tuple(streets))):
                    continue
                px, py = tr.transform(float(stops.at[sid, "stop_lon"]), float(stops.at[sid, "stop_lat"]))
                if np.hypot(used[:, 0] - px, used[:, 1] - py).min() <= config.STREETCAR_NOT_DRAWN_NEAR_M:
                    continue
                if not Point(px, py).within(boundary_geom):
                    continue
                got.add(name)
                out.append({"station": name, "latitude": round(float(stops.at[sid, "stop_lat"]), 6),
                            "longitude": round(float(stops.at[sid, "stop_lon"]), 6),
                            "lines": config.STREETCAR_LINE_NAMES[line], "reason": reason})
        return sorted(out, key=lambda r: r["station"])

    not_drawn = {}
    for line, streets in config.STREETCAR_CLOSED_FOR_WORKS.items():
        not_drawn[line] = rows_for(
            bus_trips[bus_trips["line"] == line], line,
            f"closed for works: {config.STREETCAR_LEGEND_NAMES[line]} runs as a replacement bus "
            f"in the timetable to {feed_end}", streets)
    for line, streets in config.STREETCAR_PART_CLOSED.items():
        not_drawn[line] = rows_for(
            bus_trips[bus_trips["line"] == line], line,
            f"closed for works: this stretch of {config.STREETCAR_LEGEND_NAMES[line]} runs as a "
            f"replacement bus in the timetable to {feed_end}", streets)
    for line in config.STREETCAR_INFREQUENT:
        not_drawn[line] = rows_for(
            trips[trips["line"] == line], line,
            f"15-minute test: {config.STREETCAR_LEGEND_NAMES[line]} runs at weekday peaks only")
    for line, rows in not_drawn.items():
        print(f"  not drawn, {config.STREETCAR_LEGEND_NAMES[line]}: {len(rows)} stop(s) of its own recorded")
        excluded += rows

    print("\n  per line: places inside the city, kept as stations (new or a rapid-transit station), cut")
    for line in drawn:
        mine = {p for p in inside if line in lines_of[p]}
        print(f"    {config.STREETCAR_LEGEND_NAMES[line]:<28}{len(mine):>4}{len(mine & kept):>5}"
              f"{len(mine - kept):>5}   {len(chosen[line])} sequence(s), {len(shapes[line])} shape(s)")
    return {"stations": stations, "excluded": excluded, "shapes": shapes, "drawn": drawn,
            "not_drawn": {k: len(v) for k, v in not_drawn.items()},
            "attached": {p: sorted(lines_of[p]) for p in sorted(attached)},
            "counts": {"streetcar_places": len(places), "streetcar_stations_new": len(new),
                       "streetcar_places_at_rapid_stations": len(attached),
                       "streetcar_stops_thinned": len(seen)}}


if __name__ == "__main__":
    import geopandas as gpd

    sys.stdout.reconfigure(encoding="utf-8")
    b = gpd.read_file(config.CITY_BOUNDARY_ZIP)
    b = b.set_crs(config.CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(config.CRS_GEOGRAPHIC)
    # DRY RUN ONLY, AND STALE SINCE THE LANDING: stations.csv now holds the
    # streetcar stations too, so this feeds them back in as rapid transit.
    # Step 1 passes the rapid-transit set itself and is the figure to trust.
    built = config.DATA_PROCESSED / "stations.csv"
    res = build(pd.read_csv(built), b.to_crs(config.CRS_PROJECTED).union_all())
    print(f"\n{res['counts']}\nattached: {res['attached']}")
    print(res["stations"].to_string())
    for row in res["excluded"][:12]:
        print(row["station"], "|", row["reason"])
