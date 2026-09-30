"""Steps 1 and 3 for a French tram city - the France batch's shared tram
module. `france_tram_fetch.py` downloads; this module only reads the cache.

A city's step 1 is `build_stations(config, "<Name>")` and its step 3 is
`render(config, "<Name>")`. Everything that differs lives in the city's
`config.py`, written by `scripts/scaffold_france_batch.py` and filled at build.

WHY SHARED. Rennes's step 1 is 240 lines, and twenty copies of it is the shape
`france_register.py` exists to prevent. Written 2026-09-30 for the batch
(the `france-tram-city` skill, section 2), generalised from Rennes's step 1
(commune scope), Lille's (regional scope) and Rennes's step 3.

THE STATION RULE (owner, 2026-09-29 and 09-30), applied exactly:
  1. the stops served by the kept routes' trips, minus non-boardable stops
     (`pipeline/stations.py`) and fictitious `FIC_` stops (Brest's switches);
  2. a platform with a `parent_station` becomes the PARENT'S OWN ROW;
  3. a platform without one is grouped by its UNCHANGED `stop_name`, and the
     group becomes its FIRST platform in `stops.txt` order - never a mean;
  4. on a Licence Ouverte feed ONLY, a same-name pair (case and accents
     ignored) within 150 m keeps its first row; on an ODbL feed, never.
Rennes's step 1 averages a name group. That was right for Rennes and is
wrong for the batch; do not reintroduce it.
"""
import json
import sys
import unicodedata
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import shape
from shapely.ops import unary_union

from pipeline import stations as station_gates
from pipeline.baseline import emit

# The collapsed-station floor for trams. The shared gate's default (400 m) is
# a METRO floor; every city in the batch measured a 311-510 m median, and
# Rennes's own comment anticipated passing a floor for trams. 250 m still
# catches an uncollapsed platform set, whose medians run under 150 m.
TRAM_SPACING_MIN_M = 250.0
LO_LICENCES = ("lov2", "fr-lo")
SAME_NAME_WITHIN_M = 150.0


def _need(path, what, slug):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/{slug}/fetch_sources.py")
    return path


def _norm(name):
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    return " ".join(s.casefold().split())


def _read(z, name, **kw):
    with z.open(name) as f:
        return pd.read_csv(f, dtype=str, **kw)


def _routes(cfg, z):
    """The kept routes, checked against the config both ways."""
    routes = _read(z, "routes.txt")
    rail = routes[routes["route_type"].isin(cfg.ROUTE_TYPES_RAIL)]
    agency = getattr(cfg, "GTFS_AGENCY_ID", None)
    if agency:
        rail = rail[rail["agency_id"] == agency]
    excluded = getattr(cfg, "EXCLUDED_RAIL_ROUTES", {})
    # A feed route that riders know as SEVERAL lines (Reims: one route "TRAM",
    # two public lines T1 and T2 since 2025-11-24) is named in ROUTE_BRANCHES
    # and split per trip in _trip_lines(); its branch keys are in LINE_KEYS.
    branches = getattr(cfg, "ROUTE_BRANCHES", {})
    branch_keys = {k for b in branches.values() for k in b}
    wanted = {k for k in cfg.LINE_KEYS if k not in branch_keys} | set(branches)
    kept = rail[rail["route_short_name"].isin(wanted)]
    stray = sorted(set(rail["route_short_name"]) - wanted - set(excluded))
    if stray:
        sys.exit(f"the feed carries rail route(s) {stray} that are neither kept nor "
                 f"excluded in config - a line added is a scope decision")
    missing = sorted(wanted - set(kept["route_short_name"]))
    if missing:
        sys.exit(f"line(s) {missing} are not in the feed - a line withdrawn is a "
                 f"scope decision")
    print("  kept routes (route_id -> line):")
    for _, r in kept.sort_values("route_short_name").iterrows():
        print(f"    {r['route_id']:<36} {r['route_short_name']:<6} "
              f"type {r['route_type']}  colour {r.get('route_color', '')}")
    ids = sorted(kept["route_id"])
    if sorted(cfg.ROUTE_IDS) != ids:
        sys.exit(f"config.ROUTE_IDS {sorted(cfg.ROUTE_IDS)} is not the build-day "
                 f"feed's {ids}. Fill ROUTE_IDS from the list above (the feed rolls, "
                 f"so read it from today's zip, never from the brief).")
    return dict(zip(kept["route_id"], kept["route_short_name"]))


def _served_stop_times(z, trips):
    tset = set(trips["trip_id"])
    parts = []
    with z.open("stop_times.txt") as f:
        for chunk in pd.read_csv(
                f, dtype=str, chunksize=1_000_000,
                usecols=lambda c: c in {"trip_id", "stop_id", "pickup_type",
                                        "drop_off_type"}):
            parts.append(chunk[chunk["trip_id"].isin(tset)])
    return pd.concat(parts, ignore_index=True)


def _trip_lines(cfg, trips, st, stops, key_of):
    """(trip_id, line) for every kept trip. A plain route's trips take its key.
    A route in ROUTE_BRANCHES is split by the terminus each trip serves, matched
    on the stop name (accents and case ignored): a trip serving one branch's
    terminus is that line; a trip serving neither is a trunk working and
    belongs to every branch (its stops are shared); a trip serving two is an
    error, since then the split is not by terminus."""
    branches = getattr(cfg, "ROUTE_BRANCHES", {})
    out = []
    plain = trips[~trips["route_id"].map(key_of).isin(branches)]
    out.append(pd.DataFrame({"trip_id": plain["trip_id"],
                             "line": plain["route_id"].map(key_of)}))
    if branches:
        names = stops.set_index("stop_id")["stop_name"].map(_norm)
        served = st.assign(_n=st["stop_id"].map(names)).groupby("trip_id")["_n"].agg(set)
        for route_short, legs in branches.items():
            mine = trips[trips["route_id"].map(key_of) == route_short]
            want = {k: _norm(v) for k, v in legs.items()}
            first, rest = {}, []
            for tid in mine["trip_id"]:
                hits = [k for k, term in want.items()
                        if any(term in n for n in served.get(tid, ()))]
                if len(hits) > 1:
                    sys.exit(f"trip {tid} serves the termini of {hits}: ROUTE_BRANCHES "
                             f"cannot split {route_short} by terminus")
                if hits:
                    first[tid] = hits[0]
                else:
                    rest.append(tid)
            # A short working serves neither terminus: it belongs to the branch
            # whose OWN stops it serves (Reims's trips ending at Léon Blum are
            # T2's), and only a trip on shared stops alone counts for both.
            stops_of = {k: set().union(*(served[t] for t, b in first.items() if b == k))
                        for k in legs}
            own = {k: s - set().union(*(v for j, v in stops_of.items() if j != k))
                   for k, s in stops_of.items()}
            both = 0
            for tid in rest:
                hits = [k for k in legs if served.get(tid, set()) & own[k]]
                if len(hits) == 1:
                    first[tid] = hits[0]
                else:
                    both += 1
                    for k in legs:
                        out.append(pd.DataFrame({"trip_id": [tid], "line": [k]}))
            out.append(pd.DataFrame({"trip_id": list(first), "line": list(first.values())}))
            counts = pd.Series(list(first.values())).value_counts().to_dict()
            print(f"  {route_short} split by branch: {counts}, {both} trip(s) on shared "
                  f"stops only, counted for every branch")
    return pd.concat(out, ignore_index=True)


def pure_extract(cfg, z, key_of):
    """The owner's station rule. Returns (platforms, stations, non_revenue,
    dropped_pairs)."""
    trips = _read(z, "trips.txt", usecols=["route_id", "trip_id"])
    trips = trips[trips["route_id"].isin(set(key_of))]
    st = _served_stop_times(z, trips)
    board = station_gates.boardable_stop_ids(st)
    served = set(st["stop_id"])
    keep_ids = (board if board is not None else served)
    keep_ids = {s for s in keep_ids if not str(s).startswith("FIC_")}
    non_revenue = sorted(served - keep_ids)
    stops = _read(z, "stops.txt")
    st = st[st["stop_id"].isin(keep_ids)]
    st = st.merge(_trip_lines(cfg, trips, st, stops, key_of), on="trip_id")
    lines_of_stop = st.groupby("stop_id")["line"].agg(lambda s: set(s)).to_dict()

    stops["_order"] = np.arange(len(stops))
    by_id = stops.set_index("stop_id")
    plat = stops[stops["stop_id"].isin(keep_ids)].copy()
    parent = plat["parent_station"].fillna("") if "parent_station" in plat else ""
    plat["_parent"] = parent if isinstance(parent, pd.Series) else ""
    plat["_key"] = np.where(plat["_parent"] != "", "P:" + plat["_parent"],
                            "N:" + plat["stop_name"])
    rows = []
    for key, g in plat.groupby("_key", sort=False):
        if key.startswith("P:") and key[2:] in by_id.index:
            sid = key[2:]
            r = by_id.loc[sid]
            order = int(r["_order"])
        else:
            first = g.sort_values("_order").iloc[0]
            sid, r, order = first["stop_id"], first, int(first["_order"])
        lines = set().union(*(lines_of_stop.get(s, set()) for s in g["stop_id"]))
        rows.append({"stop_id": sid, "station": r["stop_name"],
                     "latitude": float(r["stop_lat"]), "longitude": float(r["stop_lon"]),
                     "lines": "/".join(sorted(lines)), "_order": order,
                     "_platforms": len(g)})
    stations = pd.DataFrame(rows).sort_values("_order").reset_index(drop=True)

    dropped = []
    if cfg.GTFS_LICENCE in LO_LICENCES:
        g = gpd.GeoSeries(gpd.points_from_xy(stations["longitude"], stations["latitude"]),
                          crs="EPSG:4326").to_crs(cfg.CRS_PROJECTED)
        stations["_norm"] = stations["station"].map(_norm)
        gone = set()
        for i in range(len(stations)):
            if i in gone:
                continue
            for j in range(i + 1, len(stations)):
                if j in gone or stations.at[j, "_norm"] != stations.at[i, "_norm"]:
                    continue
                d = g.iloc[i].distance(g.iloc[j])
                if d <= SAME_NAME_WITHIN_M:
                    gone.add(j)
                    merged = set(stations.at[i, "lines"].split("/")) | set(stations.at[j, "lines"].split("/"))
                    stations.at[i, "lines"] = "/".join(sorted(merged))
                    dropped.append((stations.at[j, "station"], stations.at[i, "station"], round(d)))
        stations = stations.drop(index=sorted(gone)).reset_index(drop=True)
    plat_out = plat.assign(latitude=plat["stop_lat"].astype(float),
                           longitude=plat["stop_lon"].astype(float))
    return plat_out, stations, non_revenue, dropped


def osm_stop_counts(cfg):
    """{ref: stop members in the ref's most complete relation}, from the cached
    Overpass answer - read-only, no network (osm_cache, never osm)."""
    path = getattr(cfg, "OSM_ROUTES_JSON", None)
    if not path or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    best = {}
    for e in data.get("elements", []):
        if e.get("type") != "relation":
            continue
        ref = (e.get("tags") or {}).get("ref")
        # DISTINCT positions: a relation may list one stop node twice (Tours's
        # tram A does), and "stop_entry_only" / "stop_exit_only" at the termini
        # are stops too, so the role test takes every "stop*" role.
        n = len({(m.get("lat"), m.get("lon"), m.get("ref")) for m in e.get("members", ())
                 if m.get("type") == "node" and str(m.get("role", "")).startswith("stop")})
        if ref and n > best.get(ref, 0):
            best[ref] = n
    return best


def _per_line(stations, keys):
    return {k: int(sum(1 for v in stations["lines"] if k in v.split("/"))) for k in keys}


def build_stations(cfg, name):
    slug = cfg.OUTPUTS.name
    _need(cfg.GTFS_ZIP, "the GTFS feed", slug)
    _need(cfg.CITY_BOUNDARY_GEOJSON, "the commune boundary", slug)
    _need(cfg.METRO_COMMUNES_GEOJSON, "the EPCI commune contours", slug)
    cfg.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(cfg.GTFS_ZIP)
    key_of = _routes(cfg, z)
    plat, st, non_rev, dropped = pure_extract(cfg, z, key_of)
    print(f"\n  {len(plat)} platforms -> {len(st)} stations under the pure-extract rule")
    if non_rev:
        print(f"  {len(non_rev)} non-revenue or fictitious stop(s) dropped: {non_rev}")
    for gone, kept, d in dropped:
        print(f"  same-name pair {d} m apart (Licence Ouverte rule): kept {kept!r}, dropped {gone!r}")

    per_line = _per_line(st, cfg.LINE_KEYS)
    osm = osm_stop_counts(cfg)
    if osm:
        print("\n  OpenStreetMap, stop members of the most complete relation per ref "
              "(gate 3's independent count; copy to OPERATOR_STATION_COUNTS once read):")
        for k in cfg.LINE_KEYS:
            ref = cfg.OSM_REFS.get(k, k)
            print(f"    {cfg.LINE_NAMES[k]:<16} OSM {osm.get(ref, 'absent')!s:>6}   feed {per_line[k]:>4}")
    print("\n  stations per line, network-wide:")
    for k in cfg.LINE_KEYS:
        exp = cfg.EXPECTED_STATIONS_PER_LINE.get(k)
        print(f"    {cfg.LINE_NAMES[k]:<16} {per_line[k]:>4}"
              + ("" if per_line[k] == exp else f"   <- config expects {exp}"))
    if per_line != cfg.EXPECTED_STATIONS_PER_LINE:
        sys.exit("the network has changed shape since the config was written: "
                 "re-measure, then update EXPECTED_STATIONS_PER_LINE deliberately")

    print()
    station_gates.verify_stations(
        city=name, platforms=plat, stations=st, crs_projected=cfg.CRS_PROJECTED,
        non_revenue=len(non_rev),
        spacing_min=getattr(cfg, "STATION_SPACING_MIN", TRAM_SPACING_MIN_M),
        expected_per_line=cfg.OPERATOR_STATION_COUNTS or None,
        actual_per_line=per_line)
    print(f"    gate 3 source: {cfg.OPERATOR_COUNTS_SOURCE}")

    g = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                         crs=cfg.CRS_GEOGRAPHIC)
    communes = gpd.read_file(cfg.METRO_COMMUNES_GEOJSON).to_crs(cfg.CRS_GEOGRAPHIC)
    j = gpd.sjoin(g, communes[["code", "nom", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated()]
    g["commune"], g["commune_nom"] = j["code"], j["nom"]

    if cfg.SCOPE == "regional":
        keep = g
        served = (g.dropna(subset=["commune"]).groupby(["commune", "commune_nom"])
                  .size().sort_values(ascending=False))
        outside = g[g["commune"].isna()]
        if len(outside):
            sys.exit(f"{len(outside)} station(s) lie in no EPCI commune: "
                     f"{sorted(outside['station'])}")
        got = {c: n for (c, n), _ in served.items()}
        print(f"\n  {len(got)} communes served:")
        for (c, n), k in served.items():
            print(f"    {c} {n:<28} {k:>3}")
        if set(got) != set(cfg.EXPECTED_SERVED_COMMUNES):
            sys.exit(f"the served communes changed.\n  gained: "
                     f"{sorted(set(got) - set(cfg.EXPECTED_SERVED_COMMUNES))}\n  lost: "
                     f"{sorted(set(cfg.EXPECTED_SERVED_COMMUNES) - set(got))}")
        pd.DataFrame([{"commune": c, "name": n, "stations": int(k)}
                      for (c, n), k in served.items()]).to_csv(
            cfg.SERVED_COMMUNES_CSV, index=False, encoding="utf-8")
        area = unary_union(list(communes[communes["code"].isin(got)].geometry))
        cfg.SERVED_BOUNDARY_GEOJSON.write_text(json.dumps(
            {"type": "Feature", "properties": {"communes": sorted(got)},
             "geometry": area.__geo_interface__}), encoding="utf-8")
        print(f"  served communes -> {cfg.SERVED_COMMUNES_CSV.relative_to(cfg.ROOT)}")
    else:
        boundary = shape(json.loads(cfg.CITY_BOUNDARY_GEOJSON.read_bytes())["geometry"])
        inside = g.within(boundary)
        keep, out = g[inside].copy(), g[~inside].copy()
        inside_per_line = _per_line(keep, cfg.LINE_KEYS)
        print(f"\n  commune {cfg.BOUNDARY_COMMUNE_CODE}: {len(keep)} inside, {len(out)} outside")
        for k in cfg.LINE_KEYS:
            exp = cfg.EXPECTED_INSIDE_PER_LINE.get(k)
            print(f"    {cfg.LINE_NAMES[k]:<16} {inside_per_line[k]:>3} of {per_line[k]:>3}"
                  + ("" if inside_per_line[k] == exp else f"   <- config expects {exp}"))
        if inside_per_line != cfg.EXPECTED_INSIDE_PER_LINE:
            sys.exit("the commune boundary keeps a different set: scope is a "
                     "decision, not a side effect - re-take it with the owner")
        places = getattr(cfg, "EXCLUDED_STATION_PLACES", {})
        rows = []
        for _, r in out.iterrows():
            if pd.notna(r["commune"]):
                where = f"in {r['commune_nom']} ({r['commune']}), outside commune {cfg.BOUNDARY_COMMUNE_CODE}"
            elif r["station"] in places:
                where = f"in {places[r['station']]}, outside commune {cfg.BOUNDARY_COMMUNE_CODE}"
            else:
                sys.exit(f"{r['station']} lies outside every EPCI commune and has no "
                         f"entry in config.EXCLUDED_STATION_PLACES")
            rows.append({"stop_id": r["stop_id"], "station": r["station"],
                         "lines": r["lines"], "reason": where,
                         "latitude": r["latitude"], "longitude": r["longitude"]})
        ex = pd.DataFrame(rows, columns=["stop_id", "station", "lines", "reason",
                                         "latitude", "longitude"])
        ex.sort_values(["reason", "station"]).to_csv(cfg.EXCLUDED_STATIONS_CSV,
                                                     index=False, encoding="utf-8")
        for _, r in ex.sort_values(["reason", "station"]).iterrows():
            print(f"    excluded: {r['station']:<30} {r['lines']:<8} {r['reason']}")

    nn = station_gates.nearest_neighbour_m(keep["longitude"], keep["latitude"],
                                           cfg.CRS_PROJECTED)
    print(f"\n  spacing in scope (nearest neighbour, m): min {nn.min():,.0f}  "
          f"median {np.median(nn):,.0f}  mean {nn.mean():,.0f}  max {nn.max():,.0f}")
    out = (keep[["stop_id", "station", "lines", "latitude", "longitude"]]
           .sort_values("station"))
    out.to_csv(cfg.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} stations -> {cfg.STATIONS_CSV.relative_to(cfg.ROOT)}")
    emit("platforms", len(plat))
    emit("stations_network", len(st))
    emit("stations_in_scope", len(out))
    for k in cfg.LINE_KEYS:
        emit(f"stations_line_{k}", per_line[k])


# --- step 3 ---------------------------------------------------------------

def _gtfs_line_shapes(cfg):
    """Rennes's shape chooser, by line key: the fewest most-used shapes that
    cover every stop the line serves (a branch takes a second shape)."""
    from pipeline.map_common import load_line_shapes
    with zipfile.ZipFile(cfg.GTFS_ZIP) as zf:
        routes = _read(zf, "routes.txt")
        key_of = dict(zip(routes["route_id"], routes["route_short_name"]))
        trips = _read(zf, "trips.txt", usecols=["route_id", "trip_id", "shape_id"])
        trips = trips[trips["route_id"].isin(cfg.ROUTE_IDS)].dropna(subset=["shape_id"])
        st = _served_stop_times(zf, trips)
        stops = _read(zf, "stops.txt")
    # Split by branch where ROUTE_BRANCHES says so; a trunk trip counts for
    # every branch, and its shape stays a candidate for each.
    trips = trips.merge(_trip_lines(cfg, trips, st, stops, key_of)
                        .rename(columns={"line": "key"}), on="trip_id")
    link = st.merge(trips[["trip_id", "key", "shape_id"]], on="trip_id")
    shape_stops = link.groupby(["key", "shape_id"])["stop_id"].agg(set).to_dict()
    shape_trips = trips.groupby(["key", "shape_id"])["trip_id"].count().to_dict()
    key_stops = link.groupby("key")["stop_id"].agg(set).to_dict()
    specs = {}
    for k in cfg.LINE_KEYS:
        ranked = sorted((s for s in shape_trips if s[0] == k),
                        key=lambda s: (-shape_trips[s], s[1]))
        picked, covered = [], set()
        for s in ranked:
            if picked and not (shape_stops[s] - covered):
                continue
            picked.append(s[1])
            covered |= shape_stops[s]
            if covered >= key_stops.get(k, set()):
                break
        if not picked:
            sys.exit(f"no shape covers {cfg.LINE_NAMES[k]}: a drawn line needs real geometry")
        print(f"  {cfg.LINE_NAMES[k]:16s} {len(picked)} shape(s) covering "
              f"{len(covered)}/{len(key_stops.get(k, ()))} stops")
        specs[k] = (tuple(picked), cfg.LINE_COLOURS[k], cfg.LINE_NAMES[k],
                    getattr(cfg, "LINE_LABEL_ENDS", {}).get(k))
    return load_line_shapes(cfg.GTFS_ZIP, specs, cfg.MAP_SYSTEM_NAME)


def _osm_line_shapes(cfg):
    from pipeline.map_common import load_osm_line_shapes
    specs = {k: (cfg.OSM_REFS[k], cfg.LINE_COLOURS[k], cfg.LINE_NAMES[k],
                 getattr(cfg, "LINE_LABEL_ENDS", {}).get(k)) for k in cfg.LINE_KEYS}
    return load_osm_line_shapes(cfg.OSM_ROUTES_JSON, specs, cfg.MAP_SYSTEM_NAME)


def render(cfg, name):
    from pipeline.map_common import render_heatmap
    for path in (cfg.STATIONS_CSV, cfg.BUSINESSES_CLEAN_CSV, cfg.GTFS_ZIP,
                 cfg.CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    print("Line geometry (" + cfg.LINE_GEOMETRY + "):")
    lines = _osm_line_shapes(cfg) if cfg.LINE_GEOMETRY == "osm" else _gtfs_line_shapes(cfg)
    missing = sorted(set(cfg.LINE_KEYS) - set(lines))
    if missing:
        sys.exit(f"no geometry for {missing}: every drawn line needs real geometry, "
                 f"a label and a legend entry")
    focus_path = (cfg.SERVED_BOUNDARY_GEOJSON if cfg.SCOPE == "regional"
                  else cfg.CITY_BOUNDARY_GEOJSON)
    focus = shape(json.loads(focus_path.read_text(encoding="utf-8"))["geometry"])
    stations = pd.read_csv(cfg.STATIONS_CSV)
    businesses = pd.read_csv(cfg.BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts")
    render_heatmap(
        output_path=cfg.HEATMAP_HTML,
        map_title=f"{name} {cfg.MAP_SYSTEM_NAME} Business Density Heatmap",
        city_name=name,
        system_name=cfg.MAP_SYSTEM_NAME,
        stations=stations,
        businesses=businesses,
        taxonomy_system=cfg.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=cfg.CRS_GEOGRAPHIC,
        crs_projected=cfg.CRS_PROJECTED,
        ring_edges_meters=cfg.RING_EDGES_METERS,
        ring_labels=cfg.RING_LABELS,
        label_focus=focus,
    )
