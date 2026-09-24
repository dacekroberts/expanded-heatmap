"""São Paulo step 1: Metrô Lines 1-5 and 15 stations inside the município.

    python pipeline/sao_paulo/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

  * **Geometry and stations from OpenStreetMap** by route-relation membership
    (the owner's 2026-09-23 decision, osm-rail); **GeoSampa's OPERATING layer
    decides status** and supplies gate 3's count. Lines 6 and 17 are in OSM
    and only in GeoSampa's planned layer: step 1 STOPS if either appears in
    the operating layer, so an opening is added deliberately.
  * Stations collapse by NAME across directions, every spread printed.
  * Every station must lie inside the município - the brief measured all six
    operating lines inside it - and step 1 stops if one does not.
"""
import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.sao_paulo import config  # noqa: E402
from pipeline.sao_paulo.boundary import city_polygon, neighbour_polygons  # noqa: E402

GEOSAMPA_LINE = {"AZUL": "1", "VERDE": "2", "VERMELHA": "3", "AMARELA": "4", "LILAS": "5",
                 "PRATA": "15"}


def _read(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/sao_paulo/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    return " ".join(s.replace("-", " ").split())


def geosampa_status():
    feats = _read(config.GEOSAMPA_STATIONS_JSON)["features"]
    lines = {f["properties"]["nm_linha_metro_trem"] for f in feats}
    unknown = lines - set(GEOSAMPA_LINE)
    if unknown:
        sys.exit(f"GeoSampa's OPERATING layer lists line(s) {sorted(unknown)} - if Linha 6 or "
                 f"17 has opened, add it deliberately (config.NOT_YET_OPEN_REFS)")
    per_line = {}
    for f in feats:
        per_line.setdefault(GEOSAMPA_LINE[f["properties"]["nm_linha_metro_trem"]], set()).add(
            fold(f["properties"]["nm_estacao_metro_trem"]))
    names = {fold(f["properties"]["nm_estacao_metro_trem"]) for f in feats}
    for ln, added in config.GATE3_ADDED.items():
        for nm in added:
            if nm in per_line.get(ln, set()):
                sys.exit(f"GeoSampa now lists {nm} on line {ln} - drop the GATE3_ADDED correction")
            per_line.setdefault(ln, set()).add(nm)
            names.add(nm)
            print(f"  gate 3: {nm} added to line {ln} (config.GATE3_ADDED - GeoSampa is stale)")
    return per_line, names


def geosampa_line9():
    """Line 9's operating stations from GeoSampa's CPTM layer - count only."""
    feats = _read(config.GEOSAMPA_TRAIN_STATIONS_JSON)["features"]
    return {fold(f["properties"]["nm_estacao_metro_trem"]) for f in feats
            if f["properties"]["nm_linha_metro_trem"] == "ESMERALDA"
            and f["properties"]["tx_situacao_metro_trem"] == "OPERANDO"}


def stop_rows():
    els = (_read(config.OSM_RAIL_JSON)["elements"]
           + _read(config.OSM_TRAIN_JSON)["elements"])
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rows = []
    print("  route relations:")
    for r in sorted((e for e in els if e["type"] == "relation"),
                    key=lambda e: (e["tags"].get("route", ""), e["tags"].get("ref", "").zfill(3))):
        t = r["tags"]
        keep = t.get("ref") in config.DRAW_REFS.get(t.get("route"), ())
        known_out = (t.get("ref") in config.NOT_YET_OPEN_REFS
                     or (t.get("route") == "train" and t.get("ref") in config.CPTM_NOT_DRAWN))
        print(f"    {'KEEP' if keep else 'out ':4} {r['id']:>9} {t.get('route', ''):9} "
              f"{t.get('ref', ''):>3}  {t.get('name', '')[:60]}")
        if not keep and not known_out:
            sys.exit(f"relation {r['id']} ({t.get('name')}) is neither drawn nor recorded as "
                     f"not yet open - a scope question")
        if not keep:
            continue
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"{r['id']}: stop member {m['ref']} is not a named stop_position")
            rows.append({"line": t["ref"], "node": n["id"],
                         "stop_name": config.STATION_NAME_ALIASES.get(nt["name"], nt["name"]),
                         "latitude": n["lat"], "longitude": n["lon"]})
    return pd.DataFrame(rows).drop_duplicates(["line", "node"])


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    gs_per_line, gs_names = geosampa_status()
    q = stop_rows()
    order = list(config.LINE_ORDER)
    lines_by_name = q.groupby("stop_name")["line"].agg(
        lambda s: " ".join(ln for ln in order if ln in set(s)))
    platforms = q.drop_duplicates("node")
    by_name = platforms.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean"),
                                                 positions=("node", "nunique"))
    g = gpd.GeoDataFrame(platforms, geometry=gpd.points_from_xy(platforms["longitude"],
                                                                platforms["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(platforms)} stop positions -> {len(by_name)} stations by name; widest:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {nm:<40} {spread[nm]:>5.0f} m  [{lines_by_name[nm]}]")
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M} m: {too_far.round().to_dict()}")
    st_rows = by_name.reset_index()
    st_rows["lines"] = st_rows["stop_name"].map(lines_by_name)

    gs_per_line["9"] = geosampa_line9()
    metro = set(order) - {"9"}
    actual = {config.LINE_NAMES[ln]: int(sum(1 for v in st_rows["lines"] if ln in v.split()))
              for ln in order}
    actual["Metrô (network)"] = int(sum(1 for v in st_rows["lines"] if metro & set(v.split())))
    expected = {config.LINE_NAMES[ln]: len(gs_per_line.get(ln, ())) for ln in order}
    expected["Metrô (network)"] = len(gs_names)
    print()
    station_gates.verify_stations(
        city="São Paulo", platforms=platforms, stations=st_rows,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=expected, actual_per_line=actual)
    print("    gate 3 source: GeoSampa's operating layers geoportal:estacao_metro and, for "
          "Line 9, geoportal:estacao_trem (the agency's own, used for counts and status only)")
    # Name-level difference, so a count mismatch says WHICH station.
    for ln in order:
        osm_names = {fold(n) for n, v in lines_by_name.items() if ln in v.split()}
        only_gs, only_osm = gs_per_line.get(ln, set()) - osm_names, osm_names - gs_per_line.get(ln, set())
        if only_gs or only_osm:
            print(f"    {config.LINE_NAMES[ln]}: only in GeoSampa {sorted(only_gs)}; "
                  f"only in OSM {sorted(only_osm)}")

    poly = city_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(st_rows["longitude"], st_rows["latitude"]),
                        crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    outside = st_rows[~inside]
    # The six metro lines lie wholly inside the município (the brief); only a
    # CPTM line may leave it - Line 9 runs on to Osasco.
    bad = [nm for nm, ln in zip(outside["stop_name"], outside["lines"]) if ln != "9"]
    if bad:
        sys.exit(f"metro stations outside the município - the brief said none: {sorted(bad)}")
    nb = neighbour_polygons()
    excluded = []
    for _, r in outside.iterrows():
        pt = gpd.points_from_xy([r["longitude"]], [r["latitude"]])[0]
        hit = nb[nb.contains(pt) & (nb["ibge"] != config.IBGE_MUNICIPIO)]
        if len(hit) != 1:
            sys.exit(f"{r['stop_name']} is outside São Paulo and in {len(hit)} recorded municípios")
        excluded.append({"station": r["stop_name"], "lines": r["lines"],
                         "reason": f"in {hit.iloc[0]['name']} ({hit.iloc[0]['ibge']}), "
                                   f"outside município {config.IBGE_MUNICIPIO}",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    for x in excluded:
        print(f"  excluded: {x['station']} [{x['lines']}] - {x['reason']}")
    st_rows = st_rows[inside]
    keep = (st_rows.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  all {len(keep)} stations inside município {config.IBGE_MUNICIPIO} -> "
          f"{config.STATIONS_CSV.relative_to(config.ROOT)}")
    emit("stop_positions", len(platforms))
    emit("stations", len(keep))


if __name__ == "__main__":
    main()
