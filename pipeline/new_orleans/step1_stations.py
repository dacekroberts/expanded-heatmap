"""New Orleans step 1: every stop of the drawn streetcar lines.

    python pipeline/new_orleans/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the two
kept relations, collapsed by name. Scope is the City of New Orleans, as
TIGER draws it (Houston's layer). The whole line lies inside the
city, so step 3 draws OSM's relation whole. No stop is thinned.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.new_orleans import config  # noqa: E402

FETCH = "pipeline/new_orleans/fetch_sources.py"


def city_polygon():
    """The City of New Orleans (TIGER place 2255000), EPSG:4326."""
    if not config.CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.CITY_BOUNDARY_GEOJSON}\nRun: python {FETCH}")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    km2 = float(city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.CITY_AREA_KM2
    print(f"    New Orleans (TIGER place {config.CITY_GEOID}): {km2:,.1f} km2")
    if not lo <= km2 <= hi:
        sys.exit(f"the place polygon is {km2:,.1f} km2, outside {lo:,}-{hi:,}")
    return city.geometry.union_all()


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached inputs:")
    poly = city_polygon()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD,
                           name_aliases=config.NAME_ALIASES)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    # Gate 3 not run: no operator count was read for the line (the brief's 110 is
    # OSM's own count, checked below).
    station_gates.verify_stations(
        city="New Orleans", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M)

    places = gpd.GeoDataFrame([{"ref": config.CITY_GEOID, "name": "New Orleans",
                                "geometry": poly}], crs=config.CRS_GEOGRAPHIC)
    inside, outside = osm_tram.split_by_places(st, places, keep={config.CITY_GEOID})
    if len(outside):
        sys.exit("split_by_places should have exited on a stop in no place")
    print(f"\n  {len(st)} streetcar stops, all inside the city")
    if len(inside) != config.EXPECTED_STATIONS:
        sys.exit(f"{len(inside)} stations, not the brief's {config.EXPECTED_STATIONS} - "
                 f"re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the median gap is {d.median():.0f} m; the halved rings were chosen "
                 f"at 164 m - re-take the ring decision")

    # Every stop is in the city, so this is header-only; it stays written so a
    # stop that moves outside is recorded, not lost.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_in_scope", len(keep))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
