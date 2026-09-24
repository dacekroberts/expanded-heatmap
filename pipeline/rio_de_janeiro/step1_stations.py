"""Rio de Janeiro step 1: MetrôRio from the city's own layers, the VLT Carioca
from OpenStreetMap, collapsed together by name.

    python pipeline/rio_de_janeiro/step1_stations.py

Reads the cache only; fetch_sources.py downloads.

  * **Metro** - IPP's stations layer 19 (CC BY 4.0), a line's stations by its
    integer flag `flg_linha1/2/4`; line geometry from layer 18, keyed on
    `codlinmetr`. ⚠ Layer 18's `flg_ativa` is NULL on two of the three lines,
    so nothing filters on it; every station's own `flg_ativa` is 1, and step 1
    stops if one is not.
  * **VLT** - OSM route relations through pipeline/countries/brazil_rail.py's
    stop reader. The agency's own VLT layer is NOT used: its per-line flags
    give 20/14/11/14 stops where pt.wikipedia lists 16/11/10/11 and OSM agrees
    with Wikipedia (measured 2026-09-24). Its `linha_4` column is also coded
    `Sim`/`Nao` where the other three use 1/2 - the brief's trap.
  * One lines GeoJSON for step 3: the metro's agency geometry and the VLT's
    OSM ways, each feature keyed on `line`.
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import brazil_rail  # noqa: E402
from pipeline.countries.brazil_boundary import in_codes, municipios  # noqa: E402
from pipeline.rio_de_janeiro import config  # noqa: E402
from pipeline.rio_de_janeiro.boundary import city_polygon  # noqa: E402


def _features(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/rio_de_janeiro/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))["features"]


def metro_rows():
    rows = []
    for f in _features(config.METRO_STATIONS_JSON):
        p = f["properties"]
        if str(p.get("flg_ativa")) != "1":
            sys.exit(f"metro station {p.get('nome')} has flg_ativa={p.get('flg_ativa')!r} - "
                     "a closed or planned station reached the operating layer")
        lon, lat = f["geometry"]["coordinates"][:2]
        for ln, flag in config.METRO_FLAGS.items():
            if str(p.get(flag)) == "1":
                rows.append({"line": ln, "node": f"metro-{p['objectid']}",
                             "stop_name": config.STATION_NAME_ALIASES.get(p["nome"], p["nome"]),
                             "latitude": lat, "longitude": lon})
    return pd.DataFrame(rows)


def vlt_rows():
    # brazil_rail's reader, pointed at the VLT's four lines: every other OSM
    # relation (the metro, SuperVia, the Corcovado, the Bonde) is in LEFT_OUT.
    cfg = SimpleNamespace(OSM_RAIL_JSON=config.OSM_RAIL_JSON, LINE_RELATIONS=config.LINE_RELATIONS,
                          LEFT_OUT=config.LEFT_OUT, STATION_NAME_ALIASES=config.STATION_NAME_ALIASES,
                          NODE_NAMES=config.NODE_NAMES)
    q = brazil_rail.stop_rows(cfg)
    q["stop_name"] = [config.LINE_STATION_RENAMES.get((ln, nm), nm)
                      for ln, nm in zip(q["line"], q["stop_name"])]
    return q


def write_lines():
    feats = []
    for f in _features(config.METRO_LINES_JSON):
        key = str(f["properties"]["codlinmetr"])
        if key in config.METRO_FLAGS:
            feats.append({"type": "Feature", "properties": {"line": key}, "geometry": f["geometry"]})
    rels = {e["id"]: e for e in json.loads(config.OSM_RAIL_JSON.read_text(encoding="utf-8"))["elements"]
            if e["type"] == "relation"}
    for ln, ids in config.LINE_RELATIONS.items():
        # The direction relation with the most way geometry, as load_osm_line_shapes chooses.
        best = max((rels[i] for i in ids),
                   key=lambda r: sum(len(m.get("geometry") or []) for m in r["members"] if m["type"] == "way"))
        parts = [[[pt["lon"], pt["lat"]] for pt in m["geometry"]]
                 for m in best["members"] if m["type"] == "way" and m.get("geometry")]
        feats.append({"type": "Feature", "properties": {"line": ln},
                      "geometry": {"type": "MultiLineString", "coordinates": parts}})
    missing = set(config.LINE_ORDER) - {f["properties"]["line"] for f in feats}
    if missing:
        sys.exit(f"no geometry for {sorted(missing)}")
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  line geometry -> {config.LINES_GEOJSON.name} ({len(feats)} lines)")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    q = pd.concat([metro_rows(), vlt_rows()], ignore_index=True)
    order = list(config.LINE_ORDER)
    lines_by_name = q.groupby("stop_name")["line"].agg(
        lambda s: " ".join(ln for ln in order if ln in set(s)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"],
                                                                platforms["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop points -> {len(by_name)} stations by name; widest:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {nm:<40} {spread[nm]:>5.0f} m  [{lines_by_name[nm]}]")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M} m: {too_far.round().to_dict()}")
    st = by_name.reset_index()
    st["lines"] = st["stop_name"].map(lines_by_name)

    def count(ln):
        return int(sum(1 for v in st["lines"] if ln in v.split()))
    metro = set(config.METRO_FLAGS)
    vlt = set(config.VLT_LINES)
    actual = {config.LINE_NAMES[ln]: count(ln) for ln in order}
    actual["Metrô (network)"] = int(sum(1 for v in st["lines"] if metro & set(v.split())))
    actual["VLT (network)"] = int(sum(1 for v in st["lines"] if vlt & set(v.split())))
    expected = {config.LINE_NAMES[ln]: n for ln, n in config.METRO_GATE3["lines"].items()}
    expected.update({config.LINE_NAMES[ln]: n for ln, n in config.GATE3["lines"].items()})
    expected["Metrô (network)"] = config.METRO_GATE3["network"]
    expected["VLT (network)"] = config.GATE3["network"]
    print()
    station_gates.verify_stations(
        city=config.NAME, platforms=platforms, stations=st, crs_projected=config.CRS_PROJECTED,
        spacing_min=config.SPACING_MIN_M, expected_per_line=expected, actual_per_line=actual)
    print(f"    gate 3 source: {config.METRO_GATE3['source']}; {config.GATE3['source']}")

    poly = city_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(st["longitude"], st["latitude"]), crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    nb = municipios(config.OSM_MUNICIPIOS_JSON, config.CRS_GEOGRAPHIC)
    excluded = []
    for _, r in st[~inside].iterrows():
        pt = gpd.points_from_xy([r["longitude"]], [r["latitude"]])[0]
        hit = nb[nb.contains(pt) & ~nb["ibge"].map(lambda c: in_codes(c, config.SCOPE_CODES))]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} is outside the scope and in {len(hit)} recorded municípios")
        excluded.append({"station": r["stop_name"], "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['name']} ({hit.iloc[0]['ibge']}), outside "
                                   f"município {config.IBGE_MUNICIPIO}",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  scope: {len(st)} stations -> {int(inside.sum())} inside, {len(excluded)} excluded")
    keep = (st[inside].rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.name}")
    write_lines()
    emit("stop_points", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(excluded))


if __name__ == "__main__":
    main()
