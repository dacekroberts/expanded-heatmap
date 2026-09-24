"""Step 1 for a Brazilian city whose rail comes from OpenStreetMap - shared,
written once before the second OSM city (osm-rail's meta-lesson: a lesson in
one city's code does not reach the next). Reads the cache only.

The config supplies:
  OSM_RAIL_JSON, OSM_MUNICIPIOS_JSON      the fetch's two caches
  LINE_RELATIONS  {line key: (relation ids)}   the WHITELIST - by id, because a
                  `ref` can be shared (Rome's B1 is tagged B), absent (Recife's
                  second Cabo relation) or a sentence
  LEFT_OUT        {relation id: reason}    every OTHER relation in the cache,
                  named, or step 1 STOPS - a new relation is a scope question
  LINE_ORDER, LINE_NAMES, STATION_NAME_ALIASES
  COLLAPSE_MAX_SPREAD_M, SPACING_MIN_M
  GATE3 = {"lines": {line key: n}, "network": n, "source": "..."}
  SCOPE_CODES, SCOPE_AREA_KM2, CRS_*, NAME, IBGE label for the scope

Stations are the named `stop*` members of the whitelisted relations (membership
is the evidence - osm-rail), collapsed by name across directions and lines with
every spread printed and capped. An unnamed stop member is skipped and counted,
never guessed; gate 3 is what catches a station lost that way. Every station
outside the scope goes to excluded_stations.csv naming its município.
"""
import json
import sys

import geopandas as gpd
import pandas as pd

from pipeline import stations as station_gates
from pipeline.baseline import emit
from pipeline.countries.brazil_boundary import in_codes, municipios, scope_polygon


def _elements(cfg):
    if not cfg.OSM_RAIL_JSON.exists():
        sys.exit(f"missing {cfg.OSM_RAIL_JSON}\nRun the city's fetch_sources.py first.")
    return json.loads(cfg.OSM_RAIL_JSON.read_text(encoding="utf-8"))["elements"]


def stop_rows(cfg):
    els = _elements(cfg)
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = {e["id"]: e for e in els if e["type"] == "relation"}
    line_of = {rid: ln for ln, ids in cfg.LINE_RELATIONS.items() for rid in ids}
    unknown = sorted(set(rels) - set(line_of) - set(cfg.LEFT_OUT))
    if unknown:
        sys.exit(f"OSM route relations neither drawn nor recorded as left out: "
                 f"{[(r, rels[r]['tags'].get('name')) for r in unknown]}")
    missing = sorted(set(line_of) - set(rels))
    if missing:
        sys.exit(f"whitelisted relation(s) missing from the cache: {missing} - a scope question")
    print("  route relations:")
    rows, unnamed, named_by_fallback = [], 0, set()
    for rid, r in sorted(rels.items(), key=lambda kv: (kv[1]["tags"].get("route", ""),
                                                       kv[1]["tags"].get("name", ""))):
        t = r["tags"]
        keep = rid in line_of
        print(f"    {'KEEP ' + line_of[rid] if keep else 'out':14} {rid:>9} "
              f"{t.get('route', ''):10} {t.get('name', '')[:52]}"
              f"{'' if keep else '  - ' + cfg.LEFT_OUT[rid]}")
        if not keep:
            continue
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            tags = (n or {}).get("tags", {})
            name = tags.get("name")
            if n and not name:
                # An unnamed stop position is named from the config (a name
                # read from its wikidata item) or its own wikipedia tag -
                # Santos's Ana Costa carries only `pt:Estação Ana Costa`.
                name = getattr(cfg, "NODE_NAMES", {}).get(n["id"])
                wp = tags.get("wikipedia", "")
                if not name and wp.startswith("pt:"):
                    name = wp[3:].removeprefix("Estação ").removeprefix("Estação de ")
                if name:
                    named_by_fallback.add((n["id"], name))
            if not n or not name:
                unnamed += 1
                continue
            rows.append({"line": line_of[rid], "node": n["id"],
                         "stop_name": cfg.STATION_NAME_ALIASES.get(name, name),
                         "latitude": n["lat"], "longitude": n["lon"]})
    for nid, nm in sorted(named_by_fallback):
        print(f"  stop {nid} has no name tag - named '{nm}' (config NODE_NAMES or its wikipedia tag)")
    if unnamed:
        print(f"  {unnamed} unnamed stop member(s) skipped - gate 3 catches a station lost this way")
    return pd.DataFrame(rows).drop_duplicates(["line", "node"])


def write_lines(cfg):
    """The whitelisted relations for step 3's load_osm_line_shapes, retagged
    with their line key as `ref`."""
    rels = {e["id"]: e for e in _elements(cfg) if e["type"] == "relation"}
    out = []
    for ln, ids in cfg.LINE_RELATIONS.items():
        for rid in ids:
            r = json.loads(json.dumps(rels[rid]))
            r["tags"]["ref"] = ln
            out.append(r)
    cfg.OSM_LINES_JSON.write_text(json.dumps({"elements": out}), encoding="utf-8")
    print(f"  line geometry -> {cfg.OSM_LINES_JSON.name} ({len(out)} relations)")


def build_stations(cfg):
    cfg.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)
    q = stop_rows(cfg)
    order = list(cfg.LINE_ORDER)
    lines_by_name = q.groupby("stop_name")["line"].agg(
        lambda s: " ".join(ln for ln in order if ln in set(s)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"],
                                                                platforms["latitude"]),
                         crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by name; widest:")
    for nm in spread.sort_values(ascending=False).head(5).index:
        print(f"    {nm:<40} {spread[nm]:>5.0f} m  [{lines_by_name[nm]}]")
    too_far = spread[spread > cfg.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {cfg.COLLAPSE_MAX_SPREAD_M} m: {too_far.round().to_dict()}")
    st = by_name.reset_index()
    st["lines"] = st["stop_name"].map(lines_by_name)

    actual = {cfg.LINE_NAMES[ln]: int(sum(1 for v in st["lines"] if ln in v.split()))
              for ln in cfg.GATE3["lines"]}
    expected = {cfg.LINE_NAMES[ln]: n for ln, n in cfg.GATE3["lines"].items()}
    if cfg.GATE3.get("network") is not None:
        actual["network"], expected["network"] = len(st), cfg.GATE3["network"]
    print()
    station_gates.verify_stations(
        city=cfg.NAME, platforms=platforms, stations=st, crs_projected=cfg.CRS_PROJECTED,
        spacing_min=cfg.SPACING_MIN_M, expected_per_line=expected, actual_per_line=actual)
    print(f"    gate 3 source: {cfg.GATE3['source']}")

    poly = scope_polygon(cfg.OSM_MUNICIPIOS_JSON, cfg.SCOPE_CODES, cfg.SCOPE_AREA_KM2,
                         cfg.CRS_PROJECTED, cfg.NAME)
    pts = gpd.GeoSeries(gpd.points_from_xy(st["longitude"], st["latitude"]),
                        crs=cfg.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    nb = municipios(cfg.OSM_MUNICIPIOS_JSON, cfg.CRS_GEOGRAPHIC)
    excluded = []
    for _, r in st[~inside].iterrows():
        pt = gpd.points_from_xy([r["longitude"]], [r["latitude"]])[0]
        hit = nb[nb.contains(pt) & ~nb["ibge"].map(lambda c: in_codes(c, cfg.SCOPE_CODES))]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} is outside the scope and in {len(hit)} recorded municípios")
        excluded.append({"station": r["stop_name"], "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['name']} ({hit.iloc[0]['ibge']}), "
                                   f"outside the scope ({', '.join(cfg.SCOPE_CODES)})",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        cfg.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  scope: {len(st)} stations -> {int(inside.sum())} inside, {len(excluded)} excluded")
    for x in excluded:
        print(f"    {x['station']:<34} [{x['lines']}] {x['reason']}")
    print("  per line, inside the scope:")
    for ln in order:
        n_all = int(sum(1 for v in st["lines"] if ln in v.split()))
        n_in = int(sum(1 for v, i in zip(st["lines"], inside) if i and ln in v.split()))
        print(f"    {cfg.LINE_NAMES[ln]:<32} {n_in:>3} of {n_all:>3}")
    keep = (st[inside].rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(cfg.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {cfg.STATIONS_CSV.name}")
    write_lines(cfg)
    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(excluded))
