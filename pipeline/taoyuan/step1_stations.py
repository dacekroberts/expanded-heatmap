"""Taoyuan step 1: the Airport MRT's stations from the national layer, its route
from OpenStreetMap, its station list from the operator.

  * Station points: the national 捷運車站 layer (內政部), the rows named
    桃園機場捷運…站_A<n> - the station, not its entrances. Each carries an
    ADDRESS, and a station is in Taoyuan when that address is (the owner's
    scope: stations inside Taoyuan only).
  * Gate 3: the operator's own station list (Taoyuan Metro's route XML) - the
    same station IDs, one for one.
  * The route: OSM's all-stop (普通車) relation, the longest; every station must
    lie near it.

Reads the cache and NEVER fetches.

    python pipeline/taoyuan/step1_stations.py
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.taoyuan import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
STATION_TO_LINE_MAX_M = 150.0
STATION_NAME = re.compile(r"^桃園機場捷運(?P<zh>.+?)_(?P<id>A\d+a?)$")


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/taoyuan/fetch_sources.py")
    return path


def english(name):
    """The operator's English name without a trailing ' Station', except where
    that word is part of the name (Taipei Main Station, the HSR station)."""
    base = re.sub(r"\s+Station$", "", name.strip())
    return name.strip() if base.endswith(("Main", "HSR")) else base


def operator_list():
    root = ET.parse(need(config.ROUTE_XML, "the operator's station list")).getroot()
    rows = []
    for st in root.iter("Station"):
        rows.append({"id": st.findtext("StationID"), "zh": st.findtext("StationName/Zh_tw"),
                     "en": english(st.findtext("StationName/En") or "")})
    return pd.DataFrame(rows)


def national_points():
    zp = need(config.NATIONAL_STATIONS_ZIP, "the national station layer")
    import zipfile
    shp = [n for n in zipfile.ZipFile(zp).namelist() if n.lower().endswith(".shp")][0]
    g = gpd.read_file(f"zip://{zp}!{shp}", columns=["MARKNAME1", "ADDRESS"])
    m = g.MARKNAME1.str.extract(STATION_NAME)
    g = g[m["id"].notna()].copy()
    g["id"], g["zh_layer"] = m["id"], m["zh"]
    g = g.to_crs(config.CRS_GEOGRAPHIC)
    g["latitude"], g["longitude"] = g.geometry.y, g.geometry.x
    return pd.DataFrame(g.drop(columns="geometry"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    op = operator_list()
    nat = national_points()
    for sid, en in config.OPERATOR_LIST_ADDITIONS.items():
        if sid in set(op.id):
            sys.exit(f"{sid} is now in the operator's list - remove it from OPERATOR_LIST_ADDITIONS")
        zh = nat.zh_layer[nat.id == sid]
        op = pd.concat([op, pd.DataFrame([{"id": sid, "zh": zh.iloc[0] if len(zh) else "", "en": en}])],
                       ignore_index=True)
        print(f"  {sid} {en}: added to the operator's 2018 list (opened after it)")
    print(f"  operator's list: {len(op)} stations; national layer: {len(nat)} station points")
    if nat.id.duplicated().any():
        sys.exit(f"the national layer repeats station IDs: {list(nat.id[nat.id.duplicated()])}")
    st = op.merge(nat, on="id", how="left")
    missing = st[st.latitude.isna()]
    if len(missing):
        sys.exit(f"operator stations with no national point: {list(missing.id)}")
    extra = set(nat.id) - set(op.id)
    if extra:
        sys.exit(f"national points the operator does not list: {sorted(extra)}")

    els = json.loads(need(config.RAIL_OSM_JSON, "OSM relations").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    for r in rels:
        t = r["tags"]
        print(f"    {r['id']}  {t.get('route')}  ref={t.get('ref')}  colour={t.get('colour')}  {t.get('name')}")

    def n_stops(r):
        return sum(1 for m in r["members"] if m["type"] == "node" and m.get("role", "").startswith("stop"))
    allstop = [r for r in rels if config.ALL_STOP_MARK in (r["tags"].get("name") or "")]
    best = max(allstop, key=lambda r: (n_stops(r), sum(len(m.get("geometry") or ()) for m in r["members"])))
    ways = [[(p["lat"], p["lon"]) for p in m["geometry"]] for m in best["members"]
            if m["type"] == "way" and m.get("geometry")]
    stops = [m for m in best["members"] if m["type"] == "node" and m.get("role", "").startswith("stop")]
    colour = (best["tags"].get("colour") or "").upper()
    print(f"  drawn from relation {best['id']} ({len(ways)} ways, {len(stops)} stops, colour {colour})")
    if colour != config.LINE_COLOUR.upper():
        sys.exit(f"OSM's colour {colour} is not config's {config.LINE_COLOUR} - re-read it")

    line_m = unary_union([LineString([TO_M.transform(lo, la) for la, lo in g]) for g in ways])
    st["to_line_m"] = [round(line_m.distance(Point(TO_M.transform(lo, la))), 1)
                       for la, lo in zip(st.latitude, st.longitude)]
    print(f"  national station points to the OSM route: max {st.to_line_m.max():.0f} m, "
          f"median {st.to_line_m.median():.0f} m")
    far = st[st.to_line_m > STATION_TO_LINE_MAX_M]
    if len(far):
        sys.exit(f"stations further than {STATION_TO_LINE_MAX_M:.0f} m from the route: "
                 f"{far[['id', 'en', 'to_line_m']].to_dict('records')}")

    platforms = pd.DataFrame([{"latitude": nodes[m["ref"]]["lat"], "longitude": nodes[m["ref"]]["lon"]}
                              for m in stops if m["ref"] in nodes])
    station_gates.verify_stations(
        city="Taoyuan (whole line)", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED,
        expected_per_line={config.LINE_NAME: len(op)},
        actual_per_line={config.LINE_NAME: len(stops)})

    st["in_city"] = st.ADDRESS.fillna("").str.startswith(config.ADDRESS_PREFIXES)
    st["station"] = st.en
    print(f"  in Taoyuan by the layer's own address: {int(st.in_city.sum())} of {len(st)}")
    emit("stations_on_line", len(st))
    emit("stations_kept", int(st.in_city.sum()))
    emit("osm_stops", len(stops))

    out = st[~st.in_city].copy()
    out["lines"] = config.LINE_NAME
    out["reason"] = "outside Taoyuan (in " + out.ADDRESS.str[:3] + ")"
    out[["station", "lines", "reason", "latitude", "longitude"]].to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} outside Taoyuan -> {config.EXCLUDED_STATIONS_CSV.name}: "
          + "; ".join(f"{r.id} {r.station} ({r.ADDRESS[:3]})" for r in out.itertuples()))
    emit("stations_outside", len(out))

    kept = st[st.in_city].copy()
    kept["lines"] = config.LINE_KEY
    kept = kept.rename(columns={"zh": "name_zh"})
    kept[["station", "name_zh", "id", "latitude", "longitude", "lines"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(kept)} stations")

    element = {"type": "relation", "id": 1,
               "tags": {"ref": config.LINE_KEY, "name": config.LINE_NAME, "colour": config.LINE_COLOUR},
               "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                           for g in ways]}
    config.RAIL_LINES_JSON.write_text(json.dumps({"elements": [element]}), encoding="utf-8")
    emit("lines_drawn", 1)


if __name__ == "__main__":
    main()
