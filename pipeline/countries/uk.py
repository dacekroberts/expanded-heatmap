"""Steps 1 to 3 for the UK's tram and light-rail cities on the FSA register
(the UK six, 2026-10-02; Manchester (Regional) is the pilot, and the five after
it are config on this contract). A city's step files call `step1(config)`,
`step2(config)` and `step3(config, ...)` and nothing else. Reads the cache only;
`uk_fetch.py` downloads.

STEP 1 - lines and stations from OpenStreetMap, on `pipeline/osm_tram.py`:
  1. every route relation on `config.OSM_ROUTES` in the cache is KEPT by its
     ref (`config.OSM_REFS`) or named in `config.NOT_DRAWN` with a reason;
     osm_tram exits otherwise. A relation with no `ref` (Edinburgh's) takes
     one from `config.REF_BY_RELATION`, by id;
  2. their stop members, collapsed by name at the mean (Aarhus's rule) within
     `config.COLLAPSE_MAX_SPREAD_M`;
  3. **gate 3, twice, both independent of OSM** (the tram-city rule): the
     operator's own counts (`config.OPERATOR_STATION_COUNTS`, per line or for
     the whole network) and **NaPTAN** (DfT; owner, 2026-10-01): the active
     MET records with the network's ATCO prefixes inside the scope, matched
     NAME BY NAME against the stations in scope. A difference not explained in
     `config.NAPTAN_EXPLAINED` stops the step;
  4. the light-rail test's track figures, printed for the record: the share
     of the kept track tagged `railway=light_rail` or `tram`, and in tunnel or
     on a bridge (`docs/tram_city_list.md`);
  5. scope: the union of the boundary polygons, with the median gap checked
     against `config.MEDIAN_GAP_BOUNDS_M` (the spacing rule: the ring edges
     were chosen on it);
  6. the drawn geometry to `config.LINES_GEOJSON`. Either each line's kept
     relations merged by London's branch rule (`config.LINE_OSM_REFS`), or,
     where OSM's service relations no longer match the operator's lines
     (Manchester, after TfGM's 14 September 2026 change), each line ROUTED
     over the kept relations' track through the operator's own stop sequence
     (`config.LINE_STOPS`).

STEP 2 - Newcastle's step 2: the FSA files through `pipeline/fsa.py` (the
read list, the flat, childminder and trading-as rules), London's storefront
filter and Code-Point centroid tier, and the scope polygon.

STEP 3 - the map, through `map_common.render_heatmap()`, unforked.
"""
import heapq
import json
import math
import re
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, mapping
from shapely.ops import linemerge, unary_union

from pipeline import fsa
from pipeline import osm_tram
from pipeline import stations as station_gates
from pipeline.baseline import emit

NETWORK = "network"   # the OPERATOR_STATION_COUNTS key for a whole-network count
BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000
HOP_MAX_M = 6000      # a routed hop longer than this is a wrong anchor, not a line
ANCHOR_SLACK_M = 40   # a station's anchors: track vertices up to this much further than its nearest


def fetch_hint(config):
    return f"pipeline/{config.SLUG}/fetch_sources.py"


def norm_name(s):
    """A stop name for matching across OSM, NaPTAN and an operator's list:
    the network suffix NaPTAN appends, "Tram Stop", "&", apostrophes, spaces
    and case all dropped ("Besses o'th'Barn (Manchester Metrolink)" against
    OSM's "Besses o' th' Barn")."""
    s = s.replace("’", "'").replace("&", "and")
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    s = re.sub(r"(?i)\s+(tram stop|tram|metrolink stop|metrolink)$", "", s)
    return re.sub(r"[^0-9a-z]", "", s.casefold())


def boundary(config):
    if not config.CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.CITY_BOUNDARY_GEOJSON}\nRun: python {fetch_hint(config)}")
    return gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs("EPSG:4326")


def elements(config):
    els = osm_tram.read_elements(config.OSM_JSON, "OSM routes, ways and stops", fetch_hint(config))
    for e in els:
        rid = getattr(config, "REF_BY_RELATION", {}).get(e.get("id")) if e["type"] == "relation" else None
        if rid is not None:
            if "ref" in e.get("tags", {}):
                sys.exit(f"REF_BY_RELATION names relation {e['id']}, which now has ref "
                         f"{e['tags']['ref']!r} in OSM - use it and remove the entry")
            e["tags"]["ref"] = rid
    return els


def _track(rel):
    """A relation's track ways - never its `platform` outlines."""
    return [m for m in rel.get("members", []) if m.get("type") == "way"
            and len(m.get("geometry") or []) >= 2 and not m.get("role", "").startswith("platform")]


def light_rail_test(kept, els, crs):
    """The track half of the light-rail test, over the kept relations' track."""
    tags = {e["id"]: e.get("tags", {}) for e in els if e["type"] == "way"}
    to_m = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    seen, by = set(), {}
    for rels in kept.values():
        for r in rels:
            for m in _track(r):
                if m["ref"] in seen:
                    continue
                seen.add(m["ref"])
                xy = [to_m.transform(p["lon"], p["lat"]) for p in m["geometry"]]
                km = sum(math.dist(a, b) for a, b in zip(xy, xy[1:])) / 1000
                t = tags.get(m["ref"], {})
                kind = t.get("railway", "?")
                raised = "tunnel" if t.get("tunnel") not in (None, "no") else (
                    "bridge" if t.get("bridge") not in (None, "no") else "")
                by[(kind, raised)] = by.get((kind, raised), 0.0) + km
    total = sum(by.values())
    kinds = {}
    for (k, _), km in by.items():
        kinds[k] = kinds.get(k, 0.0) + km
    raised = sum(km for (_, r), km in by.items() if r)
    print(f"\n  the light-rail test, track ({len(seen)} ways, {total:.1f} km of route "
          f"track, each way counted once):")
    print("    " + ", ".join(f"railway={k} {km / total:.0%}" for k, km in
                             sorted(kinds.items(), key=lambda kv: -kv[1])))
    print(f"    in tunnel or on a bridge: {raised / total:.1%}")
    return {"track_km": round(total, 1), "tunnel_bridge_share": round(raised / total, 3),
            "railway_share": {k: round(km / total, 3) for k, km in kinds.items()}}


def merged_lines(config, kept):
    """Each line's kept relations merged by London's branch rule: the longest
    first, another only where it adds real new track."""
    feats = []
    for key, refs in config.LINE_OSM_REFS.items():
        mine = [r for ref in refs for r in kept.get(ref, [])]
        if not mine:
            sys.exit(f"{key}: no kept relation with ref(s) {refs}")
        geoms = {}
        for r in mine:
            ways = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]]) for m in _track(r)]
            geoms[r["id"]] = gpd.GeoSeries([unary_union(ways)], crs="EPSG:4326").to_crs(
                config.CRS_PROJECTED).iloc[0]
        chosen, covered = [], None
        for rid in sorted(geoms, key=lambda i: -geoms[i].length):
            g = geoms[rid]
            new = g if covered is None else g.difference(covered.buffer(BRANCH_NEAR_M))
            if new.length >= BRANCH_MIN_NEW_M:
                chosen.append(rid)
                covered = g if covered is None else covered.union(new)
        merged = linemerge(covered) if covered.geom_type == "MultiLineString" else covered
        merged = gpd.GeoSeries([merged], crs=config.CRS_PROJECTED).to_crs("EPSG:4326").iloc[0]
        parts = [p for p in getattr(merged, "geoms", [merged]) if p.length > 0]
        print(f"    {key:<12} {len(chosen)} of {len(mine)} relations, {covered.length / 1000:6.1f} km")
        feats.append({"type": "Feature", "properties": {"line": key, "osm_refs": list(refs)},
                      "geometry": mapping(MultiLineString(parts))})
    return feats


def routed_lines(config, kept, stations, seqs):
    """Each operator line routed over the kept relations' track, stop to stop
    in the operator's own order, by the shortest path along the track.

    The graph's vertices are the ways' shared coordinates (OSM ways meet at a
    shared node, so at an identical coordinate). Double track is two ways, one
    per direction, joined only at crossovers, so a station anchors at EVERY
    track vertex within ANCHOR_SLACK_M of its nearest one (both tracks), and a
    hop is the shortest path between any of the two stations' anchors. Each
    hop is drawn as its own part. A hop over HOP_MAX_M stops the step."""
    to_m = Transformer.from_crs("EPSG:4326", config.CRS_PROJECTED, always_xy=True)
    to_ll = Transformer.from_crs(config.CRS_PROJECTED, "EPSG:4326", always_xy=True)
    vid, xy, adj = {}, [], {}

    def vertex(p):
        k = (round(p["lon"], 7), round(p["lat"], 7))
        if k not in vid:
            vid[k] = len(xy)
            xy.append(to_m.transform(p["lon"], p["lat"]))
        return vid[k]
    seen = set()
    for rels in kept.values():
        for r in rels:
            for m in _track(r):
                if m["ref"] in seen:
                    continue
                seen.add(m["ref"])
                vs = [vertex(p) for p in m["geometry"]]
                for a, b in zip(vs, vs[1:]):
                    if a != b:
                        d = math.dist(xy[a], xy[b])
                        adj.setdefault(a, {})[b] = d
                        adj.setdefault(b, {})[a] = d
    pts = np.array(xy)
    sxy = np.array([to_m.transform(lo, la) for lo, la in zip(stations["longitude"], stations["latitude"])])
    anchors = {}
    for name, (x, y) in zip(stations["stop_name"], sxy):
        d = np.hypot(pts[:, 0] - x, pts[:, 1] - y)
        if d.min() > 150:
            sys.exit(f"{name}: the nearest drawn track is {d.min():.0f} m away")
        anchors[name] = set(np.flatnonzero(d <= d.min() + ANCHOR_SLACK_M).tolist())

    def path(srcs, dsts):
        dist, prev = {a: 0.0 for a in srcs}, {}
        todo = [(0.0, a) for a in srcs]
        heapq.heapify(todo)
        end = None
        while todo:
            d, u = heapq.heappop(todo)
            if d > dist[u]:
                continue
            if u in dsts:
                end = u
                break
            for v, w in adj.get(u, {}).items():
                if d + w < dist.get(v, math.inf):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(todo, (d + w, v))
        if end is None:
            return None, math.inf
        out = [end]
        while out[-1] not in srcs:
            out.append(prev[out[-1]])
        return out[::-1], dist[end]

    feats = []
    for key, seq in seqs.items():
        parts, total = [], 0.0
        for s, t in zip(seq, seq[1:]):
            vs, d = path(anchors[s], anchors[t])
            if vs is None or d > HOP_MAX_M:
                sys.exit(f"{key}: no track path of under {HOP_MAX_M} m from {s} to {t} "
                         f"({d:.0f} m)")
            total += d
            if len(vs) > 1:
                parts.append(LineString([to_ll.transform(*xy[v]) for v in vs]))
        merged = linemerge(MultiLineString(parts))
        merged = list(getattr(merged, "geoms", [merged]))
        print(f"    {key:<12} {len(seq):>3} stops, routed {total / 1000:6.1f} km in "
              f"{len(merged):>2} part(s)  {seq[0]} - {seq[-1]}")
        feats.append({"type": "Feature", "properties": {"line": key, "routed": True},
                      "geometry": mapping(MultiLineString(merged))})
    return feats


def naptan_gate(config, inside):
    """Gate 3's second source: NaPTAN's active MET records (one per stop
    access area) with the network's ATCO prefixes inside the scope, name by
    name against the stations in scope."""
    frames = []
    for code in config.NAPTAN_ATCO_AREAS:
        p = config.NAPTAN_RAW_DIR / f"{code}.csv"
        if not p.exists():
            sys.exit(f"missing {p}\nRun: python {fetch_hint(config)}")
        frames.append(pd.read_csv(p, dtype=str, low_memory=False,
                                  usecols=["ATCOCode", "CommonName", "StopType", "Status",
                                           "Longitude", "Latitude"]))
    na = pd.concat(frames)
    na = na[(na["StopType"] == "MET") & (na["Status"] == "active")
            & na["ATCOCode"].str.startswith(tuple(config.NAPTAN_PREFIXES))]
    pts = gpd.GeoSeries(gpd.points_from_xy(pd.to_numeric(na["Longitude"]), pd.to_numeric(na["Latitude"])),
                        index=na.index, crs="EPSG:4326")
    area = boundary(config).union_all()
    na = na[pts.within(area)]
    aliases = {norm_name(k): norm_name(v) for k, v in getattr(config, "NAPTAN_NAME_ALIASES", {}).items()}
    nap = {aliases.get(norm_name(n), norm_name(n)): n for n in na["CommonName"]}
    built = {norm_name(n): n for n in inside["stop_name"]}
    explained = {norm_name(k): v for k, v in getattr(config, "NAPTAN_EXPLAINED", {}).items()}
    only_n = sorted(set(nap) - set(built))
    only_b = sorted(set(built) - set(nap))
    print(f"\n  gate 3, NaPTAN: {len(na)} active MET records ({', '.join(config.NAPTAN_PREFIXES)}) "
          f"inside the scope, {len(nap)} names; {len(built)} stations built")
    bad = []
    for k in only_n:
        why = explained.get(k)
        print(f"    NaPTAN only: {nap[k]!r}" + (f" - {why}" if why else "  <- UNEXPLAINED"))
        if not why:
            bad.append(nap[k])
    for k in only_b:
        why = explained.get(k)
        print(f"    built only:  {built[k]!r}" + (f" - {why}" if why else "  <- UNEXPLAINED"))
        if not why:
            bad.append(built[k])
    stale = sorted(set(explained) - set(only_n) - set(only_b))
    if stale:
        sys.exit(f"NAPTAN_EXPLAINED names {stale}, which now match - remove the entries")
    if bad:
        sys.exit(f"gate 3 (NaPTAN): {len(bad)} unexplained difference(s): {bad} - a station "
                 f"fix or an entry in NAPTAN_EXPLAINED with its reason, never a looser match")
    print(f"    {len(set(nap) & set(built))} names match")
    return len(nap)


def step1(config):
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached inputs:")
    els = elements(config)
    places = boundary(config)
    area = places.union_all()
    refs = tuple(config.OSM_REFS)
    kept = osm_tram.select_relations(els, routes=config.OSM_ROUTES, refs=refs,
                                     operator=getattr(config, "OPERATOR", None),
                                     not_drawn=config.NOT_DRAWN, verbose=False)
    q = osm_tram.stop_rows(els, routes=config.OSM_ROUTES, refs=refs,
                           operator=getattr(config, "OPERATOR", None),
                           not_drawn=config.NOT_DRAWN,
                           station_add=getattr(config, "STATION_ADD", None),
                           name_aliases=getattr(config, "STATION_NAME_ALIASES", None),
                           accept_members=getattr(config, "ACCEPT_MEMBERS", None))
    platforms, st = osm_tram.collapse(q, refs=refs, crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=getattr(config, "COLLAPSE_MAX_SPREAD_M", 200))

    # The lines each station is on: the operator's own sequences where the
    # config gives them, otherwise the line keys of its OSM refs.
    if getattr(config, "LINE_STOPS", None):
        op_alias = {norm_name(k): norm_name(v) for k, v in getattr(config, "LINE_STOP_ALIASES", {}).items()}
        by_norm = {norm_name(n): n for n in st["stop_name"]}
        seqs, missing = {}, []
        for key, seq in config.LINE_STOPS.items():
            seqs[key] = []
            for s in seq:
                k = op_alias.get(norm_name(s), norm_name(s))
                if k not in by_norm:
                    missing.append(f"{key}: {s}")
                else:
                    seqs[key].append(by_norm[k])
        if missing:
            sys.exit(f"operator stop(s) with no OSM station: {missing}")
        on = {n: [k for k in config.LINE_STOPS if n in seqs[k]] for n in st["stop_name"]}
        orphan = sorted(n for n, ks in on.items() if not ks)
        if orphan:
            sys.exit(f"OSM station(s) on no operator line: {orphan}")
        st["lines"] = st["stop_name"].map(lambda n: "/".join(on[n]))
        line_keys = list(config.LINE_STOPS)
    else:
        key_of = {ref: key for key, rs in config.LINE_OSM_REFS.items() for ref in rs}
        st["lines"] = st["lines"].map(lambda s: "/".join(dict.fromkeys(
            key_of[r] for r in s.split("/"))))
        line_keys = list(config.LINE_OSM_REFS)

    # Gate 3, the operator: counted over the whole network, before the scope.
    print()
    actual = {k: (len(st) if k == NETWORK else
                  int(st["lines"].str.split("/").apply(lambda ls: k in ls).sum()))
              for k in config.OPERATOR_STATION_COUNTS}
    res = station_gates.verify_stations(
        city=config.CITY_NAME, platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the operator's own count - "
                 + "; ".join(f"{line}: build {b}, operator {o}"
                             for line, (b, o) in res["per_line_mismatches"].items()))

    test = light_rail_test(kept, els, config.CRS_PROJECTED)

    pts = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                           crs="EPSG:4326")
    inside_mask = pts.within(area)
    inside, outside = st[inside_mask.values].copy(), st[~inside_mask.values].copy()
    print(f"\n  scope ({config.SCOPE_LABEL}): {len(inside)} inside, {len(outside)} outside")
    n_naptan = naptan_gate(config, inside)

    nn = gpd.GeoSeries(gpd.points_from_xy(inside["longitude"], inside["latitude"]),
                       crs="EPSG:4326").to_crs(config.CRS_PROJECTED)
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing in scope (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m, outside {lo:.0f}-{hi:.0f} m, where "
                 f"the ring edges were chosen - re-take the ring decision")

    print("\n  lines drawn:")
    if getattr(config, "LINE_STOPS", None):
        feats = routed_lines(config, kept, st, seqs)
    else:
        feats = merged_lines(config, kept)
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")

    ex = (outside.rename(columns={"stop_name": "station"})
          .assign(reason=f"outside {config.SCOPE_LABEL}")
          [["station", "lines", "reason", "latitude", "longitude"]].sort_values("station"))
    ex.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station")
            .reset_index(drop=True))
    keep.insert(0, "stop_id", keep["station"])
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(ex)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    print(f"  per line: " + ", ".join(
        f"{k} {int(keep['lines'].str.split('/').apply(lambda ls: k in ls).sum())}" for k in line_keys))

    emit("stop_positions", len(platforms))
    emit("stations_in_scope", len(keep))
    emit("naptan_in_scope", n_naptan)
    emit("median_gap_m", int(round(d.median())))
    return test


def step2(config, tax_module):
    """The FSA files -> the food storefronts placed inside the scope."""
    from pipeline.taxonomies import filter_to_storefront

    TAX = tax_module
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    files = [config.FSA_RAW_DIR / f"{code}.xml" for code in config.FSA_AUTHORITIES]
    if len(files) != config.FSA_AUTHORITY_COUNT:
        sys.exit(f"{len(files)} FSA authorities, expected exactly {config.FSA_AUTHORITY_COUNT}")
    missing = [f.name for f in files if not f.exists()]
    if missing:
        sys.exit(f"missing {missing}: run python {fetch_hint(config)}")
    df = fsa.load(files)
    print(f"  {len(df):,} register rows in {df['LocalAuthorityName'].nunique()} authorities")
    emit("register_rows", len(df))
    unknown = sorted(set(df["BusinessType"]) - TAX.KNOWN_TYPES)
    if unknown:
        sys.exit(f"  business type(s) the taxonomy does not know: {unknown}")
    if df["FHRSID"].duplicated().any():
        sys.exit(f"  {df['FHRSID'].duplicated().sum()} duplicate FHRSIDs")

    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")
    print("    " + ", ".join(f"{t} {n:,}" for t, n in df["BusinessType"].value_counts().items()))
    emit("storefront_rows", len(df))
    df = fsa.drop_home_premises(df)

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.assign(latitude=lat, longitude=lon, placement="fsa_point")
    no_point = df["latitude"].isna() | df["longitude"].isna()
    print(f"\n  {int(no_point.sum()):,} without the FSA's own point ({no_point.mean():.1%})")

    pc = df["PostCode"].str.upper().str.strip()
    full = pc.str.match(fsa.FULL_POSTCODE)
    outward = no_point & pc.str.match(fsa.OUTWARD_POSTCODE)
    joinable = pd.Series(False, index=df.index)
    if config.PLACE_AT_CENTROIDS:
        # Tier 2: the postcode unit's centroid (OS Code-Point Open), for a FULL
        # postcode only, kept to the scope's GSS codes.
        cp = fsa.codepoint(config.CODEPOINT_ZIP, config.CODEPOINT_DISTRICTS, config.CODEPOINT_CRS,
                           "EPSG:4326", f"python {fetch_hint(config)}")
        key = pc.str.replace(r"\s+", "", regex=True)
        joinable = no_point & full & key.isin(cp.index)
        ll = cp.loc[key[joinable], ["latitude", "longitude"]].to_numpy()
        df.loc[joinable, ["latitude", "longitude"]] = ll
        df.loc[joinable, "placement"] = "postcode_centroid"
        print(f"    placed at their postcode's centroid: {int(joinable.sum()):,}")
        print(f"    full postcode not in Code-Point (left unplaced): {int((no_point & full & ~joinable).sum()):,}")
    else:
        print(f"    with a full postcode, not placed (no centroid tier): {int((no_point & full).sum()):,}")
    print(f"    outward code only - a private address, never placed: {int(outward.sum()):,}")
    print(f"    no usable postcode (left unplaced): {int((no_point & ~full & ~outward).sum()):,}")
    unplaced = no_point & ~joinable
    print(f"  {int(unplaced.sum()):,} NOT placed ({unplaced.mean():.1%}); by authority:")
    by = df.assign(u=unplaced).groupby("LocalAuthorityName")["u"].agg(["sum", "mean"])
    for name, r in by.sort_values("mean", ascending=False).iterrows():
        print(f"    {name:<26} {int(r['sum']):>5,} ({r['mean']:.1%})")
    emit("not_placed", int(unplaced.sum()))
    emit("placed_at_centroid", int(joinable.sum()))
    df = df[~unplaced]

    box = config.BUSINESS_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    area = boundary(config).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs="EPSG:4326").to_crs(config.CRS_PROJECTED)
    inside = pts.within(area)
    print(f"  {int((~inside).sum()):,} outside {config.SCOPE_LABEL}, dropped")
    df = df[inside]

    df = fsa.trade_names(df)

    out = df.rename(columns={"FHRSID": "fhrsid", "BusinessName": "business_name",
                             "LocalAuthorityName": "authority"})[
        ["fhrsid", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "authority", "placement"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    bucket = out[TAX.VALUE_COLUMN].map(lambda v: TAX.classify({TAX.VALUE_COLUMN: v}))
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    counts = bucket.value_counts()
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in counts.items()))
    emit("storefronts_placed", len(out))
    for b, n in counts.items():
        emit(f"bucket_{b.lower().replace(' ', '_')}", int(n))
    print(f"  placement: " + ", ".join(f"{k} {v:.1%}" for k, v in
                                       out["placement"].value_counts(normalize=True).items()))


def step3(config, *, system_name, map_title, label_ends=None):
    from pipeline.map_common import load_geojson_line_shapes, render_heatmap

    for path in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    label_ends = label_ends or {}
    specs = {key: (key, config.LINE_COLOURS[key], config.LINE_NAMES[key], label_ends.get(key))
             for key in config.LINE_ORDER}
    render_heatmap(
        output_path=config.HEATMAP_HTML,
        map_title=map_title,
        city_name=config.CITY_NAME,
        system_name=system_name,
        stations=pd.read_csv(config.STATIONS_CSV),
        businesses=pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype={"fhrsid": str}),
        taxonomy_system=config.TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(config.LINES_GEOJSON, specs, system_name),
        crs_geographic="EPSG:4326",
        crs_projected=config.CRS_PROJECTED,
        ring_edges_meters=config.RING_EDGES_METERS,
        ring_labels=config.RING_LABELS,
        label_focus=boundary(config).union_all(),
        legend_names=config.LEGEND_NAMES,
    )
