"""Step 1 - Metro de Madrid stations and line geometry, from CRTM.

NO GTFS. Madrid is the first city in this project whose rail comes from the
operator's ArcGIS feature services, and that is a licence consequence rather
than a preference - see config.CRTM_METRO_SERVICE and
docs/build_briefs/madrid.md.

What this step has to get right, each of which has bitten this project before:

  - **293 records are not 293 stations.** CODIGOESTACION is unique per
    station-PER-LINE, so an interchange appears once for each line serving it.
    243 distinct names network-wide; 193 of them inside Madrid.
  - **18 line codes are not 18 lines.** Lettered branches (7a/7b, 9A/9B,
    10a/10b) and circular lines split into two codes (6-1/6-2, 12-1/12-2)
    collapse to 13 - the Guadalajara lesson, where filtering on a label lost a
    whole line.
  - **The boundary's declared CRS is not evidence.** Surrey's said EPSG:4326
    and held UTM metres, so every containment test returned zero. Coordinate
    MAGNITUDES are checked here, not the declaration.
  - **A spatial filter and an authoritative field should agree**, and where
    they do not that is a finding rather than a tie to break silently.
"""

import json
import sys
import urllib.request
import zipfile

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent))

from pipeline.madrid.config import (  # noqa: E402
    CITY_BOUNDARY_URL,
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    CRTM_METRO_SERVICE,
    CRTM_STATIONS_LAYER,
    CRTM_TRAMOS_LAYER,
    DATA_PROCESSED,
    DATA_RAW,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    LINE_OF_CODE,
    LINE_SHAPES_GEOJSON,
    MADRID_MUNICIPIO_CODE,
    RING_EDGES_METERS,
    STATIONS_CSV,
    STATIONS_RAW_JSON,
    TRAMOS_RAW_JSON,
)

UA = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def fetch_layer(layer, cache):
    """One ArcGIS layer, cached to the gitignored raw directory.

    `resultRecordCount` is set above the known row count AND the response's
    `exceededTransferLimit` is checked: a server-side page cap that silently
    truncates is the same shape of failure as a stale mirror.
    """
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    url = (f"{CRTM_METRO_SERVICE}/{layer}/query?where=1%3D1&outFields=*"
           f"&returnGeometry=true&outSR=25830&f=json&resultRecordCount=5000")
    print(f"  fetching layer {layer} ...")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        payload = json.loads(r.read())
    if payload.get("exceededTransferLimit"):
        raise SystemExit(f"layer {layer}: the server paged the response - "
                         "raise resultRecordCount or page it, do not trust this")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload), encoding="utf-8")
    return payload


def load_boundary():
    """Madrid's término municipal, with the declared CRS treated as a claim."""
    if not CITY_BOUNDARY_ZIP.exists():
        print("  downloading the término municipal ...")
        CITY_BOUNDARY_ZIP.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(
                urllib.request.Request(CITY_BOUNDARY_URL, headers=UA), timeout=300) as r:
            CITY_BOUNDARY_ZIP.write_bytes(r.read())
    with zipfile.ZipFile(CITY_BOUNDARY_ZIP) as z:
        shp = [n for n in z.namelist() if n.lower().endswith(".shp")]
        if not shp:
            raise SystemExit(f"no .shp in {CITY_BOUNDARY_ZIP.name}: {z.namelist()[:6]}")
    b = gpd.read_file(f"zip://{CITY_BOUNDARY_ZIP}!{shp[0]}")
    if b.empty or b.geometry.isna().all():
        raise SystemExit("boundary layer has no geometry - the empty-view trap")

    # THE DECLARED CRS IS NOT EVIDENCE. Surrey's said 4326 and held UTM metres.
    xs = b.geometry.union_all().bounds
    looks_like_metres = abs(xs[0]) > 1000
    print(f"  boundary: {len(b)} feature(s), declared {b.crs}, "
          f"bounds x {xs[0]:,.0f}..{xs[2]:,.0f}")
    if looks_like_metres and (b.crs is None or b.crs.to_epsg() == 4326):
        raise SystemExit("boundary declares degrees and contains metres - "
                         "the Surrey trap; set the CRS explicitly before using it")
    if b.crs is None:
        raise SystemExit("boundary has no CRS at all")
    b = b.to_crs(CRS_PROJECTED)
    area = b.union_all().area / 1e6
    # Madrid's término municipal is ~604 km2. A layer that is really a district,
    # a bounding box or another Madrid entirely fails here rather than silently
    # keeping the wrong stations - the Guadalajara-in-Spain error's shape.
    if not 500 <= area <= 700:
        raise SystemExit(f"boundary area {area:,.1f} km2 is not Madrid's ~604 km2")
    print(f"  boundary area {area:,.1f} km2 - consistent with Madrid")
    return b


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Stations - CRTM M4_Estaciones")
    payload = fetch_layer(CRTM_STATIONS_LAYER, STATIONS_RAW_JSON)
    rows = []
    for f in payload["features"]:
        a, g = f["attributes"], f.get("geometry") or {}
        if g.get("x") is None:
            continue
        rows.append({
            "name": (a.get("DENOMINACION") or "").strip(),
            "codigo": a.get("CODIGOESTACION"),
            "municipio_code": a.get("CODIGOMUNICIPIO"),
            "x": g["x"], "y": g["y"],
        })
    st = pd.DataFrame(rows)
    print(f"  {len(st)} station-per-line records fetched")

    # THE UNNAMED RECORDS, handled explicitly rather than dropped by a filter
    # that does not mention them. Two rows (CODIGOESTACION 347, 348, both added
    # 2025-05-20) carry no DENOMINACION at all. A station with no name cannot
    # satisfy this project's every-station-labelled rule, and an unnamed
    # placeholder is not yet a station a rider can use.
    unnamed = st[st["name"] == ""]
    if len(unnamed):
        print(f"  DROPPED {len(unnamed)} record(s) with no DENOMINACION: "
              f"codigo {sorted(unnamed['codigo'])} - unnamed placeholders")
        st = st[st["name"] != ""].copy()

    # 293 records -> physical stations. An interchange is one place; averaging
    # its per-line points puts the marker between the platforms rather than on
    # an arbitrary one.
    print(f"  {st['name'].nunique()} distinct station names "
          f"(from {len(st)} records - interchanges repeat per line)")
    grouped = (st.groupby("name")
                 .agg(x=("x", "mean"), y=("y", "mean"),
                      municipios=("municipio_code", lambda s: sorted(set(s))),
                      records=("codigo", "size"))
                 .reset_index())

    gdf = gpd.GeoDataFrame(
        grouped, geometry=[Point(xy) for xy in zip(grouped.x, grouped.y)],
        crs=CRS_PROJECTED)

    print("\nBoundary - término municipal de Madrid")
    boundary = load_boundary()
    poly = boundary.union_all()

    gdf["in_city_spatial"] = gdf.geometry.within(poly)
    gdf["in_city_field"] = gdf["municipios"].map(
        lambda ms: MADRID_MUNICIPIO_CODE in ms)

    # THE TWO METHODS ARE COMPARED, NOT SILENTLY RECONCILED. Los Angeles is the
    # precedent for preferring an authoritative field, and add-city's invariant
    # is that the boundary polygon is the filter of record; where they disagree
    # that is worth printing rather than resolving by whichever ran last.
    disagree = gdf[gdf["in_city_spatial"] != gdf["in_city_field"]]
    print(f"\n  in city by boundary polygon : {int(gdf['in_city_spatial'].sum())}")
    print(f"  in city by CODIGOMUNICIPIO  : {int(gdf['in_city_field'].sum())}")
    if len(disagree):
        print(f"  ** {len(disagree)} DISAGREE - listed, not silently resolved:")
        for _, r in disagree.iterrows():
            print(f"       {r['name']:34} polygon={r['in_city_spatial']} "
                  f"field={r['municipios']}")
    else:
        print("  the two methods agree on every station")

    kept = gdf[gdf["in_city_spatial"]].copy()
    outside = gdf[~gdf["in_city_spatial"]].copy()

    # Excluded stations are a scoping RECORD, not a silent filter: San Diego
    # dropped 16 and Los Angeles 54, each named with the city it lies in.
    if len(outside):
        EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
        (outside.drop(columns="geometry")
                .assign(municipio_codes=lambda d: d["municipios"].map(
                    lambda ms: " ".join(m or "?" for m in ms)))
                .drop(columns="municipios")
                .rename(columns={"name": "station"})
                .sort_values("station")
                .to_csv(EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8"))
        print(f"\n  {len(outside)} stations lie outside Madrid - written to "
              f"{EXCLUDED_STATIONS_CSV.name}")
        print("    (each needs its own municipality's business register to be "
              "mapped - a new project, not a config change)")

    # --- lines ------------------------------------------------------------
    print("\nLine geometry - CRTM M4_Tramos")
    tramos = fetch_layer(CRTM_TRAMOS_LAYER, TRAMOS_RAW_JSON)
    segs = {}
    codes = set()
    for f in tramos["features"]:
        a, g = f["attributes"], f.get("geometry") or {}
        code = (a.get("NUMEROLINEAUSUARIO") or "").strip().upper()
        codes.add(code)
        line = LINE_OF_CODE.get(code)
        if line is None:
            raise SystemExit(f"unmapped line code {code!r} - add it to "
                             "config.LINE_OF_CODE rather than letting it vanish")
        for path in g.get("paths", []):
            if len(path) >= 2:
                segs.setdefault(line, []).append(LineString(path))
    print(f"  {len(codes)} distinct line codes -> {len(segs)} lines "
          f"(codes: {' '.join(sorted(codes))})")
    if len(segs) != 13:
        raise SystemExit(f"expected 13 Metro lines, collapsed to {len(segs)} - "
                         "the GTFS and OSM screens both say 13")

    lines = gpd.GeoDataFrame(
        [{"line": k, "name": LINE_NAMES[k], "segments": len(v)} for k, v in segs.items()],
        geometry=[__import__("shapely").ops.unary_union(v) for v in segs.values()],
        crs=CRS_PROJECTED).sort_values("line")
    LINE_SHAPES_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    lines.to_crs(CRS_GEOGRAPHIC).to_file(LINE_SHAPES_GEOJSON, driver="GeoJSON")
    print(f"  wrote {LINE_SHAPES_GEOJSON.name}")
    for _, r in lines.iterrows():
        print(f"    {r['name']:28} {r['segments']:>3} tramos")

    # --- station spacing against the outer ring ---------------------------
    #
    # add-city Step 4 asks for this explicitly: where stations sit closer than
    # the 0.6 mi outer edge their rings overlap. Nothing is double-counted (a
    # business is assigned to its nearest station) but the overlap should be a
    # conscious choice rather than a discovery.
    pts = kept.geometry
    outer = RING_EDGES_METERS[-1]
    near = 0
    for i, p in enumerate(pts):
        d = pts.drop(pts.index[i]).distance(p).min()
        if d < outer:
            near += 1
    print(f"\n  {near} of {len(kept)} kept stations sit within {outer:,.0f} m "
          f"({RING_EDGES_METERS[-1]/1609.344:.1f} mi) of another - their outer "
          "rings overlap")

    out = kept.to_crs(CRS_GEOGRAPHIC)
    st_out = pd.DataFrame({
        "station": out["name"],
        "latitude": out.geometry.y,
        "longitude": out.geometry.x,
    }).sort_values("station")
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    st_out.to_csv(STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
