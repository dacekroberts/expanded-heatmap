"""Step 1 for the Flemish tram cities (Antwerp, Ghent): De Lijn's trams ->
stations inside the city, the stops outside listed with their commune.

Each city's `step1_stations.py` is a thin wrapper over `build()`, with its own
config. What it does, in order, every stage printed:

  1. the feed's tram routes printed; the city's lines matched on
     `route_short_name`; a line the config records as absent (Antwerp's 3, 5,
     9 and 15) returning to the feed stops the build;
  2. the city's tram stop_times read in chunks (cached, keyed on the feed
     version); a stop_time where no passenger can board or alight (pickup 1
     and drop-off 1) dropped (`pipeline/stations.py`, gate 2, row by row);
  3. platforms merged into stations by name with the platform marker removed
     ("perron N", "Metro Perron X", "Metro"), compared case-folded (owner,
     2026-10-03), plus config.NAME_ALIASES. Every name carrying a marker word
     must match the marker, and a merged name wider than
     COLLAPSE_MAX_SPREAD_M stops the build. A line's stations are its
     REGULAR ROUTE: the names it serves on at least REGULAR_MIN_DAY_SHARE of
     the days it runs in the feed's window, so a short works diversion or a
     temporary stop is not the network (Amsterdam's rule);
  4. stations cut by the city's commune polygon (OSM, `ref:INS`); a stop
     outside is drawn with its line, not ringed, and listed in
     `excluded_stations.csv` with the commune it lies in. No thinning (owner);
  5. the CLOSED_FOR_WORKS stations: listed with a "closed for works" reason,
     and the build stops if the feed serves any of them again;
  6. the nearest-neighbour distribution printed, the median checked against
     the config's band (the halved-ring choice), the station gates run, and
     gate 3 run or its recorded gap printed;
  7. each line's shapes written to a small zip for step 3: its most-used
     shape, then whatever shapes it takes to pass within SHAPE_TOLERANCE_M of
     every station of the line (`belgium_delijn.cover_shapes`); its daytime
     headway on the reference date (`belgium_delijn.reference_date`)
     printed.
"""
import json
import re
import sys

import geopandas as gpd
import numpy as np
import pandas as pd

from pipeline import stations as station_gates
from pipeline.baseline import emit
from pipeline.countries import belgium_delijn as dl
from pipeline.countries.belgium import commune_polygons

# A merged name whose platforms are further apart than this is two places.
COLLAPSE_MAX_SPREAD_M = 400.0
# A line's stations are the names it serves on at least this share of the
# days it runs in the feed's window (Amsterdam's regular-route rule).
REGULAR_MIN_DAY_SHARE = 0.5
# Every station of a line must lie within this distance of a drawn shape.
SHAPE_TOLERANCE_M = 100.0


def _short(name, prefix):
    return name[len(prefix):] if prefix and name.startswith(prefix) else name


def build(cfg, city, fetch_script):
    cfg.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)
    z, meta = dl.need_feed(fetch_script)
    info = dl.feed_info(z)
    if meta.get("feed_version") != info["version"]:
        sys.exit(f"the feed's meta JSON says {meta.get('feed_version')}, the feed {info['version']}")
    ref = dl.reference_date(info)
    print(f"De Lijn feed {info['version']} ({info['start']} to {info['end']}, fetched "
          f"{meta['fetched']}); reference date {ref} (a Tuesday)\n")

    # 1. routes
    routes, all_trams = dl.tram_routes(z, city)
    back = sorted(set(cfg.ABSENT_LINES) & set(all_trams["route_short_name"]))
    if back:
        sys.exit(f"line(s) {back} are back in the feed as trams - the works shape has ended "
                 f"or changed: re-read the network and config.CLOSED_FOR_WORKS before step 1")
    feed_colours = dl.colours(routes)
    print("\n  the city's lines, feed colours (route_color / route_text_color):")
    for ln in cfg.LINES:
        c, t = feed_colours[ln]
        print(f"    {ln:<4} {c} / {t}   {sorted(set(routes.loc[routes['route_short_name'] == ln, 'route_long_name']))}")
    if cfg.FEED_COLOURS and {k: v[0] for k, v in feed_colours.items()} != cfg.FEED_COLOURS:
        sys.exit(f"the feed's colours moved: {feed_colours} against config.FEED_COLOURS")

    # 2. stop_times across the feed's window
    trips = dl.tram_trips(z, routes)
    # The second value (every stop_id any trip serves) is what showed the left
    # bank's stops are still served by buses (2026-10-04); not used here.
    st, _served_any = dl.tram_stop_times(z, trips, cfg.TRAM_STOP_TIMES_CSV, info["version"])
    services = dl.active_services(z, ref)
    day = trips[trips["service_id"].isin(services)]
    per_line = day.groupby("line").size()
    print(f"\n  trips on {ref}: " + ", ".join(f"{ln} {int(per_line.get(ln, 0))}" for ln in cfg.LINES))
    idle = [ln for ln in cfg.LINES if int(per_line.get(ln, 0)) == 0]
    if idle:
        sys.exit(f"line(s) {idle} run no trip on the reference date {ref}")
    if station_gates.boardable_stop_ids(st.head(1)) is None:
        sys.exit("the feed carries no pickup_type/drop_off_type: boardability cannot be read")
    # Boardability per stop_time row: a row with pickup 1 AND drop-off 1 is a
    # tram passing without stopping (gate 2, read row by row).
    ok = (st["pickup_type"].replace("", "0").isin(("0", "2", "3"))
          | st["drop_off_type"].replace("", "0").isin(("0", "2", "3")))
    link_all = st.merge(trips[["trip_id", "line", "service_id"]], on="trip_id")
    link = link_all[ok.values]
    unboardable = set(st["stop_id"]) - set(link["stop_id"])

    stops = pd.read_csv(z.open("stops.txt"), dtype=str, keep_default_na=False).set_index("stop_id")
    if (stops["parent_station"] != "").any():
        print("  NOTE: the feed now carries parent_station: collapse on it instead of names")
    for sid in sorted(unboardable):
        print(f"    no passenger boards or alights on any trip in the window (dropped): "
              f"{stops.at[sid, 'stop_name']}")

    # 3. platforms -> stations by name
    marker = re.compile(cfg.PLATFORM_MARKER)
    words = re.compile(cfg.PLATFORM_WORDS)
    q = stops.loc[sorted(set(link["stop_id"]))].copy()
    q["latitude"] = q["stop_lat"].astype(float)
    q["longitude"] = q["stop_lon"].astype(float)
    q["base"] = q["stop_name"].map(lambda n: dl.collapse_name(n, marker))
    unmatched = q[q["base"].isna() & q["stop_name"].str.contains(words)]
    if len(unmatched):
        sys.exit(f"name(s) carrying a platform word did not match the marker: "
                 f"{sorted(unmatched['stop_name'])} - extend config.PLATFORM_MARKER")
    q["base"] = q["base"].fillna(q["stop_name"].map(dl.norm))
    # One station under two names (config.NAME_ALIASES, each measured and
    # named in the config); an alias whose name has gone stops the build.
    gone = sorted(set(cfg.NAME_ALIASES) - set(q["base"]))
    if gone:
        sys.exit(f"config.NAME_ALIASES names no longer served: {gone} - re-read them")
    q["base"] = q["base"].replace(cfg.NAME_ALIASES)
    q["key"] = q["base"].str.casefold()

    # A line's stations are its REGULAR ROUTE: the names it serves on at least
    # REGULAR_MIN_DAY_SHARE of the days it runs in the feed's window
    # (Amsterdam's rule). A one-day reference date caught Ghent's Bijlokehof in
    # a closure that ends two days later; a works stop used for a few weeks
    # (Martelaarslaan, from 2026-11-02) is not the network either.
    days_of = dl.service_days(z, info["start"], info["end"])
    link = link.assign(key=link["stop_id"].map(q["key"]))
    regular, report = {}, {}
    for ln in cfg.LINES:
        g = link[link["line"] == ln]
        line_days = set().union(*(days_of.get(s, set()) for s in g["service_id"].unique()))
        per = g.groupby("key")["service_id"].agg(
            lambda s: len(set().union(*(days_of.get(x, set()) for x in set(s)))))
        share = per / max(len(line_days), 1)
        regular[ln] = set(share[share >= REGULAR_MIN_DAY_SHARE].index)
        report[ln] = (len(line_days), share)
    print(f"\n  regular route per line (names served on at least "
          f"{REGULAR_MIN_DAY_SHARE:.0%} of the line's days, {info['start']} to {info['end']}):")
    for ln in cfg.LINES:
        n_days, share = report[ln]
        odd = share[share < REGULAR_MIN_DAY_SHARE]
        print(f"    {ln:<4} {n_days:>3} days, {len(share):>3} names seen, {len(regular[ln]):>3} regular"
              + ("; not regular: " + ", ".join(f"{k} {v:.0%}" for k, v in odd.items())
                 if len(odd) else ""))
    keys = set().union(*regular.values())
    q = q[q["key"].isin(keys)]

    print(f"\n  {len(q)} boardable tram platforms on the regular routes, {q['key'].nunique()} "
          f"names after the merge; merged names:")
    for key, g in q.groupby("key"):
        if len(set(g["stop_name"])) > 1 or g["stop_name"].iloc[0] != g["base"].iloc[0]:
            print(f"    {g['base'].mode().iloc[0]:<44} <- {len(g)} platform(s): "
                  f"{sorted(set(g['stop_name']))}")
    gq = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q["longitude"], q["latitude"]),
                          crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    spread = gq.groupby("key")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print("  widest merges: " + ", ".join(f"{k} {v:.0f} m" for k, v in
                                          spread.sort_values(ascending=False).head(5).items()))
    wide = spread[spread > COLLAPSE_MAX_SPREAD_M]
    if len(wide):
        sys.exit(f"merged names wider than {COLLAPSE_MAX_SPREAD_M:.0f} m: {wide.round().to_dict()}")

    order = {ln: i for i, ln in enumerate(cfg.LINES)}
    by = q.groupby("key").agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"))
    by["name"] = q.groupby("key")["base"].agg(lambda s: sorted(s.value_counts().index[
        s.value_counts() == s.value_counts().max()])[0])
    by["lines"] = [" ".join(ln for ln in cfg.LINES if k in regular[ln]) for k in by.index]
    by["n_platforms"] = q.groupby("key").size()
    sd = link[link["trip_id"].isin(set(day["trip_id"]))]
    sd_all = link_all[link_all["trip_id"].isin(set(day["trip_id"]))]

    # 4. the city polygon, and the communes outside
    communes = commune_polygons(cfg.OSM_COMMUNES_JSON, fetch_script, cfg.OWN_NIS,
                                cfg.COMMUNE_AREA_KM2, city.capitalize())
    city_poly = communes.loc[communes["nis"] == cfg.OWN_NIS, "geometry"].union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(by["longitude"], by["latitude"]), index=by.index,
                        crs=cfg.CRS_GEOGRAPHIC)
    by["inside"] = pts.within(city_poly).values
    n_in = int(by["inside"].sum())
    print(f"\n  {len(by)} stations: {n_in} inside NIS {cfg.OWN_NIS}, {len(by) - n_in} outside")
    print("  per line, inside the city (whole line drawn; a stub stops the build):")
    for ln in cfg.LINES:
        mine = by[by["lines"].str.split().map(lambda ls, ln=ln: ln in ls)]
        share = mine["inside"].mean()
        print(f"    {ln:<4} {int(mine['inside'].sum()):>3} of {len(mine):>3} ({share:.0%})")
        emit(f"stops_line_{ln}", len(mine))
        if share < cfg.STUB_MIN_SHARE:
            sys.exit(f"line {ln} keeps {share:.0%} inside, under {cfg.STUB_MIN_SHARE:.0%}: "
                     f"a stub question for the owner")

    excluded = []
    for k, r in by[~by["inside"]].sort_values("name").iterrows():
        hit = communes[communes.contains(pts[k]) & (communes["nis"] != cfg.OWN_NIS)]
        if len(hit) != 1:
            sys.exit(f"{r['name']} is outside the city and in {len(hit)} recorded commune(s)")
        excluded.append({"station": _short(r["name"], cfg.OWN_PREFIX),
                         "lines": r["lines"].replace(" ", "/"),
                         "reason": f"in {hit.iloc[0]['name']} (NIS {hit.iloc[0]['nis']}), "
                                   f"outside {city.capitalize()} (NIS {cfg.OWN_NIS})",
                         "latitude": r["latitude"], "longitude": r["longitude"]})

    # 5. closed for works
    closed = []
    names = stops["stop_name"].map(dl.norm)
    for name, (label, why) in cfg.CLOSED_FOR_WORKS.items():
        ids = names.index[names == dl.norm(name)]
        if not len(ids):
            sys.exit(f"closed-for-works stop {name!r} is no longer in stops.txt by that name")
        if set(ids) & set(link["stop_id"]):
            sys.exit(f"the feed serves {name!r} by tram again (a passenger can board or "
                     f"alight on some day of its window) - it was closed for works. Take it "
                     f"out of config.CLOSED_FOR_WORKS and re-run.")
        through = sd_all[sd_all["stop_id"].isin(set(ids))]
        lines = sorted(set(through["line"]), key=order.get)
        g = stops.loc[ids]
        closed.append({"station": label, "lines": "/".join(lines), "reason": why,
                       "latitude": g["stop_lat"].astype(float).mean(),
                       "longitude": g["stop_lon"].astype(float).mean(),
                       "_through": len(through)})
    if closed:
        print(f"\n  {len(closed)} station(s) closed for works (config.CLOSED_FOR_WORKS):")
        for c in closed:
            print(f"    {c['station']:<32} lines {c['lines'] or '-':<12} trams pass without "
                  f"stopping {c['_through']} times on {ref}")
    if getattr(cfg, "CLOSED_FOR_WORKS_OPEN_QUESTION", None):
        print(f"\n  WARNING (for the lead): {cfg.CLOSED_FOR_WORKS_OPEN_QUESTION}")

    # 6. spacing, gates
    inside = by[by["inside"]]
    nn = station_gates.nearest_neighbour_m(inside["longitude"], inside["latitude"],
                                           cfg.CRS_PROJECTED)
    nn_all = station_gates.nearest_neighbour_m(by["longitude"], by["latitude"], cfg.CRS_PROJECTED)
    pct = np.percentile(nn, [0, 10, 25, 50, 75, 90, 100])
    print(f"\n  nearest-neighbour gap, {len(inside)} stations inside: "
          + ", ".join(f"p{p} {v:.0f} m" for p, v in zip((0, 10, 25, 50, 75, 90, 100), pct)))
    print(f"  network ({len(by)} stations): median {np.median(nn_all):.0f} m")
    med = float(np.median(nn))
    lo, hi = cfg.MEDIAN_GAP_BOUNDS_M
    if not lo <= med <= hi:
        sys.exit(f"the median gap {med:.0f} m is outside {lo:.0f}-{hi:.0f} m: re-take the ring "
                 f"choice (docs/ring_rules.md) before moving the band")
    print(f"  median {med:.0f} m, under about 550 m: halved rings (0.05 to 0.3 mi)")
    emit("median_gap_m", round(med))
    actual = {ln: int(by["lines"].str.split().map(lambda ls, ln=ln: ln in ls).sum())
              for ln in cfg.LINES}
    res = station_gates.verify_stations(
        city=city.capitalize(), platforms=q[q["key"].isin(inside.index)], stations=inside,
        crs_projected=cfg.CRS_PROJECTED, non_revenue=len(unboardable),
        spacing_min=cfg.SPACING_MIN_M, expected_per_line=cfg.OPERATOR_STATION_COUNTS,
        actual_per_line=actual)
    if cfg.OPERATOR_STATION_COUNTS is None:
        print(f"    gate 3 NOT RUN - OPERATOR_COUNTS_GAP: {cfg.OPERATOR_COUNTS_GAP}")
    elif res["per_line_mismatches"]:
        sys.exit(f"gate 3: per-line mismatches against {cfg.OPERATOR_COUNTS_SOURCE}: "
                 f"{res['per_line_mismatches']}")
    else:
        print(f"    gate 3 source: {cfg.OPERATOR_COUNTS_SOURCE}")
        unknown = sorted(set(cfg.OPERATOR_STATION_COUNTS) - set(cfg.LINES))
        if unknown:
            sys.exit(f"gate 3 names line(s) {unknown} this city does not draw")
        rest = [ln for ln in cfg.LINES if ln not in cfg.OPERATOR_STATION_COUNTS]
        if rest:
            if not cfg.OPERATOR_COUNTS_GAP:
                sys.exit(f"gate 3 compares no figure for {rest}, and OPERATOR_COUNTS_GAP "
                         f"does not say why")
            print(f"    gate 3 PARTIAL - not compared {rest}: {cfg.OPERATOR_COUNTS_GAP}")

    # 7. shapes and headways
    window = trips[trips["service_id"].isin(set(days_of))]
    cands = sorted(set(window.loc[window["shape_id"] != "", "shape_id"]))
    lines_xy = dl.shape_lines(z, cands, cfg.CRS_PROJECTED)
    bxy = gpd.GeoSeries(gpd.points_from_xy(by["longitude"], by["latitude"]), index=by.index,
                        crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    stations_xy = {ln: [(k, bxy[k]) for k in by.index if k in regular[ln]] for ln in cfg.LINES}
    shape_of = dl.cover_shapes(window, stations_xy, lines_xy, SHAPE_TOLERANCE_M)
    n_pts = dl.write_shapes(z, [s for ss in shape_of.values() for s in ss], cfg.LINE_SHAPES_ZIP)
    cfg.LINE_SHAPES_JSON.write_text(json.dumps(shape_of, indent=1), encoding="utf-8")
    print(f"\n  shapes drawn per line (the most used, then any needed to reach every station "
          f"within {SHAPE_TOLERANCE_M:.0f} m), {n_pts:,} points -> {cfg.LINE_SHAPES_ZIP.name}:")
    for ln in cfg.LINES:
        print(f"    {ln:<4} {shape_of[ln]}")
    hw = dl.headways(day, sd[dl.STOP_TIME_COLS], services)
    print("  mean daytime headway (trips leaving their first stop 09:00-16:00, per direction): "
          + ", ".join(f"{ln} {hw.get(ln)} min" for ln in cfg.LINES))

    # records
    rows = excluded + [{k: v for k, v in c.items() if not k.startswith("_")} for c in closed]
    out = pd.DataFrame(rows, columns=["station", "lines", "reason", "latitude", "longitude"])
    out.to_csv(cfg.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(out)} excluded -> {cfg.EXCLUDED_STATIONS_CSV.relative_to(cfg.ROOT)} "
          f"({len(excluded)} outside, {len(closed)} closed for works)")
    for r in excluded:
        print(f"    {r['station']:<34} {r['lines']:<8} {r['reason']}")

    keep = inside.reset_index().rename(columns={"key": "stop_id"})
    keep["station"] = keep["name"].map(lambda n: _short(n, cfg.OWN_PREFIX))
    if keep["station"].duplicated().any():
        sys.exit(f"two stations share a label: {sorted(keep.loc[keep['station'].duplicated(), 'station'])}")
    keep = keep[["stop_id", "station", "lines", "latitude", "longitude"]].sort_values("station")
    keep.to_csv(cfg.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(keep)} stations -> {cfg.STATIONS_CSV.relative_to(cfg.ROOT)}")
    emit("stations_network", len(by))
    emit("stations_inside", len(keep))
    emit("stations_closed", len(closed))
    return {"reference_date": str(ref), "feed": info, "colours": feed_colours,
            "headways": hw, "median_gap_m": med}
