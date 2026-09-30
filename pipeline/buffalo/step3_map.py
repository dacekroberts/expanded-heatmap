"""Step 3 - Render Buffalo's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Buffalo-specific.

Input:  data/buffalo/processed/stations.csv
        data/buffalo/processed/businesses_clean.csv
        data/buffalo/processed/lines.geojson    (NFTA Metro Rail, step 1, OSM)
        data/buffalo/raw/city_boundary.geojson  (label anchoring)
Output: outputs/buffalo/heatmap.html

Run:  python pipeline/buffalo/step3_map.py

The line is OSM's, through step 1's GeoJSON (track ways only) and Madrid's
loader path, not load_osm_line_shapes, which would also draw each relation's
platform outlines.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.buffalo.config import (  # noqa: E402
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
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402

SYSTEM = "NFTA Metro Rail"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {k: (k, LINE_COLOURS[k], LINE_NAMES[k], LINE_LABEL_ENDS.get(k)) for k in LINE_NAMES}
    lines = load_geojson_line_shapes(LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(LINE_NAMES):
        sys.exit("no geometry for the line - a line this project draws must come "
                 "from real geometry")
    city = gpd.read_file(CITY_BOUNDARY_GEOJSON).to_crs(CRS_GEOGRAPHIC).geometry.union_all()
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"zip": str})
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Buffalo NFTA Metro Rail Business Density Heatmap",
        city_name="Buffalo",
        system_name=SYSTEM,
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=lines,
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city,
    )


if __name__ == "__main__":
    main()
