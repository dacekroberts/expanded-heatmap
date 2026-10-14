"""Prague's tram stops, for step 1: which become stations, which are cut.

PID's day tram routes (config.TRAM_LINES) stop every block or two, so they
take the sub-transit-line filters (docs/sub_transit_line_filters.md), on the
same four rules as Toronto's streetcars and Milan's trams
(pipeline/toronto/streetcars.py, pipeline/milan/trams.py):

  1. a tram stop at a drawn metro station is that station;
  2. each line's two terminals are kept;
  3. a stop where the set of lines changes (a crossing or a junction) is kept;
  4. the rest are thinned to one per half mile along the line's own sequence.

PID names a stop once for all its platforms, so a place is a stop name. A
node (`asw_node_id`) is not a place: node 1040 holds both Anděl and Na
Knížecí.

Reads the cached feed only. Run alone it prints the result and writes
nothing:  python pipeline/prague/trams.py
"""

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import stations as station_gates  # noqa: E402
from pipeline.prague import config  # noqa: E402

MILE_M = config.METERS_PER_MILE


def line_name(key):
    return f"Tram {key}"


def _read(z, name, **kw):
    return pd.read_csv(io.TextIOWrapper(z.open(name), encoding="utf-8-sig"), dtype=str, **kw)


def _minutes(hms):
    h, m, _s = hms.split(":")
    return int(h) * 60 + int(m)


def load_feed():
    """Day tram trips, their stop times, the stops they use and the services
    running on config.TRAM_HEADWAY_DAY."""
    if not config.TRAM_GTFS_ZIP.exists():
        sys.exit(f"missing {config.TRAM_GTFS_ZIP}.\nRun: python pipeline/prague/fetch_sources.py")
    z = zipfile.ZipFile(config.TRAM_GTFS_ZIP)
    info = _read(z, "feed_info.txt").iloc[0]
    span = (info["feed_start_date"], info["feed_end_date"])
    if span != config.TRAM_FEED_WINDOW:
        sys.exit(f"The tram feed runs {span}; config.TRAM_FEED_WINDOW records "
                 f"{config.TRAM_FEED_WINDOW}. A new edition: re-read which routes run and the "
                 f"15-minute test, then update the config and the page's dates.")
    routes = _read(z, "routes.txt")
    tram = routes[(routes["route_type"] == "0") & (routes["is_night"] != "1")]
    feed = set(tram["route_short_name"])
    known = set(config.TRAM_LINES) | set(config.TRAM_NOT_DRAWN)
    if feed != known:
        sys.exit(f"PID's day tram routes changed.\n  feed only  : {sorted(feed - known)}\n"
                 f"  config only: {sorted(known - feed)}\n"
                 f"A route added or withdrawn is a scope decision, not a config edit.")
    line_of = dict(zip(tram["route_id"], tram["route_short_name"]))
    trips = _read(z, "trips.txt", usecols=["route_id", "service_id", "trip_id", "direction_id",
                                           "shape_id"])
    trips = trips[trips["route_id"].isin(line_of)].copy()
    trips["line"] = trips["route_id"].map(line_of)
    ids, parts = set(trips["trip_id"]), []
    for chunk in pd.read_csv(io.TextIOWrapper(z.open("stop_times.txt"), encoding="utf-8-sig"),
                             dtype=str, chunksize=1_000_000,
                             usecols=["trip_id", "stop_id", "stop_sequence", "departure_time",
                                      "pickup_type", "drop_off_type"]):
        parts.append(chunk[chunk["trip_id"].isin(ids)])
    st = pd.concat(parts, ignore_index=True)
    st["seq"] = st["stop_sequence"].astype(int)
    stops = _read(z, "stops.txt").set_index("stop_id")
    day = config.TRAM_HEADWAY_DAY
    cal, cd = _read(z, "calendar.txt"), _read(z, "calendar_dates.txt")
    weekday = pd.Timestamp(day).day_name().lower()
    on = set(cal[(cal[weekday] == "1") & (cal["start_date"] <= day)
                 & (cal["end_date"] >= day)]["service_id"])
    ex = cd[cd["date"] == day]
    on |= set(ex[ex["exception_type"] == "1"]["service_id"])
    on -= set(ex[ex["exception_type"] == "2"]["service_id"])
    return trips, st, stops, on


def midday_headways(trips, st, on):
    """{line: minutes between 10:00-15:00 departures, the busier direction}
    on config.TRAM_HEADWAY_DAY."""
    first = st.sort_values("seq").groupby("trip_id")["departure_time"].first().map(_minutes)
    t = trips[trips["service_id"].isin(on)].assign(dep=lambda d: d["trip_id"].map(first))
    t = t[(t["dep"] >= 10 * 60) & (t["dep"] < 15 * 60)]
    out = {}
    for line in list(config.TRAM_LINES) + list(config.TRAM_NOT_DRAWN):
        n = t[t["line"] == line].groupby("direction_id").size()
        out[line] = 300.0 / n.max() if len(n) else float("inf")
    return out


def build(metro, boundary_geom):
    """metro: the drawn metro stations (station, latitude, longitude).
    boundary_geom: the city polygon in the projected CRS.

    Returns {"stations": DataFrame(stop_id, station, lines, latitude,
    longitude), "excluded": [rows for excluded_stations.csv],
    "shapes": {line: [shape_id]}, "attached": {metro station: [lines]},
    "counts": {...}}."""
    from pyproj import Transformer
    from shapely.geometry import Point

    trips, st, stops, on = load_feed()
    boardable = station_gates.boardable_stop_ids(st)
    if boardable is not None:
        st = st[st["stop_id"].isin(boardable)]
    pat = st.sort_values(["trip_id", "seq"]).groupby("trip_id")["stop_id"].agg(tuple)
    trips = trips.assign(pattern=trips["trip_id"].map(pat)).dropna(subset=["pattern"])

    headway = midday_headways(trips, st, on)
    print(f"\nTrams: weekday midday headway on {config.TRAM_HEADWAY_DAY} (the 15-minute test):")
    wrong = []
    for line, h in headway.items():
        drawn_line = line in config.TRAM_LINES
        passes = h <= config.TRAM_MAX_HEADWAY_MIN
        note = "" if drawn_line and passes else ("   not drawn" if not drawn_line else "   FAILS")
        print(f"  {line_name(line):<10}{h:>6.1f} min{note}")
        if drawn_line != passes:
            wrong.append(line)
    if wrong:
        sys.exit(f"Tram lines on the wrong side of the 15-minute test: {wrong}. Drawing or "
                 f"dropping one is a scope decision (docs/category_rules.md, station scope).")
    drawn = list(config.TRAM_LINES)
    trips = trips[trips["line"].isin(drawn)]

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

    # --- places: one per stop name --------------------------------------------
    ids = sorted(serves)
    tr = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    x, y = tr.transform(stops.loc[ids, "stop_lon"].astype(float).values,
                        stops.loc[ids, "stop_lat"].astype(float).values)
    xy = np.column_stack([x, y])
    raw_names = list(stops.loc[ids, "stop_name"])
    members = {}
    for i, nm in enumerate(raw_names):
        members.setdefault(nm, []).append(i)
    name_of = {nm: nm for nm in members}
    wide = {nm: round(float(np.hypot(xy[idx][:, None, 0] - xy[idx][None, :, 0],
                                     xy[idx][:, None, 1] - xy[idx][None, :, 1]).max()))
            for nm, idx in members.items()}
    wide = {nm: w for nm, w in wide.items() if w > config.TRAM_PLACE_MAX_SPREAD_M}
    if set(wide) != set(config.TRAM_WIDE_PLACES):
        sys.exit(f"tram stops of one name more than {config.TRAM_PLACE_MAX_SPREAD_M:.0f} m apart: "
                 f"{wide}; config.TRAM_WIDE_PLACES has {sorted(config.TRAM_WIDE_PLACES)}. "
                 f"Read each on a map before treating it as one place.")
    mx, my = tr.transform(metro["longitude"].values, metro["latitude"].values)
    mxy = np.column_stack([mx, my])
    mnames = list(metro["station"])

    key_of, pxy, node_of, attached = {}, {}, {}, set()
    for n, idx in sorted(members.items()):
        d = np.hypot(xy[idx][:, None, 0] - mxy[None, :, 0], xy[idx][:, None, 1] - mxy[None, :, 1])
        j = int(d.min(axis=0).argmin())
        near = float(d.min())
        named = name_of[n] == mnames[j]
        if near <= config.TRAM_ATTACH_M or (named and near <= config.TRAM_ATTACH_NAMED_M):
            key = mnames[j]
            pxy[key] = (float(mxy[j, 0]), float(mxy[j, 1]))
            attached.add(key)
        else:
            key = name_of[n]
            if key in mnames:
                sys.exit(f"tram stop {key} shares a drawn metro station's name but is "
                         f"{near:.0f} m from it, past {config.TRAM_ATTACH_NAMED_M:.0f} m")
            pxy[key] = (float(xy[idx, 0].mean()), float(xy[idx, 1].mean()))
            node_of[key] = "T" + ids[idx[0]]
        for i in idx:
            key_of[ids[i]] = key
    places = set(key_of.values())
    inside = {p for p in places if Point(pxy[p]).within(boundary_geom)}
    lines_of = {p: set() for p in places}
    for sid, sv in serves.items():
        lines_of[key_of[sid]] |= {line for line, _d in sv}
    print(f"\n  {len(ids)} stop ids on regular patterns -> {len(places)} "
          f"places: {len(attached)} are a drawn metro station, {len(places - inside)} outside "
          f"the city")

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

    stations = pd.DataFrame({"stop_id": [node_of[p] for p in new], "station": new,
                             "lines": [lines_text(p) for p in new],
                             "latitude": np.round(lat, 6), "longitude": np.round(lon, 6)})
    excluded, seen = [], set()
    for c in sorted(cuts, key=lambda c: (c["station"], int(c["line"]))):
        p = c["station"]
        if p in seen or p in attached:
            continue
        seen.add(p)
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        miles = round(c["metres_since_kept"] / MILE_M, 3)
        how = "from" if c.get("one_way") else "after"
        excluded.append({"station": p, "lines": lines_text(p),
                         # "spacing filter" is what app/station_scope.py reads.
                         "reason": f"spacing filter on {line_name(c['line'])}: {miles} mi {how} "
                                   f"{c['nearest_kept']}, under {config.TRAM_THIN_SPACING_MILES} mi",
                         "latitude": round(la, 6), "longitude": round(lo, 6)})
    outside = sorted(places - inside)
    for p in outside:
        lo, la = back.transform(pxy[p][0], pxy[p][1])
        excluded.append({"station": p, "lines": lines_text(p),
                         "reason": f"outside obec {config.OBEC} (Praha)",
                         "latitude": round(la, 6), "longitude": round(lo, 6)})

    print("\n  per line: places inside the city, kept as stations (new or a metro station), cut")
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

    from pipeline.prague.boundary import city_polygon

    sys.stdout.reconfigure(encoding="utf-8")
    poly = gpd.GeoSeries([city_polygon(verbose=False)], crs=config.CRS_GEOGRAPHIC)
    # DRY RUN ONLY, AND STALE SINCE THE LANDING: stations.csv now holds the
    # tram stations too, so this feeds them back in as metro stations.
    # Step 1 passes the metro set itself and is the figure to trust.
    built = pd.read_csv(config.DATA_PROCESSED / "stations.csv")
    res = build(built, poly.to_crs(config.CRS_PROJECTED).iloc[0])
    print(f"\n{res['counts']}\nattached: {res['attached']}")
    print(res["stations"].to_string())
    for row in res["excluded"][:12]:
        print(row["station"], "|", row["reason"])
