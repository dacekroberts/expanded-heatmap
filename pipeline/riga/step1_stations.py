"""Riga step 1: Rīgas satiksme's seven tram routes, from its own GTFS.

  * Routes: `route_type` 0, printed before use. All seven are drawn (owner).
  * Each route's stops are those on its REGULAR stopping patterns - a pattern
    run by at least config.PATTERN_MIN_SHARE of the route's trips in that
    direction - so a depot run or a one-off diversion adds no station.
  * Platforms collapse to stations by stop name (the feed carries no
    parent_station), refused if one name spreads wider than a station.
  * Every station must lie inside the city (the union of Riga's 58
    neighbourhoods, which equals OSM's Rīga relation).
  * Stops are 380-480 m apart, so the rings are thinned with the sub-transit
    line filters, as Amsterdam's and Rotterdam's trams were: terminals and
    interchanges kept, the rest one per half mile along each regular pattern.

Reads the cache and NEVER fetches.

    python pipeline/riga/step1_stations.py
"""
import math
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.riga import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/riga/fetch_sources.py")
    return path


def haversine_miles(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    h = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2)
    return 2 * 3958.7613 * math.asin(math.sqrt(h))


def city_polygon():
    hoods = gpd.read_file(need(config.DATA_RAW / "apkaimes.gpkg", "neighbourhoods"))
    hoods = hoods.set_crs(config.CRS_SOURCE_LV) if hoods.crs is None else hoods
    poly = hoods.to_crs(config.CRS_PROJECTED).union_all()
    km2 = poly.area / 1e6
    lo, hi = config.CITY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"the neighbourhoods' union is {km2:.1f} km2, outside {lo}-{hi}")
    return len(hoods), km2, gpd.GeoSeries([poly], crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).iloc[0]


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(need(config.GTFS_ZIP, "Rīgas satiksme GTFS"))
    rd = lambda n: pd.read_csv(z.open(n), dtype=str)  # noqa: E731
    routes, trips, stops = rd("routes.txt"), rd("trips.txt"), rd("stops.txt").set_index("stop_id")
    tram = routes[routes["route_type"] == "0"].copy()
    print("Tram routes in the feed:")
    for r in tram.itertuples():
        print(f"  {r.route_id:<14} {r.route_short_name:>3}  {r.route_long_name}  #{r.route_color}")
    if sorted(tram["route_short_name"], key=int) != config.LINE_ORDER:
        sys.exit(f"the feed's tram routes are {sorted(tram.route_short_name, key=int)}, not "
                 f"{config.LINE_ORDER} - re-read routes.txt")
    rid = dict(zip(tram["route_short_name"], tram["route_id"]))
    t = trips[trips["route_id"].isin(rid.values())]
    # stop_times.txt's rows carry EIGHT fields under a SEVEN-field header (measured
    # 2026-09-24), and pandas then silently makes the first column the index -
    # "trip_id" held arrival times and no trip matched. index_col=False keeps the
    # columns where the header says they are.
    st = pd.read_csv(z.open("stop_times.txt"), dtype=str, index_col=False,
                     usecols=["trip_id", "stop_id", "stop_sequence"])
    st = st[st["trip_id"].isin(t["trip_id"])].copy()
    st["seq"] = st["stop_sequence"].astype(int)
    pattern = (st.sort_values(["trip_id", "seq"]).groupby("trip_id")["stop_id"]
               .agg(lambda s: tuple(s)))
    t = t.assign(pattern=t["trip_id"].map(pattern))

    # --- places: a stop NAME can be two places ------------------------------------
    # Riga names some stops after the street, so "Brīvības iela" is two stops
    # 1,641 m apart and "Jūrmalas gatve" two 704 m apart (measured 2026-09-24).
    # Platforms of one name are grouped into places within
    # COLLAPSE_MAX_SPREAD_M; a second place gets the key "name#2", and prints as
    # its plain name. Rotterdam's step 1 does the same.
    used_ids = sorted({s for pat in t["pattern"].dropna() for s in pat} & set(stops.index))
    lat = stops["stop_lat"].astype(float)
    lon = stops["stop_lon"].astype(float)
    key_of = {}
    for nm, ids in pd.Series(used_ids, index=[stops.at[i, "stop_name"] for i in used_ids]).groupby(level=0):
        centres = []
        for sid in ids:
            p = (lat[sid], lon[sid])
            hit = next((k for k, c in enumerate(centres)
                        if haversine_miles(p, c) * 1609.344 <= config.COLLAPSE_MAX_SPREAD_M), None)
            if hit is None:
                centres.append(p)
                hit = len(centres) - 1
            key_of[sid] = nm if hit == 0 else f"{nm}#{hit + 1}"
    split = sorted({k.split("#")[0] for k in key_of.values() if "#" in k})
    print(f"\n  names that are more than one place: {split}")
    name = pd.Series(key_of)
    line_names, seqs, shape_of = {}, [], {}
    print(f"\n  regular patterns (>= {config.PATTERN_MIN_SHARE:.0%} of a direction's trips):")
    for short in config.LINE_ORDER:
        tr = t[t["route_id"] == rid[short]]
        shape_of[short] = tr["shape_id"].value_counts().idxmax()
        kept_names = set()
        for d, grp in tr.groupby("direction_id"):
            counts = grp["pattern"].value_counts()
            regular = counts[counts / counts.sum() >= config.PATTERN_MIN_SHARE]
            for pat, n in regular.items():
                names = [name[s] for s in pat]
                seqs.append((short, names))
                kept_names |= set(names)
            print(f"    tram {short:>2} dir {d}: {len(counts)} patterns, {len(regular)} regular "
                  f"({regular.sum()} of {counts.sum()} trips)")
        line_names[short] = kept_names

    # --- one stop under two names, one per direction --------------------------
    # "Jelgavas iela" / "Jelgavas iela/Bērnu slimnīca" (25 m, tram 10), "K.Barona
    # iela" / "Brīvības iela" (55 m, tram 1): Riga names a stop's two platforms
    # differently. Two places are ONE station when they are under ALIAS_MAX_M
    # apart, share a line, and on every shared line each is served in only the
    # direction the other is not - a measured rule, not a hand list.
    dirs = {}
    for short in config.LINE_ORDER:
        tr = t[t["route_id"] == rid[short]]
        for d, grp in tr.groupby("direction_id"):
            counts = grp["pattern"].value_counts()
            for pat in counts[counts / counts.sum() >= config.PATTERN_MIN_SHARE].index:
                for sid in pat:
                    dirs.setdefault(key_of[sid], set()).add((short, d))
    cent = {k: (lat[[s for s in used_ids if key_of[s] == k]].mean(),
                lon[[s for s in used_ids if key_of[s] == k]].mean()) for k in set(key_of.values())}
    merged = {}
    keys = sorted(dirs)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if haversine_miles(cent[a], cent[b]) * 1609.344 >= config.ALIAS_MAX_M:
                continue
            shared = {ln for ln, _ in dirs[a]} & {ln for ln, _ in dirs[b]}
            if shared and all(len({d for ln, d in dirs[a] if ln == s}) == 1
                              and len({d for ln, d in dirs[b] if ln == s}) == 1
                              and {d for ln, d in dirs[a] if ln == s} != {d for ln, d in dirs[b] if ln == s}
                              for s in shared):
                merged[b] = merged.get(a, a)
    for b, a in merged.items():
        both = f"{a.split('#')[0]} / {b.split('#')[0]}"
        key_of = {s: (both if k in (a, b) else k) for s, k in key_of.items()}
        seqs = [(ln, [both if n in (a, b) else n for n in seq]) for ln, seq in seqs]
        line_names = {ln: {both if n in (a, b) else n for n in ns} for ln, ns in line_names.items()}
    print(f"  one stop under two names, merged: {[(a, b) for b, a in merged.items()]}")
    emit("directional_pairs_merged", len(merged))

    plat = stops.loc[used_ids].reset_index()
    plat["stop_name"] = plat["stop_id"].map(key_of)
    plat = plat[plat["stop_name"].isin(set().union(*line_names.values()))].copy()
    plat["latitude"], plat["longitude"] = plat["stop_lat"].astype(float), plat["stop_lon"].astype(float)
    g = gpd.GeoDataFrame(plat, geometry=gpd.points_from_xy(plat.longitude, plat.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(plat)} platforms under {spread.size} names; widest spreads:")
    for nm in spread.sort_values(ascending=False).head(5).index:
        print(f"    {nm:<32} {spread[nm]:>5.0f} m")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M:.0f} m would be averaged: "
                 f"{too_far.round().to_dict()}")
    stations = (plat.groupby("stop_name", as_index=False)
                .agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"))
                .rename(columns={"stop_name": "station"}))
    lines_of = {n: [s for s in config.LINE_ORDER if n in line_names[s]] for n in stations.station}
    stations["lines"] = [" ".join(lines_of[n]) for n in stations.station]
    station_gates.verify_stations(city="Riga", platforms=plat, stations=stations,
                                  crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M)
    emit("platforms", len(plat))
    emit("station_names", len(stations))

    # --- the city ---------------------------------------------------------------
    n_hoods, km2, poly = city_polygon()
    print(f"  city: {n_hoods} neighbourhoods, {km2:.1f} km2")
    pts = gpd.GeoSeries(gpd.points_from_xy(stations.longitude, stations.latitude), crs=config.CRS_GEOGRAPHIC)
    outside = stations[~pts.within(poly).values]
    if len(outside):
        sys.exit(f"tram stations outside Riga: {list(outside.station)} - the brief measured none")

    # --- thinning -----------------------------------------------------------------
    coords = {r.station: (r.latitude, r.longitude) for r in stations.itertuples()}
    interchange = {n for n, ls in lines_of.items() if len(ls) >= 2}
    kept, cuts = set(), []
    for short, seq in seqs:
        mark = [n in interchange for n in seq]
        mark[0] = mark[-1] = True
        since, last = 0.0, seq[0]
        for i in range(1, len(seq)):
            since += haversine_miles(coords[seq[i - 1]], coords[seq[i]])
            if mark[i]:
                since, last = 0.0, seq[i]
            elif since >= config.THIN_SPACING_MILES:
                mark[i], since, last = True, 0.0, seq[i]
            else:
                cuts.append({"station": seq[i], "line": short, "nearest_kept": last,
                             "miles_since_kept": round(since, 3)})
        kept |= {n for n, m in zip(seq, mark) if m}
    cuts = [c for c in cuts if c["station"] not in kept]
    print(f"\n  thinning (terminals and {len(interchange)} interchanges kept, the rest one per "
          f"{config.THIN_SPACING_MILES} mi): {len(stations)} -> {len(kept)} stations")
    emit("stations_kept", len(kept))

    excluded, seen = [], set()
    for c in sorted(cuts, key=lambda c: (c["station"], c["line"])):
        if c["station"] in seen:
            continue
        seen.add(c["station"])
        la, lo = coords[c["station"]]
        excluded.append({"station": c["station"].split("#")[0], "lines": " ".join(lines_of[c["station"]]),
                         # "spacing filter" is the phrase app/station_scope.py reads.
                         "reason": f"spacing filter on tram {c['line']}: {c['miles_since_kept']} mi after "
                                   f"{c['nearest_kept']}, under {config.THIN_SPACING_MILES} mi",
                         "latitude": la, "longitude": lo})
    pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(excluded)} thinned -> {config.EXCLUDED_STATIONS_CSV.name}")
    emit("stations_thinned", len(excluded))

    out = stations[stations.station.isin(kept)].sort_values("station").reset_index(drop=True)
    # A second place under one name keeps its "#2" key internally and prints as its name.
    out["station"] = out["station"].str.replace(r"#\d+$", "", regex=True)
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(out)} stations")
    print("\n  drawn shape per line (the most-used): " +
          ", ".join(f"{s}={shape_of[s]}" for s in config.LINE_ORDER))
    config.LINE_SHAPES_JSON.write_text(pd.Series(shape_of).to_json(), encoding="utf-8")


if __name__ == "__main__":
    main()
