"""Taichung step 1: the Green Line's stations from the operator, its route from OSM.

Stations are Taichung Metro's own table (station code, Chinese and English
names, coordinates). The line's route is the OpenStreetMap relation of the
same line - checked against the operator's stations: every station must lie
within STATION_TO_LINE_MAX_M of the drawn route, and the relation's stop count
must equal the operator's (gate 3).

Every station is kept (one line, uniformly spaced, all inside the city).

Reads the cache and NEVER fetches.

    python pipeline/taichung/step1_stations.py
"""
import csv
import io
import json
import sys
from pathlib import Path

import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.taichung import config  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
STATION_TO_LINE_MAX_M = 150.0


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/taichung/fetch_sources.py")
    return path


def operator_stations():
    # The portal prefixes its CSVs with SEVERAL byte-order marks (cjk-text: a BOM
    # hides in the first header); utf-8-sig strips only one.
    text = need(config.STATIONS_RAW_CSV, "Green Line stations").read_bytes().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text.lstrip(chr(0xFEFF)))))
    st = pd.DataFrame({"station": [r["車站英文"].strip() for r in rows],
                       "name_zh": [r["車站中文"].strip() for r in rows],
                       "code": [r["車站編號"].strip() for r in rows],
                       "latitude": [float(r["緯度"]) for r in rows],
                       "longitude": [float(r["經度"]) for r in rows],
                       "address": [r["地址"].strip() for r in rows]})
    dup = st.code[st.code.duplicated(keep=False)]
    if len(dup):
        # Recorded, not fixed: the table gives 烏日 and 高鐵臺中站 both G17
        # (2026-09-25). Stations are keyed by name, so it changes nothing.
        print(f"  NOTE: the operator's table repeats station code(s) {sorted(set(dup))}: "
              f"{list(st.name_zh[st.code.isin(dup)])} - keyed by name instead")
    if st.station.duplicated().any():
        sys.exit(f"duplicate station names: {list(st.station[st.station.duplicated()])}")
    return st


def green_line():
    els = json.loads(need(config.RAIL_OSM_JSON, "OSM rail relations").read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    print("  rail route relations in the city's box:")
    for r in rels:
        t = r.get("tags", {})
        print(f"    {r['id']}  {t.get('route')}  ref={t.get('ref')}  network={t.get('network')}  "
              f"colour={t.get('colour')}  {t.get('name')}")
    mine = [r for r in rels if r.get("tags", {}).get("route") in ("subway", "light_rail")
            and config.LINE_MATCH in (r["tags"].get("name") or "")]
    if not mine:
        sys.exit(f"no subway/light_rail relation named with {config.LINE_MATCH!r}")
    return mine, nodes


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    st = operator_stations()
    print(f"  {len(st)} stations in the operator's table")

    rels, nodes = green_line()
    best = max(rels, key=lambda r: sum(len(m.get("geometry") or ()) for m in r["members"]
                                       if m["type"] == "way"))
    ways = [[(p["lat"], p["lon"]) for p in m["geometry"]] for m in best["members"]
            if m["type"] == "way" and m.get("geometry")]
    colours = {(r["tags"].get("colour") or "").upper() for r in rels} - {""}
    print(f"  drawn from relation {best['id']} ({len(ways)} ways); colours on the relations: {colours}")
    stops = [m for m in best["members"] if m["type"] == "node" and m.get("role", "").startswith("stop")]

    line_m = unary_union([LineString([TO_M.transform(lo, la) for la, lo in g]) for g in ways])
    d = [line_m.distance(Point(TO_M.transform(lo, la))) for la, lo in zip(st.latitude, st.longitude)]
    st["to_line_m"] = [round(x, 1) for x in d]
    far = st[st.to_line_m > STATION_TO_LINE_MAX_M]
    print(f"  operator stations to the OSM route: max {max(d):.0f} m, median {sorted(d)[len(d) // 2]:.0f} m")
    if len(far):
        sys.exit(f"stations further than {STATION_TO_LINE_MAX_M:.0f} m from the drawn route: "
                 f"{far[['station', 'to_line_m']].to_dict('records')}")

    platforms = pd.DataFrame([{"latitude": nodes[m["ref"]]["lat"], "longitude": nodes[m["ref"]]["lon"]}
                              for m in stops if m["ref"] in nodes])
    station_gates.verify_stations(
        city="Taichung", platforms=platforms if len(platforms) else st, stations=st,
        crs_projected=config.CRS_PROJECTED,
        expected_per_line={config.LINE_NAME: len(st)},
        actual_per_line={config.LINE_NAME: len(stops)})

    outside = st[~st.address.str.startswith(config.ADDRESS_PREFIXES)]
    if len(outside):
        sys.exit(f"stations whose address is not in Taichung: {list(outside.station)}")
    print(f"  every station's address is in Taichung ({len(st)} of {len(st)})")
    emit("stations_kept", len(st))
    emit("osm_stops", len(stops))

    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    st["lines"] = config.LINE_KEY
    st[["station", "name_zh", "latitude", "longitude", "lines"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(st)} stations; none excluded")

    element = {"type": "relation", "id": 1,
               "tags": {"ref": config.LINE_KEY, "name": config.LINE_NAME, "colour": config.LINE_COLOUR},
               "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                           for g in ways]}
    config.RAIL_LINES_JSON.write_text(json.dumps({"elements": [element]}), encoding="utf-8")
    emit("lines_drawn", 1)


if __name__ == "__main__":
    main()
