"""Steps 1 and 3 for a Czech tram city whose trams come from OpenStreetMap -
Plzeň, Olomouc, Ostrava, Liberec (Regional) and Most (Regional).

Thin over the shared `pipeline/osm_tram.py` (the tram kits' module, controlled
on Aarhus) and `czechia_boundary.py`. A city's step files call `step1(config)`
and `step3(config, system_name)` and nothing else, as its step 2 calls
`czechia_register.build_storefronts`. Reads the cache only; `fetch_sources.py`
downloads.

STEP 1, in order:
  1. the operator's route=tram relations, every one KEPT (by ref) or named in
     the config's NOT_DRAWN with a reason - osm_tram exits otherwise;
  2. their stop members, collapsed by name at the mean within
     COLLAPSE_MAX_SPREAD_M (Aarhus's rule, the OSM rule: France's never-a-mean
     rule came from the French portal's conditions);
  3. the station gates (pipeline/stations.py) at the tram floor SPACING_MIN_M,
     with gate 3 where the config names an independent count;
  4. scope over the obce (one or two), asserted against
     EXPECTED_INSIDE_PER_LINE;
  5. the drawn geometry - each kept ref's relation with the most track - to
     LINES_GEOJSON, which step 3 draws and line_colour_search.py reads, so what
     is drawn is exactly what was kept.
A stop that only a NOT_DRAWN relation reaches is listed in excluded_stations.csv
when it lies BEYOND the map's obce, as outside; one inside the city is disclosed
in prose instead (Kyoto's and Madrid's precedent, owner 2026-09-30) - Ostrava's
line 5 is the case.
"""
import json
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping
from shapely.ops import linemerge

from pipeline import osm_tram
from pipeline import stations as station_gates
from pipeline.baseline import emit
from pipeline.countries.czechia_boundary import city_polygon, obec_polygons

ROUTES = ("tram",)


def _track(rel):
    """A relation's track ways - never its `platform` outlines, which linemerge
    would keep as stray rings beside the line (Aarhus)."""
    return [m for m in rel.get("members", []) if m.get("type") == "way"
            and m.get("geometry") and not m.get("role", "").startswith("platform")]


def write_lines(kept, path):
    feats = []
    for ref, rels in kept.items():
        best = max(rels, key=lambda r: (sum(len(m["geometry"]) for m in _track(r)), -r["id"]))
        merged = linemerge(MultiLineString(
            [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in _track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        feats.append({"type": "Feature",
                      "properties": {"line": ref, "relation": best["id"]},
                      "geometry": mapping(MultiLineString([list(g.coords) for g in parts]))})
        print(f"    line {ref:>3}: relation {best['id']} ({len(parts)} piece(s))")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"type": "FeatureCollection", "features": feats},
                               ensure_ascii=False), encoding="utf-8")


def _not_drawn_stops(elements, cfg, kept_names, scope):
    """Stops reached only by a NOT_DRAWN relation and lying BEYOND the map's
    obce, listed as outside (what app/station_scope.py reads them as).

    A not-drawn line's stops INSIDE the city are not listed: they are
    disclosed in prose - the city's page and its section of
    docs/excluded_categories.md - as Kyoto's Sagano line and Madrid's Metro
    Ligero ML2 and ML3 are (owner, 2026-09-30, "follow the precedent").
    Ostrava's line 5 is the case: Poruba,koupaliště and Krásné Pole."""
    from shapely.geometry import Point

    nodes = {e["id"]: e for e in elements if e["type"] == "node"}
    place = ", ".join(f"{o} ({getattr(cfg, 'OBEC_NAMES', {}).get(o, cfg.CITY_NAME)})"
                      for o in cfg.OBEC_CODES)
    rows = []
    for r in (e for e in elements if e["type"] == "relation" and e["id"] in cfg.NOT_DRAWN):
        for m in r.get("members", []):
            n = nodes.get(m["ref"]) if m["type"] == "node" else None
            if not n or not m.get("role", "").startswith("stop"):
                continue
            name = n.get("tags", {}).get("name")
            if (name and name not in kept_names
                    and not scope.contains(Point(n["lon"], n["lat"]))):
                rows.append({"station": name, "lines": r["tags"].get("ref", ""),
                             "reason": (f"outside obec {place}, on a line not drawn: "
                                        f"{cfg.NOT_DRAWN[r['id']]}"),
                             "latitude": n["lat"], "longitude": n["lon"]})
    return pd.DataFrame(rows, columns=["station", "lines", "reason", "latitude",
                                       "longitude"]).drop_duplicates("station")


def step1(cfg):
    cfg.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cfg.OUTPUTS.mkdir(parents=True, exist_ok=True)
    fetch = f"pipeline/{cfg.SLUG}/fetch_sources.py"
    els = osm_tram.read_elements(cfg.OSM_TRAM_JSON, "OSM tram relations", fetch)

    q = osm_tram.stop_rows(els, routes=ROUTES, refs=cfg.LINE_ORDER,
                           operator=cfg.OSM_TRAM_OPERATOR, not_drawn=cfg.NOT_DRAWN,
                           station_add=getattr(cfg, "STATION_ADD", None),
                           name_aliases=getattr(cfg, "STATION_NAME_ALIASES", None))
    platforms, st = osm_tram.collapse(q, refs=cfg.LINE_ORDER, crs_projected=cfg.CRS_PROJECTED,
                                      max_spread_m=cfg.COLLAPSE_MAX_SPREAD_M)

    def count(frame):
        return {ln: int(sum(1 for v in frame["lines"] if ln in v.split("/")))
                for ln in cfg.LINE_ORDER}

    per_line = count(st)
    print(f"\n  {len(platforms)} stop positions -> {len(st)} stations; per line {per_line}")
    print()
    station_gates.verify_stations(
        city=cfg.SLUG, platforms=platforms, stations=st, crs_projected=cfg.CRS_PROJECTED,
        spacing_min=cfg.SPACING_MIN_M,
        expected_per_line=cfg.OPERATOR_STATION_COUNTS or None,
        actual_per_line={cfg.LINE_NAMES[k]: v for k, v in per_line.items()})
    print(f"    gate 3 source: {cfg.OPERATOR_COUNTS_SOURCE or 'none read (see config)'}")

    polys = obec_polygons(cfg)
    names = getattr(cfg, "OBEC_NAMES", {})
    places = gpd.GeoDataFrame({"ref": list(polys), "name": [names.get(o, o) for o in polys]},
                              geometry=list(polys.values()), crs=cfg.CRS_GEOGRAPHIC)
    inside, outside = osm_tram.split_by_places(st, places, keep=cfg.OBEC_CODES)
    inside_per_line = count(inside)
    print(f"\n  {len(st)} stations -> {len(inside)} inside {' + '.join(cfg.OBEC_CODES)}, "
          f"{len(outside)} outside; per line inside {inside_per_line}")
    if len(cfg.OBEC_CODES) > 1:
        print(f"  by obec: {inside['name'].value_counts().to_dict()}")
    if not cfg.EXPECTED_INSIDE_PER_LINE:
        sys.exit("EXPECTED_INSIDE_PER_LINE is empty: record the measured set above in "
                 "config.py (a decision re-taken if it ever changes), then re-run")
    if inside_per_line != cfg.EXPECTED_INSIDE_PER_LINE:
        sys.exit(f"the scope keeps a different set than recorded.\n"
                 f"  measured: {inside_per_line}\n  config  : {cfg.EXPECTED_INSIDE_PER_LINE}")

    nn = inside.to_crs(cfg.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")

    print("\n  drawn geometry (one relation per line, the most track):")
    write_lines(osm_tram.select_relations(els, routes=ROUTES, refs=cfg.LINE_ORDER,
                                          operator=cfg.OSM_TRAM_OPERATOR,
                                          not_drawn=cfg.NOT_DRAWN, verbose=False),
                cfg.LINES_GEOJSON)

    cols = ["station", "lines", "reason", "latitude", "longitude"]
    excluded = pd.concat([
        pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                      "reason": "outside the map's obce, in " + outside["name"],
                      "latitude": outside["latitude"], "longitude": outside["longitude"]},
                     columns=cols),
        _not_drawn_stops(els, cfg, set(st["stop_name"]),
                         places.geometry.union_all()),
    ], ignore_index=True)
    excluded.to_csv(cfg.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(cfg.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {cfg.STATIONS_CSV.relative_to(cfg.ROOT)}; "
          f"{len(excluded)} excluded")
    emit("platforms", len(platforms))
    emit("stations", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(excluded))


def step3(cfg, system_name):
    from pipeline.map_common import load_geojson_line_shapes, render_heatmap

    for path in (cfg.STATIONS_CSV, cfg.BUSINESSES_CLEAN_CSV, cfg.LINES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run fetch_sources.py and the earlier steps first.")
    if set(cfg.LINE_COLOURS) != set(cfg.LINE_ORDER):
        sys.exit("LINE_COLOURS must cover every drawn line: run "
                 f"python scripts/line_colour_search.py {cfg.SLUG} and record its choice")
    ends = getattr(cfg, "LINE_LABEL_ENDS", {})
    specs = {k: (k, cfg.LINE_COLOURS[k], cfg.LINE_NAMES[k], ends.get(k))
             for k in cfg.LINE_ORDER}
    lines = load_geojson_line_shapes(cfg.LINES_GEOJSON, specs, system_name)
    missing = [k for k in cfg.LINE_ORDER if k not in lines]
    if missing:
        sys.exit(f"no geometry for line(s) {missing} - every drawn line needs real "
                 f"geometry, a label and a legend entry")
    stations = pd.read_csv(cfg.STATIONS_CSV)
    businesses = pd.read_csv(cfg.BUSINESSES_CLEAN_CSV)
    print(f"\n  {len(stations):,} stations, {len(businesses):,} storefronts, "
          f"{len(lines)} lines")
    render_heatmap(
        output_path=cfg.HEATMAP_HTML,
        map_title=f"{cfg.CITY_NAME} {system_name} Business Density Heatmap",
        city_name=cfg.CITY_NAME,
        system_name=system_name,
        stations=stations,
        businesses=businesses,
        taxonomy_system=cfg.TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=cfg.CRS_GEOGRAPHIC,
        crs_projected=cfg.CRS_PROJECTED,
        ring_edges_meters=cfg.RING_EDGES_METERS,
        ring_labels=cfg.RING_LABELS,
        label_focus=city_polygon(cfg, verbose=False),
    )
