"""Step 3 - Render Tbilisi's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Tbilisi-specific.

Input:  data/tbilisi/processed/stations.csv
        data/tbilisi/processed/businesses_clean.csv
        data/tbilisi/processed/lines.geojson        (the two lines, step 1, OSM)
        data/tbilisi/processed/city_boundary.geojson (label anchoring)
Output: outputs/tbilisi/heatmap.html

Run:  python pipeline/tbilisi/step3_map.py

The lines are OSM's, through step 1's GeoJSON and Madrid's loader path.
Business names are in Georgian script, which the shared font stack reaches
through Segoe UI on Windows and the browser's own fallback elsewhere.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.tbilisi.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_REFS,
    LINES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

SYSTEM = "Tbilisi Metro"
# Per-line label end override: "start" or "end"; None = automatic.
LINE_LABEL_ENDS = {}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINES_GEOJSON, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")
    specs = {k: (k, LINE_COLOURS[k], LINE_REFS[k], LINE_LABEL_ENDS.get(k)) for k in LINE_REFS}
    lines = load_geojson_line_shapes(LINES_GEOJSON, specs, SYSTEM)
    if set(lines) != set(LINE_REFS):
        sys.exit("a line has no geometry - a line this project draws must come "
                 "from real geometry")
    city = gpd.read_file(CITY_BOUNDARY_GEOJSON).to_crs(CRS_GEOGRAPHIC).geometry.union_all()
    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype={"activity_code": str, "stat_id": str})
    print(f"  {len(stations):,} stations, {len(businesses):,} storefronts")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Tbilisi Metro Business Density Heatmap",
        city_name="Tbilisi",
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
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
