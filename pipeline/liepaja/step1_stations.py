"""Liepāja step 1: every stop of the one tram line.

    python pipeline/liepaja/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
two ref-1 relations, plus three stops the relations miss, added by node
(config.STATION_ADD). The whole line lies inside the city, so step 3 draws
OSM's relation whole. No stop is thinned (owner, call 13).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.liepaja import config  # noqa: E402

FETCH = "pipeline/liepaja/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def city_polygon():
    """The city of Liepāja (OSM relation 13048685), EPSG:4326, area-gated."""
    rels = [e for e in osm_tram.read_elements(config.OSM_CITY_JSON, "city boundary", FETCH)
            if e["type"] == "relation" and e["id"] == config.OSM_CITY_RELATION]
    if len(rels) != 1:
        sys.exit(f"relation {config.OSM_CITY_RELATION} not in {config.OSM_CITY_JSON.name}")
    outer, inner = _rings(rels[0], "outer"), _rings(rels[0], "inner")
    if outer is None or outer.is_empty:
        sys.exit("Liepāja's outer ways did not close into a polygon")
    poly = outer.difference(inner) if inner is not None else outer
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.CITY_AREA_KM2
    print(f"    {rels[0]['tags'].get('name')}: {km2:.1f} km2")
    if not lo <= km2 <= hi:
        sys.exit(f"the city polygon is {km2:.1f} km2, outside {lo}-{hi}")
    return poly


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    poly = city_polygon()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    # Gate 3 not run: no operator count was read for the line (the brief's 18
    # is the screen's own OSM count, not the operator's).
    station_gates.verify_stations(
        city="Liepāja", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M)

    places = gpd.GeoDataFrame([{"ref": config.ATVK, "name": config.CITY_NAME_LV,
                                "geometry": poly}], crs=config.CRS_GEOGRAPHIC)
    inside, outside = osm_tram.split_by_places(st, places, keep={config.ATVK})
    if len(outside):
        sys.exit("split_by_places should have exited on a stop in no place")
    print(f"\n  {len(st)} tram stations, all inside the city")
    if len(inside) != 18:
        sys.exit(f"{len(inside)} stations, not the screen's 18 - re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m; the halved rings were chosen "
                 f"at 329 m - re-take the ring decision")

    # Every stop is in the city, so this is header-only; it stays written so a
    # stop that moves outside is recorded, not lost.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stop_positions_added", int((q["source"] == "added").sum()))
    emit("stations_in_scope", len(keep))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
