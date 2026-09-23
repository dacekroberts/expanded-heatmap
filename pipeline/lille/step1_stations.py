"""Lille (Regional) step 1: ilévia's métro and tram stations, and the communes
they serve.

    python pipeline/lille/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

THE FIRST FRENCH CITY BUILT WITHOUT A FEED. Stations come from MEL's own WFS
layers rather than from GTFS stops, which changes three things every earlier
French step 1 took for granted:

  * **There is no route membership to read.** The métro layer names its line
    (`ligne` 1 or 2); the TRAM layer names none, so each tram stop is placed on
    R and/or T by snapping it to MEL's own line geometry. A stop too far from
    both exits rather than being guessed.
  * **The scope is derived, not given.** Every station is placed in the
    official commune contours; the communes that hold one ARE the scope, and
    the result is asserted against config so a change is a decision.
  * **Gate 3 is against OpenStreetMap**, the one count here that does not come
    from the source being checked. MEL publishes the stations; comparing MEL
    with MEL would pass by construction.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import MultiLineString, Point, mapping, shape
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates
from pipeline.lille import config
from pipeline.osm_cache import load as osm_load

# A tram stop further than this from both R's and T's geometry is not placed on
# either. Measured max once the build ran is printed below; the cap is a guard
# against a stop that belongs to neither, not a tuning knob.
SNAP_MAX_M = 75.0
# Rows sharing a name further apart than this are two places, not one station.
SAME_NAME_MAX_SPREAD_M = 400.0


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\n"
                 f"Run: python pipeline/lille/fetch_sources.py")
    return path


def features(path):
    return json.loads(path.read_text(encoding="utf-8"))["features"]


def to_l93(geom):
    return gpd.GeoSeries([geom], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).iloc[0]


def tram_line_geometry():
    """R and T assembled from MEL's SECTIONS.

    `tramway_lignes` holds four features: R's branch, T's branch, and the shared
    Lille - Croisé Laroche trunk TWICE, once per line. Which copy belongs to
    which line is read from the data - each branch's `tramway` id - rather than
    hard-coded, so a renumbering fails here instead of swapping two lines.
    """
    sections = features(config.TRAM_LINES_GEOJSON)
    branch_id = {}
    for f in sections:
        pr = f["properties"]
        if pr["ligne"] in ("R", "T"):
            branch_id[pr["tramway"]] = pr["ligne"]
    if sorted(branch_id.values()) != ["R", "T"]:
        sys.exit(f"expected one R and one T branch section, got {branch_id}")

    parts = {"R": [], "T": []}
    for f in sections:
        pr, g = f["properties"], f["geometry"]
        coords = ([g["coordinates"]] if g["type"] == "LineString"
                  else g["coordinates"])
        if pr["ligne"] in ("R", "T"):
            parts[pr["ligne"]].extend(coords)
        elif pr["ligne"] == "R,T":
            owner = branch_id.get(pr["tramway"])
            if owner is None:
                sys.exit(f"trunk section with tramway={pr['tramway']!r} "
                         f"matches no branch {branch_id}")
            parts[owner].extend(coords)
        else:
            sys.exit(f"unexpected tram section ligne={pr['ligne']!r}")
    return parts


def main():
    for path, what in ((config.METRO_STATIONS_GEOJSON, "MEL métro stations"),
                       (config.TRAM_STOPS_GEOJSON, "MEL tram stops"),
                       (config.TRAM_LINES_GEOJSON, "MEL tram lines"),
                       (config.MEL_COMMUNES_GEOJSON, "MEL commune contours"),
                       (config.OSM_ROUTES_JSON, "the OSM route relations")):
        need(path, what)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    # --- tram geometry, per line -------------------------------------------
    parts = tram_line_geometry()
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"line": k},
         "geometry": mapping(MultiLineString(v))} for k, v in parts.items()]}
    config.TRAM_LINES_BY_LINE_GEOJSON.write_text(
        json.dumps(fc, ensure_ascii=False), encoding="utf-8")
    tram_l93 = {k: to_l93(MultiLineString(v)) for k, v in parts.items()}
    print("tram lines assembled from MEL sections: "
          + ", ".join(f"{k} {len(v)} part(s)" for k, v in parts.items()))

    # --- station-line rows ---------------------------------------------------
    rows = []
    for f in features(config.METRO_STATIONS_GEOJSON):
        pr = f["properties"]
        x, y = f["geometry"]["coordinates"][:2]
        rows.append({"name": pr["nom_statio"].strip(), "line": f"M{pr['ligne']}",
                     "longitude": x, "latitude": y})

    worst = 0.0
    for f in features(config.TRAM_STOPS_GEOJSON):
        pr = f["properties"]
        x, y = f["geometry"]["coordinates"][:2]
        pt = to_l93(Point(x, y))
        dist = {k: pt.distance(g) for k, g in tram_l93.items()}
        on = [k for k, d in dist.items() if d <= SNAP_MAX_M]
        if not on:
            sys.exit(f"tram stop {pr['nom_statio']!r} is "
                     f"{min(dist.values()):.0f} m from both R and T - more "
                     f"than {SNAP_MAX_M:.0f} m, so it is not placed on either")
        worst = max(worst, min(dist.values()))
        for k in on:
            rows.append({"name": pr["nom_statio"].strip(), "line": k,
                         "longitude": x, "latitude": y})
    print(f"tram stops snapped to line geometry: worst {worst:.1f} m "
          f"(cap {SNAP_MAX_M:.0f} m)")

    raw = pd.DataFrame(rows)
    platforms = raw.drop_duplicates(["name", "longitude", "latitude"]).copy()

    # --- collapse to stations, with a distance guard -------------------------
    g = gpd.GeoDataFrame(raw, geometry=gpd.points_from_xy(raw.longitude,
                                                          raw.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    out = []
    for name, grp in g.groupby("name"):
        cx, cy = grp.geometry.x.mean(), grp.geometry.y.mean()
        spread = float(np.hypot(grp.geometry.x - cx, grp.geometry.y - cy).max())
        if spread > SAME_NAME_MAX_SPREAD_M:
            sys.exit(f"{name!r}: rows {spread:.0f} m from their centre - two "
                     f"places share a name, and merging them would move a "
                     f"station. Split them by line before collapsing.")
        out.append({"station": name,
                    "lines": "/".join(sorted(set(grp["line"]))),
                    "latitude": grp["latitude"].mean(),
                    "longitude": grp["longitude"].mean()})
    st = pd.DataFrame(out)
    inter = st[st["lines"].str.contains("/")]
    print(f"{len(raw)} station-line rows -> {len(st)} stations, "
          f"{len(inter)} serving more than one line:")
    for _, r in inter.iterrows():
        print(f"    {r['station']:32} {r['lines']}")

    # --- gate 3, against OpenStreetMap ---------------------------------------
    elements, host = osm_load(config.OSM_ROUTES_JSON, "ilévia route relations")
    rels = [e for e in elements if e.get("type") == "relation"]
    expected, actual = {}, {}
    for key, (_mode, ref, _name) in config.LINES.items():
        mine = [r for r in rels if (r.get("tags") or {}).get("ref") == ref]
        per_direction = [
            sum(1 for m in r.get("members", ())
                if m.get("type") == "node"
                and (m.get("role") or "").startswith("stop"))
            for r in mine]
        expected[config.LINE_NAMES[key]] = max(per_direction) if per_direction else 0
        actual[config.LINE_NAMES[key]] = int(
            sum(1 for v in st["lines"] if key in v.split("/")))

    print()
    station_gates.verify_stations(
        city="Lille (Regional)", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED,
        expected_per_line=expected, actual_per_line=actual)
    print(f"    gate 3 source: OpenStreetMap route relations via {host} - the "
          f"stations are MEL's, so this is the independent count")

    nn = station_gates.nearest_neighbour_m(st["longitude"], st["latitude"],
                                           config.CRS_PROJECTED)
    print(f"    spacing: min {nn.min():.0f}  median {np.median(nn):.0f}  "
          f"mean {nn.mean():.0f}  max {nn.max():.0f} m")

    # --- the served communes ---------------------------------------------------
    communes = [(f["properties"]["code"], f["properties"]["nom"],
                 shape(f["geometry"]))
                for f in features(config.MEL_COMMUNES_GEOJSON)]
    placed, per_commune = [], defaultdict(Counter)
    for _, r in st.iterrows():
        pt = Point(r["longitude"], r["latitude"])
        hits = [(c, n) for c, n, geom in communes if geom.contains(pt)]
        if len(hits) != 1:
            sys.exit(f"{r['station']!r} falls in {len(hits)} MEL communes")
        code, nom = hits[0]
        placed.append(code)
        for line in r["lines"].split("/"):
            per_commune[(code, nom)][line] += 1
    st["commune_code"] = placed

    served = {c for c, _ in per_commune}
    expected_codes = set(config.EXPECTED_SERVED_COMMUNES)
    if served != expected_codes:
        sys.exit(f"the network now serves a different set of communes.\n"
                 f"  gained: {sorted(served - expected_codes)}\n"
                 f"  lost  : {sorted(expected_codes - served)}\n"
                 f"The scope IS this set, so a change is a decision - see "
                 f"config.EXPECTED_SERVED_COMMUNES.")

    with open(config.SERVED_COMMUNES_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["commune_code", "commune", "stations"] + list(config.LINES))
        for (code, nom), lines in sorted(per_commune.items(),
                                         key=lambda kv: -sum(kv[1].values())):
            n = int((st["commune_code"] == code).sum())
            w.writerow([code, nom, n] + [lines.get(k, 0) for k in config.LINES])
    print(f"\n  {len(served)} communes served -> "
          f"{config.SERVED_COMMUNES_CSV.relative_to(config.ROOT)}")

    boundary = unary_union([geom for c, _, geom in communes if c in served])
    config.SERVED_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "properties": {"communes": sorted(served)},
         "geometry": mapping(boundary)}), encoding="utf-8")
    area = to_l93(boundary).area / 1e6
    minx, miny, maxx, maxy = boundary.bounds
    print(f"  served area {area:.1f} km2, extent {miny:.4f}-{maxy:.4f} N, "
          f"{minx:.4f}-{maxx:.4f} E")

    st["stop_id"] = st["station"].str.lower().str.replace(r"[^a-z0-9]+", "-",
                                                          regex=True)
    keep = st[["stop_id", "station", "lines", "commune_code",
               "latitude", "longitude"]].sort_values("station")
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> "
          f"{config.STATIONS_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
