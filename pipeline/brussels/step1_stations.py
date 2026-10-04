"""Brussels step 1: STIB's metro, premetro and tram stations in the City.

    python pipeline/brussels/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **The corridor is a name list.** The 25 underground metro and premetro
    stations in the commune are always kept, and three of them (Anneessens,
    Bourse, Lemonnier) are served by trams alone, so "served by the metro"
    would thin them as surface stops.
  * **Trams are thinned** (Amsterdam's rule, docs/sub_transit_line_filters.md)
    on each line's stretch inside the commune. Every cut stop is recorded.
  * **A line's stations are its regular route** (Amsterdam's rule): stops it
    serves on at least half its days in the feed's window.
  * **Names are bilingual.** The feed's names are upper case; translations.txt
    gives French and Dutch, shown "French / Dutch" where they differ.
  * Stations outside the commune are named with their commune from the
    Region's commune limits, or as outside the Region.
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
from pipeline.brussels import config  # noqa: E402
from pipeline.countries.belgium import brussels_region_communes  # noqa: E402

FETCH = "pipeline/brussels/fetch_sources.py"


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python {FETCH}")
    return path


def base(key):
    """'ROGIER#0' -> 'ROGIER'."""
    return key.split("#", 1)[0]


def places(stops, used_ids):
    """stop_id -> place key 'NAME#k': one name's platforms split into places by
    single-linkage distance (Amsterdam's rule), west to east."""
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
        groups = sorted(roots.values(), key=lambda m: min(pts[i].x for i in m))
        for k, members in enumerate(groups):
            spread = max((pts[a].distance(pts[b]) for a in members for b in members), default=0.0)
            if spread > config.COLLAPSE_MAX_SPREAD_M:
                sys.exit(f"{name}: one place {spread:.0f} m across")
            for i in members:
                key[ids[i]] = f"{name}#{k}"
    return key


def load_feed():
    z = zipfile.ZipFile(need(config.GTFS_ZIP, "STIB's GTFS"))
    info = pd.read_csv(z.open("feed_info.txt"), dtype=str).iloc[0]
    print(f"STIB feed {info['feed_version']}: {info['feed_start_date']} to {info['feed_end_date']}")
    routes = pd.read_csv(z.open("routes.txt"), dtype=str)
    rail = routes[routes["route_type"].isin(config.ROUTE_TYPES_RAIL)].copy()
    lines = sorted(rail["route_short_name"], key=lambda x: (len(x), x))
    want = sorted(config.LINE_ORDER + config.TRAM_LINES_OUTSIDE, key=lambda x: (len(x), x))
    if lines != want:
        sys.exit(f"STIB's rail lines changed.\n  feed  : {lines}\n  config: {want}\n"
                 f"A line added or withdrawn is a scope decision, not a config edit.")
    metro = sorted(rail.loc[rail["route_type"] == config.METRO_ROUTE_TYPE, "route_short_name"])
    if metro != sorted(config.METRO_LINES):
        sys.exit(f"metro lines in the feed: {metro}")
    recorded = {**config.METRO_FEED_COLOURS, **config.TRAM_FEED_COLOURS}
    for _, r in rail[rail["route_short_name"].isin(config.LINE_ORDER)].iterrows():
        feed = "#" + str(r["route_color"]).lower()
        if feed != recorded[r["route_short_name"]]:
            sys.exit(f"line {r['route_short_name']}'s route_color is now {feed}; config "
                     f"records {recorded[r['route_short_name']]}: re-measure the colours")
    line_of = dict(zip(rail["route_id"], rail["route_short_name"]))
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
    days = dates_of_services(z, set(trips["service_id"]))
    tr = pd.read_csv(z.open("translations.txt"), dtype=str)
    tr = tr[(tr["table_name"] == "stops") & (tr["field_name"] == "stop_name")]
    names = {lang: dict(zip(g["field_value"], g["translation"]))
             for lang, g in tr.groupby("language")}
    return rail, trips, st, stops, days, names


def dates_of_services(z, services):
    """{service_id: set of dates it runs}: calendar.txt expanded, then
    calendar_dates.txt's additions and removals applied."""
    days = {s: set() for s in services}
    cal = pd.read_csv(z.open("calendar.txt"), dtype=str)
    cal = cal[cal["service_id"].isin(services)]
    wd = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for _, r in cal.iterrows():
        for d in pd.date_range(r["start_date"], r["end_date"]):
            if r[wd[d.weekday()]] == "1":
                days[r["service_id"]].add(d.strftime("%Y%m%d"))
    cd = pd.read_csv(z.open("calendar_dates.txt"), dtype=str)
    for _, r in cd[cd["service_id"].isin(services)].iterrows():
        if r["exception_type"] == "1":
            days[r["service_id"]].add(r["date"])
        else:
            days[r["service_id"]].discard(r["date"])
    return days


def regular_routes(trips, st, stops, days_of):
    """{line: set of place keys it serves on at least the configured share of its days}."""
    link = st.merge(trips[["trip_id", "line", "service_id"]], on="trip_id")
    link["name"] = link["stop_id"].map(stops["stop_name"])
    regular, report = {}, {}
    for line, g in link.groupby("line"):
        line_days = set().union(*(days_of.get(s, set()) for s in g["service_id"].unique()))
        per = g.groupby("name")["service_id"].agg(
            lambda s: len(set().union(*(days_of.get(x, set()) for x in set(s)))))
        share = per / len(line_days)
        trip_share = g.groupby("name")["trip_id"].nunique() / g["trip_id"].nunique()
        keep = set(share[(share >= config.REGULAR_ROUTE_MIN_DAY_SHARE)
                         & (trip_share >= config.REGULAR_ROUTE_MIN_TRIP_SHARE)].index)
        regular[line] = keep
        report[line] = (len(line_days), len(share), len(keep))
    return regular, report


def sequences(line, trips, st, stops, regular):
    """Ordered stop sequences covering the line's regular route (Amsterdam's
    rule: all-regular trips, longest first, each kept if it adds a stop)."""
    t = trips[trips["line"] == line]
    s = st[st["trip_id"].isin(set(t["trip_id"]))].copy()
    s["name"] = s["stop_id"].map(stops["stop_name"])
    s["seq"] = s["stop_sequence"].astype(int)
    pattern = s.sort_values(["trip_id", "seq"]).groupby("trip_id")["name"].agg(tuple)
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


def display(key, names):
    """'GARE CENTRALE#0' -> 'Gare Centrale / Centraal Station'."""
    raw = base(key)
    fr = names.get("fr", {}).get(raw)
    nl = names.get("nl", {}).get(raw)
    if not fr and not nl:
        sys.exit(f"{raw}: no French or Dutch name in translations.txt")
    fr, nl = fr or nl, nl or fr
    return fr if fr == nl else f"{fr} / {nl}"


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    rail, trips, st, stops, days_of, names = load_feed()
    print(f"  {len(rail)} rail lines, {len(trips):,} trips, {len(st):,} stop times")

    boardable = station_gates.boardable_stop_ids(st)
    non_revenue = 0
    if boardable is not None:
        before = st["stop_id"].nunique()
        st = st[st["stop_id"].isin(boardable)]
        non_revenue = before - st["stop_id"].nunique()

    stops["stop_name"] = stops["stop_name"].replace(config.STOP_NAME_ALIASES)
    place = places(stops, set(st["stop_id"]))
    stops =stops.loc[list(place)].copy()
    stops["stop_name"] = pd.Series(place)
    shared = sum(1 for k in set(place.values()) if not k.endswith("#0"))
    print(f"  {len(set(place.values()))} places; {shared} share a stop name with another place")

    regular, report = regular_routes(trips, st, stops, days_of)
    all_lines = config.LINE_ORDER + config.TRAM_LINES_OUTSIDE
    print("\n  regular route per line (stops served on >= "
          f"{config.REGULAR_ROUTE_MIN_DAY_SHARE:.0%} of the line's days):")
    for ln in all_lines:
        d, seen, kept = report[ln]
        print(f"    {ln:>3} {d:>3} days  {seen:>3} stop names seen, {kept:>3} regular")

    # --- the commune -------------------------------------------------------
    com = brussels_region_communes(config.COMMUNES_GEOJSON, FETCH)
    city = com[com["nis"] == config.COMMUNE_CODE].geometry.union_all()
    area = float(gpd.GeoSeries([city], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6)
    lo, hi = config.COMMUNE_AREA_KM2
    print(f"\n  City of Brussels ({config.COMMUNE_CODE}): {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"the City's polygon is {area:.1f} km2, outside {lo}-{hi}")

    every = set().union(*regular.values())
    q = stops[stops["stop_name"].isin(every) & stops.index.isin(set(st["stop_id"]))].copy()
    q["latitude"] = q["stop_lat"].astype(float)
    q["longitude"] = q["stop_lon"].astype(float)
    by_all = q.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                        longitude=("longitude", "mean"))
    pts_all = gpd.GeoSeries(gpd.points_from_xy(by_all["longitude"], by_all["latitude"]),
                            index=by_all.index, crs=config.CRS_GEOGRAPHIC)
    inside = set(by_all.index[pts_all.within(city).values])
    inside |= {n for n in by_all.index if base(n) in config.CORRIDOR}
    entering = sorted((ln for ln in all_lines if regular[ln] & inside),
                      key=lambda x: (len(x), x))
    if entering != sorted(config.LINE_ORDER, key=lambda x: (len(x), x)):
        sys.exit(f"lines entering the commune changed: {entering} against {list(config.LINE_ORDER)}")

    names_drawn = set().union(*(regular[ln] for ln in config.LINE_ORDER))
    q = q[q["stop_name"].isin(names_drawn)]
    by_name = by_all.loc[sorted(names_drawn)].copy()
    lines_of = {n: [ln for ln in config.LINE_ORDER if n in regular[ln]] for n in names_drawn}
    by_name["lines"] = [" ".join(lines_of[n]) for n in by_name.index]

    metro_names = {n for n in names_drawn if set(lines_of[n]) & set(config.METRO_LINES)}
    actual = {config.LINE_NAMES[ln]: len(regular[ln]) for ln in config.METRO_LINES}
    emit("metro_stations_network", len(metro_names))
    print()
    station_gates.verify_stations(
        city="Brussels", platforms=q, stations=by_name, crs_projected=config.CRS_PROJECTED,
        non_revenue=non_revenue, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    corridor = {n for n in inside & names_drawn if base(n) in config.CORRIDOR}
    found = {base(n) for n in corridor}
    if found != set(config.CORRIDOR) or len(corridor) != config.CORRIDOR_COUNT:
        sys.exit(f"corridor: {len(corridor)} places; missing {sorted(set(config.CORRIDOR) - found)}")
    print(f"  corridor: all {len(corridor)} underground stations found inside the commune")
    emit("corridor_stations", len(corridor))

    inside_drawn = inside & names_drawn
    print(f"\n  {len(names_drawn)} stop places on the drawn lines -> {len(inside_drawn)} inside, "
          f"{len(names_drawn) - len(inside_drawn)} outside")
    for ln in config.LINE_ORDER:
        n_in = len(regular[ln] & inside)
        print(f"    {config.LINE_NAMES[ln]:<9} {n_in:>3} of {len(regular[ln]):>3} inside")

    # --- thinning ------------------------------------------------------------
    xy = station_gates.projected_xy(by_name.index, by_name["longitude"], by_name["latitude"],
                                    config.CRS_PROJECTED, config.CRS_GEOGRAPHIC)
    interchange = {n for n in inside_drawn if len(lines_of[n]) >= 2}
    kept, cuts, line_shapes = set(), [], {}
    for ln in config.LINE_ORDER:
        seqs, shapes = sequences(ln, trips, st, stops, regular[ln])
        line_shapes[ln] = shapes
        if ln in config.METRO_LINES:
            kept |= regular[ln] & inside
            continue
        k, c = station_gates.thin([[n for n in seq if n in inside] for seq in seqs], xy,
                                  spacing_m=config.THIN_SPACING_MILES * 1609.344,
                                  keep_always=corridor, interchange=interchange)
        kept |= k
        cuts += [{**x, "line": config.LINE_NAMES[ln]} for x in c]
    cuts = [c for c in cuts if c["station"] not in kept]
    print(f"\n  thinning (corridor kept, terminals kept, {len(interchange)} interchanges kept, "
          f"the rest one per {config.THIN_SPACING_MILES} mi): {len(inside_drawn)} in-commune "
          f"places -> {len(kept)} stations")
    emit("stations_inside", len(inside_drawn))
    emit("stations_kept", len(kept))

    kept_xy = by_name.loc[sorted(kept)]
    nn = station_gates.nearest_neighbour_m(kept_xy["longitude"], kept_xy["latitude"],
                                           config.CRS_PROJECTED)
    print(f"  kept stations: median nearest-neighbour gap {float(pd.Series(nn).median()):.0f} m")

    # --- records -------------------------------------------------------------
    excluded = []
    for n in sorted(names_drawn - inside):
        pt = gpd.points_from_xy([by_name.at[n, "longitude"]], [by_name.at[n, "latitude"]])[0]
        hit = com[com.contains(pt)]
        where = (f"in {hit.iloc[0]['name_fr']} ({hit.iloc[0]['nis']}), outside the City of Brussels"
                 if len(hit) == 1 else "outside the Brussels-Capital Region")
        excluded.append({"station": display(n, names), "lines": by_name.at[n, "lines"],
                         "reason": where,
                         "latitude": by_name.at[n, "latitude"],
                         "longitude": by_name.at[n, "longitude"]})
    seen = set()
    for c in sorted(cuts, key=lambda c: (c["station"], c["line"])):
        if c["station"] in seen:
            continue
        seen.add(c["station"])
        excluded.append({"station": display(c["station"], names),
                         "lines": by_name.at[c["station"], "lines"],
                         # "spacing filter" is the phrase app/station_scope.py reads.
                         "reason": f"spacing filter on {c['line']}: "
                                   f"{round(c['metres_since_kept'] / 1609.344, 3)} mi after "
                                   f"{display(c['nearest_kept'], names)}, under "
                                   f"{config.THIN_SPACING_MILES} mi",
                         "latitude": by_name.at[c["station"], "latitude"],
                         "longitude": by_name.at[c["station"], "longitude"]})
    out = pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    n_out = int(out["reason"].str.startswith(("in ", "outside")).sum())
    print(f"\n  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}: "
          f"{n_out} outside the commune, {len(out) - n_out} thinned")

    keep = by_name.loc[sorted(kept)].reset_index().rename(columns={"stop_name": "station_key"})
    keep.insert(0, "stop_id", keep["station_key"])
    keep.insert(1, "station", [display(k, names) for k in keep["station_key"]])
    keep = keep[["stop_id", "station", "lines", "latitude", "longitude"]].sort_values("station")
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    config.LINE_SHAPES_JSON.write_text(json.dumps(line_shapes, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
