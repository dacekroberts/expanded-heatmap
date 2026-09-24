"""Rotterdam step 1: RET's metro and tram stations inside the gemeente.

    python pipeline/rotterdam/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **The feed is national** - the same file Amsterdam reads, copied from its
    cache. RET's rail routes are read out of it; nothing else is touched.
    Line 12, the stadium event service, is named in config.NOT_DRAWN.
  * **A line's stations are its REGULAR ROUTE** - the stops it serves on most
    days of the feed's window - because an operator runs many shapes per line
    (Amsterdam's rule) (short workings, weekend closures, works diversions) and neither the
    most-used shape nor any single date is the network a reader rides.
  * **Trams are thinned** with the sub-transit-line filters
    (docs/sub_transit_line_filters.md), San Francisco's four rules, applied to
    each line's stretch INSIDE the gemeente. Every cut stop is recorded.
  * **Excluded stations are named with their gemeente**, from OSM's own
    neighbouring-gemeente relations (a naming layer only).
  * Step 3's line geometry is written here as a small zip of RET's shapes, so
    step 3 does not parse the national shapes.txt.
"""
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.rotterdam import config  # noqa: E402
from pipeline.rotterdam.boundary import city_polygon  # noqa: E402
from pipeline.baseline import emit  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/rotterdam/fetch_sources.py")
    return path


def haversine_miles(a, b):
    (lat1, lon1), (lat2, lon2) = a, b
    p1, p2 = math.radians(lat1), math.radians(lat2)
    h = (math.sin(math.radians(lat2 - lat1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * 3958.8 * math.asin(math.sqrt(h))


def stop_name(full):
    """The feed's 'Town, Platform name' with the platform suffix rewritten to
    the stop's own name (config.STOP_NAME_PATTERNS), town prefix kept."""
    town, _, name = str(full).rpartition(", ")
    for pat, rep in config.STOP_NAME_PATTERNS:
        name = re.sub(pat, rep, name)
    return f"{town}, {name}" if town else name


def short(key):
    """'Rotterdam, Beurs#0' -> 'Beurs'. The gemeente's own places lose their
    prefix (config.STRIP_PREFIXES); other towns keep theirs."""
    name = key.split("#", 1)[0]
    for p in config.STRIP_PREFIXES:
        if name.startswith(p):
            return name[len(p):]
    return name


def places(stops, used_ids):
    """stop_id -> PLACE key. A stop name can be a street, not a place (Amsterdam's GVB: the
    metro's Jan van Galenstraat and the tram stop of the same name are 1.6 km
    apart), and three tram lines each have a "Prinsengracht" where they cross
    the canal. So each name's platforms are split into places by single-linkage
    distance (LINK_M), and a place wider than COLLAPSE_MAX_SPREAD_M stops the
    build rather than being averaged."""
    q = stops.loc[sorted(used_ids)].copy()
    g = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q["stop_lon"].astype(float),
                                                        q["stop_lat"].astype(float)),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    key = {}
    for name, grp in g.groupby("stop_name"):
        ids, pts = list(grp.index), list(grp.geometry)
        comp = list(range(len(ids)))

        def find(i):
            while comp[i] != i:
                comp[i] = comp[comp[i]]
                i = comp[i]
            return i
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if pts[i].distance(pts[j]) <= config.PLACE_LINK_M:
                    comp[find(i)] = find(j)
        roots = {}
        for i in range(len(ids)):
            roots.setdefault(find(i), []).append(i)
        # Stable numbering: west to east.
        groups = sorted(roots.values(), key=lambda m: min(pts[i].x for i in m))
        for k, members in enumerate(groups):
            spread = max((pts[a].distance(pts[b]) for a in members for b in members), default=0.0)
            if spread > config.COLLAPSE_MAX_SPREAD_M:
                sys.exit(f"{name}: one place {spread:.0f} m across")
            for i in members:
                key[ids[i]] = f"{name}#{k}"
    return key


def load_feed():
    z = zipfile.ZipFile(need(config.GTFS_ZIP, "the national GTFS"))
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    rail = routes[(routes["agency_id"] == config.GTFS_AGENCY_ID)
                  & routes["route_type"].isin(config.ROUTE_TYPES_RAIL)].copy()
    lines = sorted(rail["route_short_name"], key=lambda x: (len(x), x))
    if sorted(lines) != sorted(list(config.LINE_ORDER) + list(config.NOT_DRAWN)):
        sys.exit(f"RET's rail lines changed.\n  feed  : {lines}\n"
                 f"  config: {sorted(list(config.LINE_ORDER) + list(config.NOT_DRAWN))}\n"
                 f"A line added or withdrawn is a scope decision, not a config edit.")
    rail = rail[rail["route_short_name"].isin(config.LINE_ORDER)].copy()
    for _, r in rail[rail["route_type"] == config.METRO_ROUTE_TYPE].iterrows():
        feed = "#" + str(r["route_color"]).lower()
        if feed != config.METRO_FEED_COLOURS[r["route_short_name"]]:
            sys.exit(f"Metro {r['route_short_name']}'s route_color is now {feed}; config "
                     f"records {config.METRO_FEED_COLOURS[r['route_short_name']]}")
    line_of = dict(zip(rail["route_id"], rail["route_short_name"]))
    mode_of = dict(zip(rail["route_short_name"], rail["route_type"]))

    trips = pd.read_csv(z.open("trips.txt"), dtype=str,
                        usecols=["route_id", "service_id", "trip_id", "direction_id", "shape_id"])
    trips = trips[trips["route_id"].isin(line_of)].copy()
    trips["line"] = trips["route_id"].map(line_of)
    ids = set(trips["trip_id"])
    parts = []
    for chunk in pd.read_csv(z.open("stop_times.txt"), dtype=str, chunksize=2_000_000,
                             usecols=["trip_id", "stop_sequence", "stop_id",
                                      "pickup_type", "drop_off_type"]):
        parts.append(chunk[chunk["trip_id"].isin(ids)])
    st = pd.concat(parts, ignore_index=True)
    stops = pd.read_csv(z.open("stops.txt"), dtype=str).set_index("stop_id")
    stops["stop_name"] = stops["stop_name"].map(stop_name)
    cal = pd.read_csv(z.open("calendar_dates.txt"), dtype=str)
    cal = cal[(cal["exception_type"] == "1") & cal["service_id"].isin(set(trips["service_id"]))]
    return z, rail, line_of, mode_of, trips, st, stops, cal


def regular_routes(trips, st, stops, cal):
    """{line: set of stop NAMES it serves on at least the configured share of its days}."""
    days_of = cal.groupby("service_id")["date"].agg(set).to_dict()
    link = st.merge(trips[["trip_id", "line", "service_id"]], on="trip_id")
    link["name"] = link["stop_id"].map(stops["stop_name"])
    regular, report = {}, {}
    for line, g in link.groupby("line"):
        line_days = set().union(*(days_of.get(s, set()) for s in g["service_id"].unique()))
        per = g.groupby("name")["service_id"].agg(
            lambda s: len(set().union(*(days_of.get(x, set()) for x in set(s)))))
        share = per / len(line_days)
        keep = set(share[share >= config.REGULAR_ROUTE_MIN_DAY_SHARE].index)
        regular[line] = keep
        report[line] = (len(line_days), len(share), len(keep))
    return regular, report


def sequences(line, trips, st, stops, regular):
    """Ordered stop-name sequences that together cover the line's regular
    route: trips whose stops are ALL regular, longest first, each kept only if
    it adds a regular stop. Returns (sequences, shape_ids)."""
    t = trips[trips["line"] == line]
    s = st[st["trip_id"].isin(set(t["trip_id"]))].copy()
    s["name"] = s["stop_id"].map(stops["stop_name"])
    s["seq"] = s["stop_sequence"].astype(int)
    pattern = (s.sort_values(["trip_id", "seq"]).groupby("trip_id")["name"].agg(tuple))
    shape_of = t.set_index("trip_id")["shape_id"]
    counts = pattern.value_counts()
    ok = [p for p in counts.index if set(p) <= regular]
    ok.sort(key=lambda p: (-len(set(p)), -counts[p]))
    chosen, covered, shapes = [], set(), []
    for p in ok:
        if set(p) - covered:
            chosen.append(list(p))
            covered |= set(p)
            trip = pattern[pattern == p].index[0]
            if pd.notna(shape_of.get(trip)):
                shapes.append(shape_of[trip])
        if covered >= regular:
            break
    missing = regular - covered
    if missing:
        sys.exit(f"{config.LINE_NAMES[line]}: no all-regular trip reaches {sorted(missing)}")
    return chosen, shapes


def thin(line, seqs, inside_names, keep_always, interchange, coords):
    """San Francisco's four filters on one line's in-gemeente stretch."""
    kept, cut = set(), []
    for seq in seqs:
        seq = [n for n in seq if n in inside_names]
        if not seq:
            continue
        mark = [n in keep_always or n in interchange for n in seq]
        mark[0] = mark[-1] = True                          # the in-gemeente terminals
        since, last = 0.0, seq[0]
        for i in range(1, len(seq)):
            since += haversine_miles(coords[seq[i - 1]], coords[seq[i]])
            if mark[i]:
                since, last = 0.0, seq[i]
            elif since >= config.THIN_SPACING_MILES:
                mark[i], since, last = True, 0.0, seq[i]
            else:
                cut.append({"station": seq[i], "line": config.LINE_NAMES[line],
                            "nearest_kept": last, "miles_since_kept": round(since, 3)})
        kept |= {n for n, m in zip(seq, mark) if m}
    return kept, [c for c in cut if c["station"] not in kept]


def neighbour_polygons():
    els = json.loads(need(config.OSM_NEIGHBOURS_JSON, "the neighbouring gemeenten")
                     .read_text(encoding="utf-8"))["elements"]
    rows = []
    for rel in els:
        lines = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel.get("members", [])
                 if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")]
        if lines:
            rows.append({"name": rel["tags"].get("name"),
                         "code": rel["tags"].get("ref:gemeentecode"),
                         "geometry": unary_union(list(polygonize(linemerge(MultiLineString(lines)))))})
    return gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)


def write_shapes(z, shape_ids):
    """RET's chosen shapes only, as a one-file GTFS zip for step 3."""
    want, parts = set(shape_ids), []
    for chunk in pd.read_csv(z.open("shapes.txt"), dtype=str, chunksize=2_000_000):
        parts.append(chunk[chunk["shape_id"].isin(want)])
    shp = pd.concat(parts, ignore_index=True)
    buf = io.StringIO()
    shp.to_csv(buf, index=False)
    with zipfile.ZipFile(config.RET_SHAPES_ZIP, "w", zipfile.ZIP_DEFLATED) as out:
        out.writestr("shapes.txt", buf.getvalue())
    return shp["shape_id"].nunique()


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    z, rail, line_of, mode_of, trips, st, stops, cal = load_feed()
    print(f"RET rail in the national feed: {len(rail)} lines drawn "
          f"({', '.join(config.NOT_DRAWN)} not), {len(trips):,} trips, "
          f"{len(st):,} stop times")

    boardable = station_gates.boardable_stop_ids(st)
    non_revenue = 0
    if boardable is not None:
        before = st["stop_id"].nunique()
        st = st[st["stop_id"].isin(boardable)]
        non_revenue = before - st["stop_id"].nunique()
    siding = set(stops.index[stops["stop_name"].str.split(", ", n=1).str[-1]
                             .str.startswith(config.NON_REVENUE_PREFIX)])
    sidings = sorted(stops.loc[list(siding & set(st["stop_id"])), "stop_name"].unique())
    st = st[~st["stop_id"].isin(siding)]
    non_revenue += len(sidings)
    print(f"  turning sidings dropped as non-revenue: {sidings}")

    # From here on a stop's "name" is its PLACE key (name#k), never the bare name.
    place = places(stops, set(st["stop_id"]))
    stops = stops.loc[list(place)].copy()
    stops["stop_name"] = pd.Series(place)
    shared = sum(1 for k in set(place.values()) if not k.endswith("#0"))
    print(f"  {len(set(place.values()))} places; {shared} share a stop name with another place")

    regular, report = regular_routes(trips, st, stops, cal)
    print("\n  regular route per line (stops served on >= "
          f"{config.REGULAR_ROUTE_MIN_DAY_SHARE:.0%} of the line's days):")
    for ln in config.LINE_ORDER:
        days, seen, kept = report[ln]
        print(f"    {config.LINE_NAMES[ln]:<9} {days:>3} days  {seen:>3} stop names seen, "
              f"{kept:>3} regular")

    names = set().union(*regular.values())
    q = stops[stops["stop_name"].isin(names) & stops.index.isin(set(st["stop_id"]))].copy()
    q["latitude"] = q["stop_lat"].astype(float)
    q["longitude"] = q["stop_lon"].astype(float)
    g = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q["longitude"], q["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(q)} platforms under {len(names)} names; widest spreads:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {short(nm):<34} {spread[nm]:>5.0f} m")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M} m would be averaged "
                 f"into one point: {too_far.round().to_dict()}")
    by_name = q.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                         longitude=("longitude", "mean"))
    lines_of = {n: sorted((ln for ln, s in regular.items() if n in s),
                          key=config.LINE_ORDER.index) for n in names}
    by_name["lines"] = [" ".join(lines_of[n]) for n in by_name.index]

    metro_lines = [ln for ln in config.LINE_ORDER if mode_of[ln] == config.METRO_ROUTE_TYPE]
    metro_names = {n for n in names if set(lines_of[n]) & set(metro_lines)}
    actual = {config.LINE_NAMES[ln]: len(regular[ln]) for ln in metro_lines}
    actual["Metro (network)"] = len(metro_names)
    print()
    station_gates.verify_stations(
        city="Rotterdam", platforms=q, stations=by_name, crs_projected=config.CRS_PROJECTED,
        non_revenue=non_revenue, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    emit("regular_stop_names", len(names))
    emit("metro_stations_network", len(metro_names))

    # --- the gemeente ------------------------------------------------------
    poly = city_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(by_name["longitude"], by_name["latitude"]),
                        index=by_name.index, crs=config.CRS_GEOGRAPHIC)
    inside = set(by_name.index[pts.within(poly).values])
    print(f"\n  gemeente {config.GEMEENTE_CODE}: {len(names)} stop names -> {len(inside)} inside, "
          f"{len(names) - len(inside)} outside")
    survival = {}
    print("  per line, inside the gemeente (the worst line decides the scope question):")
    for ln in config.LINE_ORDER:
        n_in = len(regular[ln] & inside)
        survival[ln] = n_in / len(regular[ln])
        print(f"    {config.LINE_NAMES[ln]:<9} {n_in:>3} of {len(regular[ln]):>3}  "
              f"({survival[ln]:.0%})")
    worst = min(survival, key=survival.get)
    print(f"  worst: {config.LINE_NAMES[worst]} at {survival[worst]:.0%}")
    if min(survival.values()) == 0:
        sys.exit("gemeente-only scope drops a whole line; the scope decision needs re-taking")

    # --- thinning ------------------------------------------------------------
    coords = {n: (r["latitude"], r["longitude"]) for n, r in by_name.iterrows()}
    interchange = {n for n in inside if len(lines_of[n]) >= 2}
    kept, cuts, all_shapes, line_shapes = set(), [], [], {}
    for ln in config.LINE_ORDER:
        seqs, shapes = sequences(ln, trips, st, stops, regular[ln])
        line_shapes[ln] = shapes
        all_shapes += shapes
        k, c = thin(ln, seqs, inside, metro_names, interchange, coords)
        kept |= k
        cuts += c
    cuts = [c for c in cuts if c["station"] not in kept]
    print(f"\n  thinning (metro kept, terminals kept, {len(interchange)} interchanges kept, "
          f"the rest one per {config.THIN_SPACING_MILES} mi): {len(inside)} in-gemeente stop "
          f"names -> {len(kept)} stations")
    emit("stations_inside", len(inside))
    emit("stations_kept", len(kept))

    # --- records -------------------------------------------------------------
    nb = neighbour_polygons()
    excluded = []
    for n in sorted(names - inside):
        pt = pts[n]
        hit = nb[nb.contains(pt) & (nb["code"] != config.GEMEENTE_CODE)]
        if len(hit) != 1:
            sys.exit(f"{n} is outside Rotterdam and in {len(hit)} recorded neighbour(s)")
        excluded.append({"station": short(n), "lines": by_name.at[n, "lines"],
                         "reason": f"in {hit.iloc[0]['name']} ({hit.iloc[0]['code']}), "
                                   f"outside gemeente {config.GEMEENTE_CODE}",
                         "latitude": by_name.at[n, "latitude"],
                         "longitude": by_name.at[n, "longitude"]})
    seen = set()
    for c in sorted(cuts, key=lambda c: (c["station"], c["line"])):
        if c["station"] in seen:
            continue
        seen.add(c["station"])
        excluded.append({"station": short(c["station"]), "lines": by_name.at[c["station"], "lines"],
                         # "spacing filter" is the phrase app/station_scope.py
                         # reads to count a stop as thinned on the published
                         # scope table (check_scope_disclosure.py).
                         "reason": f"spacing filter on {c['line']}: {c['miles_since_kept']} mi after "
                                   f"{short(c['nearest_kept'])}, under "
                                   f"{config.THIN_SPACING_MILES} mi",
                         "latitude": by_name.at[c["station"], "latitude"],
                         "longitude": by_name.at[c["station"], "longitude"]})
    out = pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    n_out = int(out["reason"].str.startswith("in ").sum())
    print(f"\n  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}: "
          f"{n_out} outside the gemeente, {len(out) - n_out} thinned")
    for _, r in out[out["reason"].str.startswith("in ")].iterrows():
        print(f"    {r['station']:<34} {r['lines']:<10} {r['reason']}")

    keep = by_name.loc[sorted(kept)].reset_index().rename(columns={"stop_name": "station_key"})
    keep.insert(0, "stop_id", keep["station_key"])
    keep.insert(1, "station", keep["station_key"].map(short))
    keep = keep[["stop_id", "station", "lines", "latitude", "longitude"]].sort_values("station")
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    n_shapes = write_shapes(z, all_shapes)
    config.LINE_SHAPES_JSON.write_text(json.dumps(line_shapes, indent=1), encoding="utf-8")
    print(f"  {n_shapes} RET shapes -> {config.RET_SHAPES_ZIP.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
