"""Step 3 - Render Kitchener–Waterloo (Regional)'s heatmap to a standalone
HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Kitchener–Waterloo-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/kitchener_waterloo/processed/stations.csv
        data/kitchener_waterloo/processed/businesses_clean.csv
        data/kitchener_waterloo/processed/lines.geojson       (ION, step 1, OSM)
        data/kitchener_waterloo/raw/cities_and_towns.geojson  (label anchoring)
Output: outputs/kitchener_waterloo/heatmap.html

Run:  python pipeline/kitchener_waterloo/step3_map.py

The line is OSM's, through step 1's GeoJSON (track ways only) and Madrid's
loader path, as Ottawa's and Buffalo's are.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.kitchener_waterloo.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "ION"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {k: (k, LINE_COLOURS[k], LINE_NAMES[k], LINE_LABEL_ENDS.get(k)) for k in LINE_NAMES}
    lines = load_geojson_line_shapes(LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(LINE_NAMES):
        sys.exit(f"geometry for {sorted(lines)}, not every line in {sorted(LINE_NAMES)} - a "
                 "line this project draws must come from real geometry")
    cities = gpd.read_file(CITY_BOUNDARY_GEOJSON).to_crs(CRS_GEOGRAPHIC).geometry.union_all()
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    for col in ("latitude", "longitude"):
        businesses[col] = pd.to_numeric(businesses[col])
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Kitchener–Waterloo ION Business Density Heatmap",
        city_name="Kitchener–Waterloo",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=cities,
    )


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # the en dash in the city's name. UTF-8 regardless.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
